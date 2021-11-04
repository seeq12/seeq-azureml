import ipyvuetify as v
import traitlets
from typing import Callable
from pathlib import Path

CURRENT_DIR = Path(__file__).parent.resolve()


class ModelInputs(v.VuetifyTemplate):
    """
    UI component - Model Inputs card with endpoints and assets dropdowns

    Attributes
    ----------
    template_file: str
        Modifies the VueTemplate.template_file attribute with the
        seeq.addons.azureml.ui_components.templates._model_inputs.vue template.
    model_inputs_visible: bool, default True
        If True, the entire Model Inputs card will be visible. Otherwise,
        the entire Model Inputs card will not be visible.
    endpoint_disabled: bool
        If True, the endpoints dropdown is disabled. Otherwise, it is enabled.
    endpoint_color: str
        Primary color of the endpoints dropdown.
    endpoint_items: list, default []
        List of items of the endpoints dropdown.
    endpoint_selection: str
        Selected value of the endpoints dropdown.
    endpoint_loading: bool
        If True, the endpoints dropdown will show a progress loading bar.
        Otherwise, the progress loading bar is invisible.
    asset_color: str
        Primary color of the assets dropdown.
    asset_items: list, default []
        List of items of the assets dropdown.
    asset_selection: str
        Selected value of the assets dropdown.
    asset_visible: bool
        If True, the assets dropdown is visible. Otherwise, it is invisible.
    asset_disabled: bool
        If True, the assets dropdown is disabled. Otherwise, it is enabled.

    """

    template_file = str(CURRENT_DIR.joinpath('templates', '_model_inputs.vue'))
    model_inputs_visible = traitlets.Bool(default_value=True).tag(sync=True)
    endpoint_disabled = traitlets.Bool().tag(sync=True)
    endpoint_color = traitlets.Unicode().tag(sync=True)
    endpoint_items = traitlets.List(default_value=[]).tag(sync=True)
    endpoint_selection = traitlets.Unicode(allow_none=True).tag(sync=True)
    endpoint_loading = traitlets.Bool().tag(sync=True)
    asset_color = traitlets.Unicode().tag(sync=True)
    asset_items = traitlets.List(default_value=[]).tag(sync=True)
    asset_selection = traitlets.Unicode(allow_none=True).tag(sync=True)
    asset_visible = traitlets.Bool(allow_none=True).tag(sync=True)
    asset_disabled = traitlets.Bool().tag(sync=True)

    def __init__(self, *args,
                 endpoint_on_change: Callable[[str], None] = None,
                 asset_on_change: Callable[[str], None] = None,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.endpoint_disabled = self.set_default('endpoint_disabled', True, **kwargs)
        self.endpoint_color = self.set_default('endpoint_color', 'primary', **kwargs)
        self.endpoint_selection = self.set_default('endpoint_selection', None, **kwargs)
        self.endpoint_loading = self.set_default('endpoint_loading', False, **kwargs)

        self.asset_disabled = self.set_default('asset_disabled', True, **kwargs)
        self.asset_visible = self.set_default('asset_visible', True, **kwargs)
        self.asset_color = self.set_default('asset_color', 'primary', **kwargs)
        self.asset_selection = self.set_default('asset_selection', None, **kwargs)

        self.endpoint_on_change = endpoint_on_change
        self.asset_on_change = asset_on_change

    @staticmethod
    def set_default(arg, default, **kwargs):
        return default if kwargs.get(arg) is None else kwargs.get(arg)

    def vue_endpoint_on_change(self, data=None):
        self.endpoint_on_change(data)

    def vue_asset_on_change(self, data=None):
        self.asset_on_change(data)
