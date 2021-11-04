import ipyvuetify as v
import traitlets
from typing import Callable
from pathlib import Path
from ._schedule_inputs import ScheduleInputs
from ._investigate_range import InvestigateRange

CURRENT_DIR = Path(__file__).parent.resolve()


class ModelAction(v.VuetifyTemplate):
    """
    UI component - Model Action card with action dropdown, investigation range
    component and schedule component

    Attributes
    ----------
    template_file: str
        Modifies the VueTemplate.template_file attribute with the
        seeq.addons.azureml.ui_components.templates._model_action.vue template.
    components: str, default {}
        Modifies the VueTemplate.components attribute with a serialized
        instance of seeq.addons.ui_components.InvestigateRange and
        seeq.addons.ui_components.ScheduleInputs.
    model_action_visible: bool, default True
        If True, the entire Model Action card will be visible. If false,
        the entire Model Action card will not be visible.
    color: str
        Color of the dropdowns and text fields in the Model Action card.
    selection: {'Investigate', 'Deploy'}, default 'Investigate'
        Options of the action dropdown. If 'Investigate', the Model Action
        card will show the InvestigateRange component. If 'Deploy', the Model
        Action card will show the 'ScheduleInputs' component.
    action_disabled: bool, default True
        If True, the action dropdown is disabled. Otherwise, it is enabled.
    result_name: str, default ''
        The name of the result signal that will be pushed to Seeq.
    result_name_disabled: bool
        If True, the result_name field is disabled. Otherwise, it is enabled.
    investigation_form_valid: bool, default True
        If False, the result_name field will show an error message to hint the
        user. Otherwise, the field gets the default color and no error message.

    """

    template_file = str(CURRENT_DIR.joinpath('templates', '_model_action.vue'))
    components = traitlets.Dict(default_value={}).tag(sync=True, **v.VuetifyTemplate.class_component_serialization)
    model_action_visible = traitlets.Bool(default_value=True).tag(sync=True)
    color = traitlets.Unicode().tag(sync=True)
    selection = traitlets.Unicode(allow_none=True, default_value='Investigate').tag(sync=True)
    action_disabled = traitlets.Bool(default_value=True).tag(sync=True)
    result_name = traitlets.Unicode(default_value='').tag(sync=True)
    result_name_disabled = traitlets.Bool().tag(sync=True)
    investigation_form_valid = traitlets.Bool(default_value=True).tag(sync=True)

    def __init__(self, *args,
                 action_on_change: Callable[[str], None] = None,
                 result_name_on_change: Callable[[str], None] = None,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.color = self.set_default('color', 'primary', **kwargs)
        self.action_disabled = self.set_default('action_disabled', True, **kwargs)
        self.result_name_disabled = self.set_default('result_name_disabled', True, **kwargs)

        self.action_on_change = action_on_change
        self.result_name_on_change = result_name_on_change

        self.deploy_input_form = ScheduleInputs(deploy_form_visible=False, **kwargs)
        self.investigate_range = InvestigateRange(**kwargs)

        self.components = {
            'investigate_widget': self.investigate_range,
            'deploy_widget': self.deploy_input_form
        }

    @staticmethod
    def set_default(arg, default, **kwargs):
        return default if kwargs.get(arg) is None else kwargs.get(arg)

    def vue_action_change(self, data):
        self.investigate_range.investigation_range_visible = True if data == 'Investigate' else False
        self.deploy_input_form.deploy_form_visible = True if data == 'Deploy' else False
        if self.action_on_change is not None:
            self.action_on_change(data)

    def vue_result_name_change(self, data):
        if self.result_name_on_change:
            self.result_name_on_change(data)
