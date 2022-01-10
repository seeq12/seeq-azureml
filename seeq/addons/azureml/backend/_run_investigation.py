import json
import os
import ssl
import copy
import pandas as pd
from typing import Union
from datetime import datetime
import urllib.request
import hashlib
from urllib.error import HTTPError
from seeq import spy
from seeq.addons.azureml.utils import AzureMLException

DEFAULT_DATASOURCE_NAME = 'Azure ML'
DEFAULT_WORKBOOK_PATH = 'Data Lab >> Azure ML Integration'
DEFAULT_WORKBOOK_NAME = DEFAULT_WORKBOOK_PATH.split('>>')[-1].strip()
DEFAULT_WORKSHEET_NAME = 'From Azure ML Integration'
DEFAULT_RESULT_SIGNAL_NAME = 'Prediction Azure ML'


class RunInvestigation:
    """
    Takes the input parameters supplied by the user (typically, via Azure ML
    Integration UI), posts a request to the Azure ML model, gets a result
    signal back from Azure ML and pushes the result back to Seeq.

    This class assumes that the Azure ML model returns only ONE signal.

    Attributes
    ----------
    input_signals: dict
        A dictionary whose keys are the names of the input signals and whose
        values are the Seeq IDs of the input signals.
    result_name: str
        The name of the result signal that will be pushed to Seeq.
    az_model_name: str
        Name of the Azure ML model used to compute the result signal.
    az_model_version: str
        The version of the Azure ML model used to compute the result signal.
    start: str
        The starting time for which to pull data with spy.pull.
    end: str
        The end time for which to pull data with spy.pull.
    grid: str
        A period to use for interpolation in the spy.pull call, such that all
        returned samples have the same timestamps.
    workbook: str
        The ID of the Seeq workbook that all pushed items will be 'scoped to'.
    worksheet: str
        The name of a worksheet within the workbook to create/update that will
        render the result signal that has been pushed.
    datasource: str
        The name of the datasource within which to contain all the pushed items.
    endpoint_uri: str
        The endpoint identifier of the AzureML model used to compute the result
        signal.
    aml_primary_key: str
        The primary key of the Azure ML endpoint
    quiet: bool
        If True, suppresses progress output. Note that when status is
        provided, the quiet setting of the Status object that is passed
        in takes precedence.
    data: pd.DataFrame
        A DataFrame with timestamps as Index and input signals data as
        columns. This dataset is passed in the request to the endpoint_uri to
        compute the resulting signal.
    result_signal: pd.DataFrame
        A DataFrame with timestamps as Index and one column with the
        data of the result signal
    pushed_df: pd.DataFrame
        A DataFrame with the metadata for the result signal pushed, along with
        any errors and statistics about the operation.
    error_info: str
        Information on the most recent error that has occurred.

    Methods
    -------
    validate_inputs()
        Validates the type of the input parameters
    allow_self_signed_https(allowed)
        Checks whether to allow self-signed https certificates
    get_seeq_data()
        Pulls the input signals required for the Azure ML model from Seeq
    run()
        Posts a request to the Azure ML endpoint_uri with the input data and,
        if successful, retrieves the serialized result signal
    push_to_seeq()
        Pushes the result signal from Azure ML model to Seeq.

    """

    def __init__(self,
                 input_signals: dict,
                 result_name: str,
                 az_model_name: str,
                 az_model_version: str,
                 start: Union[pd.Timedelta, datetime],
                 end: Union[pd.Timedelta, datetime],
                 grid: Union[str, None] = '5 min',
                 workbook: Union[str, None] = DEFAULT_WORKBOOK_PATH,
                 worksheet: Union[str, None] = DEFAULT_WORKSHEET_NAME,
                 datasource: Union[str, None] = DEFAULT_DATASOURCE_NAME,
                 endpoint_uri: Union[str, None] = None,
                 aml_primary_key: Union[str, None] = None,
                 self_signed_certificate=True,
                 quiet=True):
        """

        Parameters
        ----------
        input_signals: dict
            A dictionary whose keys are the names of the input signals and whose
            values are the Seeq IDs of the input signals.
        result_name: str
            The name of the result signal that will be pushed to Seeq.
        az_model_name: str
            Name of the Azure ML model used to compute the result signal.
        az_model_version: str
            The version of the Azure ML model used to compute the result signal.
        start: str
            The starting time for which to pull data with spy.pull.
        end: str
            The end time for which to pull data with spy.pull.
        grid: str, default '5 min'
            A period to use for interpolation in the spy.pull call, such that all
            returned samples have the same timestamps.
        workbook: str, default 'Data Lab >> Azure ML Integration'
            The ID of the Seeq workbook that all pushed items will be 'scoped to'.
        worksheet: str, default 'From Azure ML Integration'
            The name of a worksheet within the workbook to create/update that will
            render the result signal that has been pushed.
        datasource: str, default 'Azure ML'
            The name of the datasource within which to contain all the pushed items.
        endpoint_uri: str
            The endpoint identifier of the AzureML model used to compute the result
            signal.
        aml_primary_key: str
            The primary key of the Azure ML endpoint
        self_signed_certificate: bool, default True
            If True, allows self-signed https certificates
        quiet: bool
            If True, suppresses progress output. Note that when status is
            provided, the quiet setting of the Status object that is passed
            in takes precedent.
        """

        self.input_signals = input_signals
        self.result_name = result_name
        self.az_model_name = az_model_name
        self.az_model_version = az_model_version
        self.start = start
        self.end = end
        self.grid = grid
        self.workbook = workbook
        self.worksheet = worksheet
        self.datasource = datasource
        self.endpoint_uri = endpoint_uri
        self.aml_primary_key = aml_primary_key
        self.quiet = quiet

        self.validate_inputs()
        self.allow_self_signed_https(self_signed_certificate)

        self.data = pd.DataFrame()
        self.result_signal = pd.DataFrame()
        self.pushed_df = None
        self.error_info = None

    def validate_inputs(self):
        """
        Validates the type of the input parameters

        Returns
        -------
        -: None

        """
        for name, idd in self.input_signals.items():
            if not spy.utils.is_guid(idd):
                raise TypeError(f'The signal ID "{idd}" of the signal "{name}" is malformed')

        if not (isinstance(self.start, pd.Timedelta) or isinstance(self.start, datetime)):
            raise TypeError(f"The 'start' argument must be of type pd.Timedelta or datetime.datetime. "
                            f"Got start: {type(self.start)}")

        if not (isinstance(self.end, pd.Timedelta) or isinstance(self.end, datetime)):
            raise TypeError(f"The 'start' argument must be of type pd.Timedelta or datetime.datetime. "
                            f"Got start: {type(self.end)}")

        for prop in ['result_name', 'az_model_name', 'az_model_version', 'workbook', 'worksheet', 'datasource',
                     'endpoint_uri', 'aml_primary_key']:
            if prop is None:
                continue
            if not isinstance(getattr(self, prop), str):
                raise TypeError(f"The {prop} argument must be of type str. Got {type(getattr(self, prop))}")

        if not isinstance(self.endpoint_uri, str):
            raise TypeError(f"Argument 'endpoint_uri' must be a string")

        try:
            pd.Timedelta(self.grid)
        except ValueError as e:
            raise e

    @staticmethod
    def allow_self_signed_https(allowed):
        """
        Checks whether to allow self-signed https certificates

        Parameters
        ----------
        allowed: bool
            If True, allows self-signed https certificates

        Returns
        -------
        -: None

        """
        # bypass the server certificate verification on client side
        if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
            ssl._create_default_https_context = ssl._create_unverified_context

    def get_seeq_data(self):
        """
        Pulls the input signals required for the Azure ML model from Seeq

        Returns
        -------
        -: None

        """
        signals = copy.deepcopy(self.input_signals)  # spy.pull is modifying the input dict
        data = spy.pull(pd.DataFrame([{"ID": x, 'Type': 'Signal'} for x in signals.values()]),
                        start=self.start,
                        end=self.end,
                        grid=self.grid,
                        header='ID',
                        quiet=self.quiet)
        cols = dict(zip(self.input_signals.values(), self.input_signals.keys()))
        data.rename(columns=cols, inplace=True)
        data.dropna(inplace=True)
        if len(data) == 0:
            raise ValueError("There is no data available for these input signals during the selected time range")
        self.data = data

    def _prepare_request(self):
        self.get_seeq_data()
        body = self.data.to_json(date_format='iso').encode()
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.aml_primary_key}'
        }
        return urllib.request.Request(self.endpoint_uri, body, headers)

    def run(self):
        """
        Posts a request to the Azure ML endpoint_uri with the input data and,
        if successful, retrieves the serialized result signal

        Returns
        -------
        -: None

        """
        request = self._prepare_request()
        # Hit the endpoint with the data, get the response, and push into Seeq
        try:
            response = urllib.request.urlopen(request)
            result = response.read()
            self.result_signal = pd.read_json(json.loads(result))

        except HTTPError as error:
            self.error_info = error
            raise AzureMLException(code=error.code, reason=error.reason, message="Azure request failed")

    def push_to_seeq(self):
        """
        Pushes the result signal from Azure ML model to Seeq.

        Returns
        -------
        -: None
        """
        if len(self.result_signal.columns) > 1:
            raise AzureMLException(code=None, reason=None,
                                   message=f'This implementation assumes a single signal resulting from '
                                           f'the Azure ML model')
        s = self.result_name + self.az_model_name + self.az_model_version + str(set(self.input_signals.values()))
        hash_object = hashlib.sha1(s.encode())
        self.result_signal.columns = [hash_object.hexdigest()]  # Rename the name coming from Azure ML model

        self.pushed_df = spy.push(
            self.result_signal,
            workbook=self.workbook,
            datasource=self.datasource,
            worksheet=self.worksheet,
            status=spy.Status(quiet=self.quiet)
        )

        separator = ",\n"
        description = f"Model Name: {self.az_model_name}\nModel Version: {self.az_model_version}\n" \
                      f"Inputs: \n[{separator.join(self.input_signals.values())}]"

        metadata = self.pushed_df.copy()
        metadata['Original Name'] = hash_object.hexdigest()
        metadata["Name"] = self.result_name,
        metadata["Description"] = description,
        metadata['Model Name'] = self.az_model_name,
        metadata["Model Version"] = self.az_model_version,
        metadata["Input Signals"] = str(list(set(self.input_signals.values()))),
        metadata["Type"] = "Signal"
        spy.push(metadata=metadata, quiet=self.quiet)
