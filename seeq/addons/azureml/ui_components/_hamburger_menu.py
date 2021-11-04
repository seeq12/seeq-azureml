import ipyvuetify as v
from pathlib import Path

CURRENT_DIR = Path(__file__).parent.resolve()


class HamburgerMenu(v.VuetifyTemplate):
    """
    UI component - Hamburger menu of Add-on

    Attributes
    ----------
    template_file: str
        Modifies the VueTemplate.template_file attribute with the
        seeq.addons.azureml.ui_components.templates._hamburger_menu.vue template

    """

    template_file = str(CURRENT_DIR.joinpath('templates',  '_hamburger_menu.vue'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
