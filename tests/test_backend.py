import pytest
import mock
import json
import requests
from typing import Optional
from seeq import spy
from seeq.addons import azureml
from seeq.addons.azureml import _config
from seeq.addons.azureml import backend
from . import test_common

test_worksheet_url: Optional[str] = None


# @pytest.fixture(autouse=True, scope='session')
# def setup_module():
#     _config.validate_configuration_file(test_common.TEST_CONFIG_FILE)
#     test_common.login(url=_config.get('seeq', 'seeq_url'),
#                       credentials_file=_config.get('seeq', 'credentials_file'),
#                       data_dir=_config.get('seeq', 'seeq_data_dir'))
#     wb = test_common.create_worksheet_for_tests()
#     global test_worksheet_url
#     test_worksheet_url = wb.worksheets[0].url
#
#
# @pytest.mark.system
# def test_ui_instance():
#     notebook = f'{spy.utils.get_data_lab_project_url()}/dummy.ipynb?workbookId=' \
#                f'{spy.utils.get_workbook_id_from_url(test_worksheet_url)}'
#     C = azureml.MlOperate(config_file=test_common.TEST_CONFIG_FILE, sdl_notebook_url=notebook)  # sdl_notebook_url
#     C.run()

@pytest.mark.system
def test_mock_test():
    with open("data/onlineEnpoints_response.json") as f:
        response = json.load(f)

    with mock.patch.object(backend.AmlOnlineEndpointService, '_authorize',
                           return_value="token"):
        with mock.patch.object(requests, 'get',
                               return_value=test_common.MockResponse(response, 200)):
            instance_ = backend.AmlOnlineEndpointService("tenant_id", "app_id", "app_secret", "subscription_id",
                                                         "resource_group",
                                                         "workspace_name")
            oes = instance_.list_online_endpoints()
            print(oes)
