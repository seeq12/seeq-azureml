import ipyvuetify as v
import traitlets
from typing import Callable
from pathlib import Path

CURRENT_DIR = Path(__file__).parent.resolve()


class ScheduleInputs(v.VuetifyTemplate):
    """
    UI component - Form used for the "deploy" option with text fields for the
    result signal, the jobname, and the frequency of the deployed schedule.

    Attributes
    ----------
    template_file: str
        Modifies the VueTemplate.template_file attribute with the
        seeq.addons.azureml.ui_components.templates._schedule_inputs.vue template.
    color: str
        Primary color of the text fields for the "deploy" option in the Model
        Action card.
    frequency: str, default ''
        A Cron expression with the frequency that the scheduled job will be run.
    frequency_disabled: bool
        If True, the frequency text field is disabled. Otherwise, it is enabled.
    jobname: str, default ''
        The name of the job to be deployed.
    jobname_disabled: bool
        If True, the jobname text field is disabled. Otherwise, it is enabled.
    deploy_form_visible: bool, default True
        If True, the jobname and frequency fields are visible. Otherwise, they
        are invisible.
    deploy_form_valid: bool, default True
        If True, the form that wraps the jobname and frequency fields is marked
        as valid. Otherwise, the form is invalid.

    """
    template_file = str(CURRENT_DIR.joinpath('templates', '_schedule_inputs.vue'))
    color = traitlets.Unicode().tag(sync=True)
    frequency = traitlets.Unicode(default_value='').tag(sync=True)
    frequency_disabled = traitlets.Bool().tag(sync=True)
    jobname = traitlets.Unicode(default_value='').tag(sync=True)
    jobname_disabled = traitlets.Bool().tag(sync=True)
    deploy_form_visible = traitlets.Bool(default_value=True).tag(sync=True)
    deploy_form_valid = traitlets.Bool(default_value=True).tag(sync=True)

    def __init__(self, *args,
                 jobname_on_change: Callable[[str], None] = None,
                 frequency_on_change: Callable[[str], None] = None,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.color = self.set_default('color', 'primary', **kwargs)
        self.jobname_disabled = self.set_default('jobname_disabled', True, **kwargs)
        self.frequency_disabled = self.set_default('frequency_disabled', True, **kwargs)

        self.jobname_on_change = jobname_on_change
        self.frequency_on_change = frequency_on_change

    @staticmethod
    def set_default(arg, default, **kwargs):
        return default if kwargs.get(arg) is None else kwargs.get(arg)

    def vue_jobname_change(self, data):
        if self.jobname_on_change:
            self.jobname_on_change(data)

    def vue_frequency_change(self, data):
        if self.frequency_on_change:
            self.frequency_on_change(data)
