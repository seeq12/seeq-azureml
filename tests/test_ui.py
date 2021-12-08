import pytest
import mock
import requests
from typing import Optional
from seeq import spy
from seeq.addons import azureml
from seeq.addons.azureml import _config
from seeq.addons.azureml import ui_components
from . import test_common

test_worksheet_url: Optional[str] = None


@pytest.fixture()
def system_test_config():
    # This fixture is needed if we add unit test to this file
    _config.validate_configuration_file(test_common.TEST_CONFIG_FILE)


@pytest.fixture(scope='session')
def system_test_setup():
    # This fixture is needed if we add unit test to this file
    _config.validate_configuration_file(test_common.TEST_CONFIG_FILE)
    test_common.login(url=_config.get('seeq', 'seeq_url'),
                      credentials_file=_config.get('seeq', 'credentials_file'),
                      data_dir=_config.get('seeq', 'seeq_data_dir'))
    wb = test_common.create_worksheet_for_tests()
    global test_worksheet_url
    test_worksheet_url = wb.worksheets[0].url


@pytest.mark.system
def test_ui_instance(system_test_config, system_test_setup):
    # This test doesn't test the rendering of the UI, just the instantiation of the UI
    notebook = f'{spy.utils.get_data_lab_project_url()}/dummy.ipynb?workbookId=' \
               f'{spy.utils.get_workbook_id_from_url(test_worksheet_url)}'
    C = azureml.MlOperate(config_file=test_common.TEST_CONFIG_FILE, sdl_notebook_url=notebook)  # sdl_notebook_url
    app = C.run()
    assert isinstance(app, ui_components.AppLayout)
