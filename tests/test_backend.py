import pytest
from typing import Optional
from seeq import spy
from seeq.addons import azureml
from seeq.addons.azureml import _config
from . import test_common

test_worksheet_url: Optional[str] = None


@pytest.fixture(autouse=True, scope='session')
def setup_module():
    _config.validate_configuration_file(test_common.TEST_CONFIG_FILE)
    test_common.login(url=_config.get('seeq', 'seeq_url'),
                      credentials_file=_config.get('seeq', 'credentials_file'),
                      data_dir=_config.get('seeq', 'seeq_data_dir'))
    wb = test_common.create_worksheet_for_tests()
    global test_worksheet_url
    test_worksheet_url = wb.worksheets[0].url


@pytest.mark.system
def test_ui_instance():
    notebook = f'{spy.utils.get_data_lab_project_url()}/dummy.ipynb?workbookId=' \
               f'{spy.utils.get_workbook_id_from_url(test_worksheet_url)}'
    C = azureml.MlOperate(config_file=test_common.TEST_CONFIG_FILE, sdl_notebook_url=notebook)  # sdl_notebook_url
    C.run()

# with mock.patch.object(_login, 'get_server_version_tuple', return_value=(53, 0, 1)):
#     with pytest.raises(SPyException, match=ERROR_53):
#         _addons_common.verify_addons_support()
