import pandas as pd
import tzlocal
import ipyvuetify as v
from seeq import spy
from seeq.sdk.rest import ApiException
from IPython.display import display, Javascript, clear_output, HTML
from seeq.addons.azureml.utils import get_workbook_worksheet_workstep_ids, AzureMLException
from seeq.addons.azureml.backend import RunInvestigation, ModelInputsProvider
from seeq.addons.azureml import ui_components

DEFAULT_WORKSHEET_NAME = 'From Azure ML Integration'


class MlOperate:
    """
    Main class for the Seeq - Azure Ml integration Add-on. Creates an instance
    of the Add-on UI and passes the callbacks for the different events.

    Attributes
    ----------
    workbook_id: str
        The ID of the Seeq workbook where the Add-on was instantiated
    config_file: str
        The configuration file with the necessary information to connect to the
        Azure ML service. By default, the file is located in ~/.seeq/aml_config.ini
    default_time_delta: str
        Default time delta to populate the start time of the investigate range
    deploy_frequency: pd.Timedelta
        The schedule frequency for the "deploy" option as a pandas.Timedelta
    inputs_provider: seeq.addons.azureml.backend.ModelInputsProvider
        An instance of the ModelInputsProvider object that gets the input signal
        IDs from Seeq that are required by the Azure ML model.
    app: seeq.addons.azureml.ui_components.AppLayout
        An instance of the Add-on UI
    """

    v.theme.themes.light.success = '#007960'
    v.theme.themes.light.primary = '#007960'
    v.theme.themes.light.secondary = '#EEEEEE'
    v.theme.themes.dark.secondary = '#EEEEEE'

    def __init__(self, sdl_notebook_url, config_file=None):
        display(HTML("<style>#appmode-leave {display: none;}"))
        self.workbook_id, _, __ = get_workbook_worksheet_workstep_ids(sdl_notebook_url)
        self.config_file = config_file
        self.default_time_delta = '1 hour'
        self.deploy_frequency = None
        self.inputs_provider = None

        self.app = ui_components.AppLayout(endpoint_on_change=self.on_endpoint_dropdown_change,
                                           asset_on_change=self.on_asset_dropdown_change,
                                           action_on_change=self.on_action_dropdown_change,
                                           result_name_on_change=self.on_result_name_change,
                                           start_on_change=self.on_date_range_change,
                                           end_on_change=self.on_date_range_change,
                                           jobname_on_change=self.on_jobname_change,
                                           frequency_on_change=self.on_frequency_change,
                                           button_on_click=self.on_submit_click
                                           )
        self.set_disable_value_for_all_components(disabled=True)

    def set_disable_value_for_all_components(self, disabled=True):
        self.app.model_inputs.endpoint_disabled = disabled
        self.app.model_inputs.asset_disabled = disabled
        self.app.model_action.action_disabled = disabled
        self.app.model_action.result_name_disabled = disabled
        self.app.model_action.investigate_range.start_range.disabled = disabled
        self.app.model_action.investigate_range.end_range.disabled = disabled
        self.app.model_action.deploy_input_form.jobname_disabled = disabled
        self.app.model_action.deploy_input_form.frequency_disabled = disabled
        self.app.model_summary.button_disabled = disabled

    def set_cards_visible_spinner_invisible(self, visible=True):
        self.app.model_inputs.model_inputs_visible = visible
        self.app.model_action.model_action_visible = visible
        self.app.model_summary.model_summary_visible = visible
        self.app.spinner_visible = not visible
        self.app.spinner_message_visible = not visible

    def validate_forms(self):
        if not self.app.model_action.investigation_form_valid:
            self.app.model_summary.button_disabled = True
            return
        if self.app.model_action.selection == 'Deploy':
            if not self.app.model_action.deploy_input_form.deploy_form_valid:
                self.app.model_summary.button_disabled = True
                return
        if self.app.model_summary.time_range_warning:
            self.app.model_summary.button_disabled = True
            return
        self.app.model_summary.button_disabled = False

    def run(self):
        display(self.app)
        self.populate_available_aml_endpoints()
        clear_output()
        return self.app

    def set_error_message(self, title=None, message=None, status='ERROR', disabled_submit=True):
        self.app.model_summary.message_type = status
        self.app.model_summary.error_title = title
        self.app.model_summary.error_message = message
        if disabled_submit:
            self.app.model_summary.button_disabled = True

    def set_spinner_message(self, title=None, message=None, status='RUNNING'):
        self.app.message_status = status
        self.app.spinner_message_title = title
        self.app.spinner_message = message

    def populate_available_aml_endpoints(self):
        self.set_cards_visible_spinner_invisible(visible=False)
        self.set_spinner_message(message="Connecting to Azure ML service")

        try:
            self.inputs_provider = ModelInputsProvider(config_file=self.config_file)
        except AzureMLException as e:
            self.set_spinner_message(title="Azure Exception", message=str(e), status="ERROR")
            self.app.spinner_visible = False
            return
        # populate dropdown with available model endpoints
        self.app.model_inputs.endpoint_items = list(self.inputs_provider.endpoints.keys())
        self.app.model_inputs.endpoint_disabled = False
        self.set_cards_visible_spinner_invisible()

    def populate_assets_dropdown(self, items: list = None):
        self.app.model_inputs.asset_items = items
        self.app.model_inputs.asset_visible = False if not items else True
        self.app.model_inputs.asset_disabled = True if not items else False

        if not items:
            self.app.model_summary.asset_info = "Not applicable"

    def populate_summary(self, **kwargs):
        validate_model_summary_properties(kwargs.keys())
        for key, value in kwargs.items():
            if value is not None:
                setattr(self.app.model_summary, key, value)

    def populate_investigate_range(self):
        current_time = pd.Timestamp.today().floor(freq='s')
        end_time = current_time.tz_localize(str(tzlocal.get_localzone()))
        if self.app.model_action.investigate_range.end_range.value is None:
            self.app.model_action.investigate_range.end_range.value = end_time
        else:
            end_time = self.app.model_action.investigate_range.end_range.value
        self.app.model_action.investigate_range.start_range.value = end_time - pd.Timedelta(self.default_time_delta)
        self.app.model_action.investigate_range.end_range.value = end_time
        self.set_disable_value_for_all_components(disabled=False)
        self.validate_forms()

    def on_endpoint_dropdown_change(self, data):
        if data is None:
            return
        self.set_disable_value_for_all_components(disabled=True)
        self.app.model_inputs.endpoint_disabled = False
        self.set_error_message(disabled_submit=False)
        self.app.model_inputs.endpoint_loading = True
        self.app.model_inputs.asset_visible = False

        try:
            self.inputs_provider.update_assets_from_endpoint(self.inputs_provider.endpoints[data])
        except AzureMLException as e:
            self.set_error_message(title="AzureMLException: ", message=str(e))
            self.validate_forms()
            return
        except ApiException as e:
            self.set_error_message(title="ApiException: ", message=str(e))
            self.validate_forms()
            return

        if self.inputs_provider.asset_paths is None:
            try:
                self.inputs_provider.update_signal_inputs_from_endpoint(self.inputs_provider.endpoints[data])
            except AzureMLException as e:
                self.set_error_message(title="AzureMLException: ", message=str(e))
                self.validate_forms()
                return
            except ApiException as e:
                self.set_error_message(title="ApiException: ", message=str(e))
                self.validate_forms()
                return
            self.populate_investigate_range()
            self.populate_summary(endpoint_info=data,
                                  asset_info=list(self.inputs_provider.asset_path_from_signals.keys())[0] if
                                  self.inputs_provider.asset_path_from_signals is not None else "NA",
                                  signals_info=", ".join(self.inputs_provider.model_signal_inputs.keys()))
            self.on_action_dropdown_change(self.app.model_action.selection)
        else:
            items = list(self.inputs_provider.asset_paths.keys())
            self.populate_assets_dropdown(items)
            self.populate_summary(endpoint_info=data, asset_info='', signals_info="")
            if self.app.model_inputs.asset_selection in items:  # if there is already an asset selection.
                # Unfortunately, ipyvuetify assigns the value of the selection till the end of the callback
                # then, we manually assign it to `endpoint_selection` before executing `on_asset_dropdown_change`
                self.app.model_inputs.endpoint_selection = data
                self.on_asset_dropdown_change(data=self.app.model_inputs.asset_selection)

        self.app.model_inputs.endpoint_loading = False
        self.validate_forms()

    def on_asset_dropdown_change(self, data):
        self.set_error_message(disabled_submit=False)
        if data is None:
            return
        try:
            self.inputs_provider.update_signal_inputs_from_endpoint(
                self.inputs_provider.endpoints[self.app.model_inputs.endpoint_selection],
                self.inputs_provider.asset_paths[data])
        except AzureMLException as e:
            self.set_error_message(title="AzureMLException: ", message=str(e))
            self.validate_forms()
            return
        except ApiException as e:
            self.set_error_message(title="ApiException: ", message=str(e))
            self.validate_forms()
            return
        self.populate_investigate_range()
        self.populate_summary(asset_info=data,
                              signals_info=", ".join(self.inputs_provider.model_signal_inputs.keys()))
        self.on_action_dropdown_change(self.app.model_action.selection)
        self.validate_forms()

    def on_action_dropdown_change(self, data):
        self.set_error_message(disabled_submit=False)
        if data == 'Investigate':
            self.populate_summary(jobname_info="NA", frequency_info="NA")
            self.on_date_range_change()
        elif data == 'Deploy':
            self.populate_summary(start_info="NA", end_info="")
            self.on_jobname_change(self.app.model_action.deploy_input_form.jobname)
            self.on_frequency_change(self.app.model_action.deploy_input_form.frequency)
        self.app.model_action.selection = data
        self.validate_forms()

    def on_date_range_change(self, *_):
        self.set_error_message(disabled_submit=False)
        start = self.app.model_action.investigate_range.start_range.value
        end = self.app.model_action.investigate_range.end_range.value
        if start is None or end is None:
            self.validate_forms()
            return
        if start > end:
            self.app.model_summary.time_range_warning = True
            start = 'Invalid'
            self.populate_summary(start_info=str(start), end_info=str(end))
            self.validate_forms()
            return
        self.app.model_summary.time_range_warning = False
        self.populate_summary(start_info=str(start), end_info=str(end))
        self.validate_forms()

    def on_result_name_change(self, data):
        self.set_error_message(disabled_submit=False)
        self.populate_summary(result_signal_info=data)
        self.validate_forms()

    def on_jobname_change(self, data):
        self.set_error_message(disabled_submit=False)
        self.populate_summary(jobname_info=data)
        self.validate_forms()

    def on_frequency_change(self, data):
        self.set_error_message(disabled_submit=False)
        self.populate_summary(frequency_info="")
        try:
            self.deploy_frequency = pd.Timedelta(self.app.model_action.deploy_input_form.frequency.lower().replace(
                'every', ''))
        except ValueError as e:
            self.set_error_message(title="ValueError: ", message=str(e))
            # manually disabling the button since the check in the try block is not implemented in Rules of the Template
            self.app.model_summary.button_disabled = True
            return

        self.populate_summary(frequency_info=data)
        self.validate_forms()

    def on_submit_click(self, data):
        self.set_error_message(disabled_submit=False)
        self.validate_forms()
        if self.app.model_summary.button_disabled:
            self.set_error_message(title="Incomplete form: ", message=f'Complete all required fields')
            return
        if not self.inputs_provider.model_signal_inputs:
            self.set_error_message(title="Wrong input: ", message=f'Could not find input signals for model endpoint "'
                                                                  f'{self.app.model_inputs.endpoint_selection}"')
            return

        if self.app.model_action.selection == 'Investigate':
            self.app.model_summary.button_loading = True

            investigation = RunInvestigation(input_signals=self.inputs_provider.model_signal_inputs,
                                             result_name=self.app.model_action.result_name,
                                             az_model_name=self.inputs_provider.model_name,
                                             az_model_version=str(self.inputs_provider.model_version),
                                             start=self.app.model_action.investigate_range.start_range.value,
                                             end=self.app.model_action.investigate_range.end_range.value,
                                             grid=self.inputs_provider.model_sample_rate,
                                             workbook=self.workbook_id,
                                             worksheet=DEFAULT_WORKSHEET_NAME,
                                             endpoint_uri=self.inputs_provider.model_endpoint_uri,
                                             aml_primary_key=self.inputs_provider._model_primary_key,
                                             quiet=True)

            try:
                investigation.run()
                investigation.push_to_seeq()
            except AzureMLException as e:
                self.set_error_message(title="AzureMLException: ", message=str(e))
                self.app.model_summary.button_loading = False
                return
            except ValueError as e:
                self.set_error_message(title="Value Error: ", message=str(e))
                self.app.model_summary.button_loading = False
                return

            try:
                wb = spy.workbooks.pull(pd.DataFrame([
                    {
                        'ID': self.workbook_id,
                        'Workbook Type': 'Analysis',
                        'Type': 'Workbook'
                    }
                ]), status=spy.Status(quiet=True))[0]
            except ApiException as e:
                self.set_error_message(title="ApiException: ", message=str(e))
                self.app.model_summary.button_loading = False
                return

            try:
                ws = [x for x in wb.worksheets if x.name == DEFAULT_WORKSHEET_NAME][0]
            except IndexError as e:
                self.set_error_message(title="IndexError: ", message=str(e))
                return

            self.app.model_summary.button_loading = False
            display(Javascript(f'window.open("{ws.url}");'))

        elif self.app.model_action.selection == 'Deploy':
            self.app.model_summary.button_loading = True
            job_parameters = {
                'Schedule': self.app.model_action.deploy_input_form.frequency,
                'Frequency': self.deploy_frequency,
                'Input Signals': self.inputs_provider.model_signal_inputs,
                'Result Name': self.app.model_action.result_name,
                'AZ model name': self.inputs_provider.model_name,
                'AZ model version': str(self.inputs_provider.model_version),
                'Grid': self.inputs_provider.model_sample_rate,
                'Workbook': self.workbook_id,
                'Worksheet': DEFAULT_WORKSHEET_NAME,
                'Endpoint': self.inputs_provider.model_endpoint_uri,
                'aml_primary_key': self.inputs_provider._model_primary_key,
                'User': f'{spy.user.first_name} {spy.user.last_name}',
                'Job Name': "job name"
                }
            url = f"{spy.utils.get_data_lab_project_url()}/notebooks/deployment/azureml_integration_deploy_model.ipynb"

            jobs = pd.DataFrame([job_parameters])
            spy.jobs.push(jobs, datalab_notebook_url=url, quiet=True)
            self.app.model_summary.button_loading = False
            self.set_error_message(title='SUCCESS: ', message='Job has been scheduled', status='SUCCESS')


def validate_model_summary_properties(props):
    allowed_kwargs = ['endpoint_info', 'asset_info', 'signals_info', 'start_info', 'end_info', 'jobname_info',
                      'frequency_info', 'result_signal_info']
    for prop in props:
        if prop not in allowed_kwargs:
            raise KeyError(f'Property "{prop}" is not a recognized Model Summary property')
