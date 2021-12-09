import pytest
from seeq import spy
from seeq.addons import azureml
from seeq.addons.azureml import ui_components
from . import test_common


@pytest.mark.system
def test_ui_instance(system_test_config, system_test_setup):
    # This test doesn't test the rendering of the UI, just the instantiation of the UI
    notebook = f'{spy.utils.get_data_lab_project_url()}/dummy.ipynb?workbookId=' \
               f'{spy.utils.get_workbook_id_from_url(system_test_setup)}'
    C = azureml.MlOperate(config_file=test_common.TEST_CONFIG_FILE, sdl_notebook_url=notebook)  # sdl_notebook_url
    app = C.run()
    assert isinstance(app, ui_components.AppLayout)
