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


@pytest.mark.unit
def test_list_online_endpoints():
    with mock.patch.object(backend.AmlOnlineEndpointService, '_authorize', return_value="token"), \
            mock.patch.object(requests, 'get', side_effect=test_common.mocked_response), \
            mock.patch.object(requests, 'post', side_effect=test_common.mocked_response):
        instance_ = backend.AmlOnlineEndpointService("tenant_id", "app_id", "app_secret", "subscription_id",
                                                     "resource_group",
                                                     "workspace_name")
        oes = instance_.list_online_endpoints()

    assert isinstance(oes, list)
    assert len(oes) == 4
    for endpoint in oes:
        assert endpoint.type == 'Microsoft.MachineLearningServices/workspaces/onlineEndpoints'
        assert endpoint.name in ['seeq-simple-demo', 'seeq-simple-demo-2', 'seeq-simple-demo-3', 'jrd-test']
        if endpoint.name == 'jrd-test':
            assert len(endpoint.deployment) == 0
        else:
            assert len(endpoint.deployment) == 1
