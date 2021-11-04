import ipyvuetify as v
import traitlets
from pathlib import Path
from typing import Callable

CURRENT_DIR = Path(__file__).parent.resolve()


class ModelSummary(v.VuetifyTemplate):
    """
    UI component - Model Summary card

    Attributes
    ----------
    template_file: str
        Modifies the VueTemplate.template_file attribute with the
        seeq.addons.azureml.ui_components.templates._model_summary.vue template.
    model_summary_visible: bool, default True
        If True, the entire Model Summary card will be visible. Otherwise,
        the entire Model Inputs card will not be visible.
    endpoint_info: str
        Displays the selected value of the endpoints dropdown of the Model
        Inputs card.
    asset_info: str
        Displays the selected value of the assets dropdown of the Model Inputs
        card.
    signals_info: str
        Displays the input signal names that will be send to the Azure ML model
        endpoint.
    start_info: str
        Displays the start time of the investigation range selected in the Model
        Action card if the "investigate" option is selected.
    end_info: str
        Displays the end time of the investigation range selected in the Model
        Action card if the "investigate" option is selected.
    result_signal_info: str
        Displays the name of the result signal supplied in the Model Actions
        card.
    time_range_warning: bool
        Displays a warning in red color if the start time is greater than the
        end time in the investigation range
    jobname_info: str
        Displays the jobname supplied in the Model Actions if the "deploy"
        option is selected
    frequency_info: str
        Displays the frequency supplied in the Model Actions if the "deploy"
        option is selected
    button_disabled: bool
        If True, the submit button is disabled. Otherwise, it is enabled.
    button_loading: bool, default False
        If True, the submit button shows a loading spinner. Otherwise, it
        shows the name of the button.
    error_title: str
        Title of the error_message displayed to the left of error_message.
    error_message: str
        Message to be display at the bottom of the Model Summary card.
    message_type: {SUCCESS, ERROR}
        Allows to color the message depending on the type selected.

    """

    template_file = str(CURRENT_DIR.joinpath('templates', '_model_summary.vue'))
    model_summary_visible = traitlets.Bool(default_value=True).tag(sync=True)
    endpoint_info = traitlets.Unicode(allow_none=True).tag(sync=True)
    asset_info = traitlets.Unicode(allow_none=True).tag(sync=True)
    signals_info = traitlets.Unicode(allow_none=True).tag(sync=True)
    start_info = traitlets.Unicode(allow_none=True).tag(sync=True)
    end_info = traitlets.Unicode(allow_none=True).tag(sync=True)
    result_signal_info = traitlets.Unicode(allow_none=True).tag(sync=True)
    time_range_warning = traitlets.Bool(allow_none=True).tag(sync=True)
    jobname_info = traitlets.Unicode(allow_none=True).tag(sync=True)
    frequency_info = traitlets.Unicode(allow_none=True).tag(sync=True)
    button_disabled = traitlets.Bool(allow_none=True).tag(sync=True)
    button_loading = traitlets.Bool(default_value=False).tag(sync=True)
    error_title = traitlets.Unicode(allow_none=True).tag(sync=True)
    error_message = traitlets.Unicode(allow_none=True).tag(sync=True)
    message_type = traitlets.Unicode(allow_none=True).tag(sync=True)

    def __init__(self, *args, button_on_click: Callable[[str], None] = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.endpoint_info = kwargs.get('endpoint_info')
        self.asset_info = kwargs.get('asset_info')
        self.signals_info = kwargs.get('signals_info')
        self.start_info = kwargs.get('start_info')
        self.end_info = kwargs.get('end_info')
        self.jobname_info = kwargs.get('jobname_info')
        self.frequency_info = kwargs.get('frequency_info')
        self.result_signal_info = kwargs.get('result_signal_info')
        self.button_disabled = kwargs.get('button_disabled')
        self.error_message = kwargs.get('error_message')
        self.error_title = kwargs.get('error_title')
        self.message_type = kwargs.get('message_type')
        self.time_range_warning = kwargs.get('time_range_warning')

        self.button_on_click = button_on_click

    def vue_button_on_click(self, data=None):
        if self.button_on_click:
            self.button_on_click(data)
