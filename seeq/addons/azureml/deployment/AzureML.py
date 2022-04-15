import textwrap
import json
import numpy as np
from pathlib import Path
from typing import Dict
import urllib.request
from urllib.error import HTTPError

import pandas as pd

from seeq.addons.azureml import backend
from extcalc import KeywiseExternalCalculationScript

MAX_INPUT_SIGNALS = 10
DIRECTORY = Path(__file__).resolve().parent


def get_params():
    parameters = [
        {'Name': 'endpoint_name', 'Formula': '"http://"'},
        {'Name': 'signal1', 'Formula': '1.toSignal()'},

    ]

    for i in range(MAX_INPUT_SIGNALS - 1):
        parameters.append({'Name': f'signal{i + 2}', 'Formula': '1.toSignal()', 'Optional': True})

    return parameters


class AzureML(KeywiseExternalCalculationScript):

    def __init__(self):
        super().__init__()
        self.endpoint = None
        self.i = 0
        self.config_file = DIRECTORY.joinpath('test_config.ini')
        self.inputs_provider = backend.ModelInputsProvider(config_file=self.config_file)

    def initialize(self):
        pass

    def function_definition(self) -> Dict[str, str]:
        """
        Defines the parameters, formula, name, examples and documentation
        for this calculation.

        :return: dictionary containing function details
        """

        parameters = get_params()

        examples = [
            {
                'Formula': '@@functionName@@($endpoint_name, $signal1)',
                'Description': 'Takes 1 input signal, calls the AzureML endpoint, and returns one signal'
            },
            {
                'Formula': '@@functionName@@($endpoint_name, $signal1, $signal2, $signal3)',
                'Description': 'Takes 3 input signals, calls the AzureML endpoint, and returns one signal'

            }
        ]
        optional_signals = ",".join([f'$signal{i + 2}' for i in range(MAX_INPUT_SIGNALS - 1)])
        formula = f'externalCalculation(@@scriptId@@, $endpoint_name.toSignal(), $signal1, {optional_signals})'

        function_details = {
            'Name': 'myCoolFunction',
            'Documentation': textwrap.dedent(""" text goes here
                """).strip(),
            'Formula': formula,
            'Parameters': parameters,
            'Examples': examples
        }
        return function_details

    def validate(self, validation_object):
        """
        # type: (ValidationObject) -> None

        """

    def compute(self, key, samples_for_key):
        # samples_for_key = ['endpoint_name', 2, 3, ...]
        try:
            if self.endpoint is None:
                self.get_endpoint(samples_for_key[0])

            data = pd.DataFrame(data=[samples_for_key[1:]], index=[key])
            result = self.run_azureml(data)
            return key, result

        except Exception as e:
            # print(e)
            return key, np.nan

    def compute_output_mode(self):
        return 'NUMERIC'

    def close(self):
        pass

    def get_endpoint(self, endpoint_name):
        if endpoint_name not in self.inputs_provider.endpoints.keys():
            return
        self.endpoint = self.inputs_provider.endpoints[endpoint_name]

    def _prepare_request(self, data):
        body = data.to_json(date_format='iso').encode()
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.endpoint.primaryKey}'
        }
        return urllib.request.Request(self.endpoint.scoringUri, body, headers)

    def run_azureml(self, data):
        """
        Posts a request to the Azure ML endpoint_uri with the input data and,
        if successful, retrieves the serialized result signal

        Returns
        -------
        -: None

        """
        request = self._prepare_request(data)
        # Hit the endpoint with the data, get the response, and push into Seeq
        try:
            response = urllib.request.urlopen(request)
            result = response.read()
            result_signal = pd.read_json(json.loads(result))
            return result_signal.values[0][0]

        except HTTPError as error:
            return error.reason
