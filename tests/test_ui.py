import pytest
import mock
import requests
from typing import Optional
from seeq import spy
from seeq.addons import azureml
from seeq.addons.azureml import _config
from seeq.addons.azureml import backend
from . import test_common

test_worksheet_url: Optional[str] = None


@pytest.fixture(scope='session')
def system_setup():
    _config.validate_configuration_file(test_common.TEST_CONFIG_FILE)
    test_common.login(url=_config.get('seeq', 'seeq_url'),
                      credentials_file=_config.get('seeq', 'credentials_file'),
                      data_dir=_config.get('seeq', 'seeq_data_dir'))
    wb = test_common.create_worksheet_for_tests()
    global test_worksheet_url
    test_worksheet_url = wb.worksheets[0].url


@pytest.mark.system
def test_ui_instance(system_setup):
    notebook = f'{spy.utils.get_data_lab_project_url()}/dummy.ipynb?workbookId=' \
               f'{spy.utils.get_workbook_id_from_url(test_worksheet_url)}'
    C = azureml.MlOperate(config_file=test_common.TEST_CONFIG_FILE, sdl_notebook_url=notebook)  # sdl_notebook_url
    C.run()


@pytest.mark.unit
def test_user_selections():
    with mock.patch.object(backend.AmlOnlineEndpointService, '_authorize', return_value="token"), \
            mock.patch.object(requests, 'get', side_effect=test_common.mocked_response), \
            mock.patch.object(requests, 'post', side_effect=test_common.mocked_response), \
            mock.patch.object(_config, 'validate_configuration_file', return_value=None):
        if _config.get('azure', 'TENANT_ID'):
            print(_config.get('azure', 'TENANT_ID'))
            raise
        # TODO: TO REMOVE THIS IF I NEED ANOTHER FIXTURE FOR UNIT TEST
        user_selections = azureml.UserSelections()
        print('')
