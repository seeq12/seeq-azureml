import ipywidgets as widgets
import ipyvuetify as v
import ipydatetime
import traitlets
from typing import Callable
from pathlib import Path

CURRENT_DIR = Path(__file__).parent.resolve()


class InvestigateRange(v.VuetifyTemplate):
    """
    UI component - DatetimePicker for the start and end times of the
    investigation range

    Attributes
    ----------
    template_file: str
        Modifies the VueTemplate.template_file attribute with the
        seeq.addons.azureml.ui_components.templates._investigate_range.vue template
    start_range: ipydatetime.DatetimePicker
        DatetimePicker widget for the start time of the investigation range
    end_range: ipydatetime.DatetimePicker
        DatetimePicker widget for the end time of the investigation range
    investigation_range_visible: bool, default True
        If True, the two DatetimePicker for the start and end times of the
        investigation range will be visible

    """

    template_file = str(CURRENT_DIR.joinpath('templates', '_investigate_range.vue'))
    start_range = traitlets.Any().tag(sync=True, **widgets.widget_serialization)
    end_range = traitlets.Any().tag(sync=True, **widgets.widget_serialization)
    investigation_range_visible = traitlets.Bool(default_value=True).tag(sync=True)

    def __init__(self, *args,
                 start_on_change: Callable[[], None] = None,
                 end_on_change: Callable[[], None] = None,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.start_range = ipydatetime.DatetimePicker()
        self.end_range = ipydatetime.DatetimePicker()
        self.start_range.disabled = self.set_default('start_range_disabled', True, **kwargs)
        self.end_range.disabled = self.set_default('end_range_disabled', True, **kwargs)
        self.start_on_change = start_on_change
        self.end_on_change = end_on_change

        if start_on_change:
            self.start_range.observe(self.start_on_change, names='value')
        if end_on_change:
            self.end_range.observe(self.end_on_change, names='value')

    @staticmethod
    def set_default(arg, default, **kwargs):
        return default if kwargs.get(arg) is None else kwargs.get(arg)

