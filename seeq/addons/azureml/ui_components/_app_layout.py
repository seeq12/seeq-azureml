import traitlets
import ipyvuetify as v
from pathlib import Path
from ._hamburger_menu import HamburgerMenu
from ._model_inputs import ModelInputs
from ._model_action import ModelAction
from ._model_summary import ModelSummary

CURRENT_DIR = Path(__file__).parent.resolve()


class AppLayout(v.VuetifyTemplate):
    """
    UI component - Layout of the Add-on

    Attributes
    ----------
    template_file: str
        Modifies the VueTemplate.template_file attribute with the
        seeq.addons.azureml.ui_components.templates._app_layout.vue template
    spinner_message_title: str, default ''
        Title of the message to display just before the spinner_message
    spinner_message: str, default ''
        Message to display below the progress spinner
    spinner_message_visible: bool, default True
        If True, the message below the progress spinner will be visible
    spinner_visible: bool, default False
        If True, the progress spinner will be visible
    message_status: str, default 'RUNNING'
        Keyword describing the message type which allows to display the
        spinner_message with different colors

    """

    template_file = str(CURRENT_DIR.joinpath('templates', '_app_layout.vue'))
    spinner_message_title = traitlets.Unicode(default_value='', allow_none=True).tag(sync=True)
    spinner_message = traitlets.Unicode(default_value='', allow_none=True).tag(sync=True)
    spinner_message_visible = traitlets.Bool(default_value=True).tag(sync=True)
    spinner_visible = traitlets.Bool(default_value=False).tag(sync=True)
    message_status = traitlets.Unicode(default_value='RUNNING').tag(sync=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hamburger_menu = HamburgerMenu(**kwargs)
        self.model_inputs = ModelInputs(**kwargs)
        self.model_action = ModelAction(**kwargs)
        self.model_summary = ModelSummary(**kwargs)
        self.components = {
            'hamburger-menu': self.hamburger_menu,
            'model-inputs': self.model_inputs,
            'model-action': self.model_action,
            'model-summary': self.model_summary,
        }
