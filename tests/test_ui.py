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


@pytest.fixture()
def unit_test_config():
    _config.configuration_parser = None


@pytest.fixture()
def system_test_config():
    _config.validate_configuration_file(test_common.TEST_CONFIG_FILE)


@pytest.fixture(scope='session')
def system_test_setup():
    _config.validate_configuration_file(test_common.TEST_CONFIG_FILE)
    test_common.login(url=_config.get('seeq', 'seeq_url'),
                      credentials_file=_config.get('seeq', 'credentials_file'),
                      data_dir=_config.get('seeq', 'seeq_data_dir'))
    wb = test_common.create_worksheet_for_tests()
    global test_worksheet_url
    test_worksheet_url = wb.worksheets[0].url


@pytest.mark.unit
def test_user_selections_asset_path_ids(unit_test_config, system_test_setup):
    with mock.patch.object(backend.AmlOnlineEndpointService, '_authorize', return_value="token"), \
            mock.patch.object(requests, 'get', side_effect=test_common.mocked_aml_response), \
            mock.patch.object(requests, 'post', side_effect=test_common.mocked_aml_response), \
            mock.patch.object(_config, 'validate_configuration_file', return_value=None):
        selected_endpoint = 'seeq-simple-demo-3'

        assert _config.get('azure', 'TENANT_ID') is None
        user_selections = azureml.UserSelections()
        assert user_selections.asset_paths is None
        user_selections.get_assets(user_selections.endpoints[selected_endpoint])
        assert user_selections.asset_paths == {
            'Example >> Cooling Tower 1 >> Area A': '2407642C-0169-4ED0-A25C-321E29DC975B',
            'Example >> Cooling Tower 1 >> Area B': 'AA1E42AE-90BD-4CF7-9449-F8CC81625E8F'
            }

        user_selections.get_signal_inputs(
            user_selections.endpoints[selected_endpoint],
            user_selections.asset_paths['Example >> Cooling Tower 1 >> Area A'])

        assert user_selections.model_signal_inputs == {
            'Relative Humidity': '4E9416E8-9C75-426A-8E0A-4D07432CAC5D',
            'Optimizer': '62E6F850-E523-408D-AD10-0C87E65F996B',
            'Wet Bulb': 'CD732D0B-C3BA-496F-B69E-55543944B5F1',
            'Temperature': 'F8E053D1-A4D5-4671-9969-1D5D7D4F27DD'
            }


@pytest.mark.system
def test_ui_instance(system_test_config, system_test_setup):
    notebook = f'{spy.utils.get_data_lab_project_url()}/dummy.ipynb?workbookId=' \
               f'{spy.utils.get_workbook_id_from_url(test_worksheet_url)}'
    C = azureml.MlOperate(config_file=test_common.TEST_CONFIG_FILE, sdl_notebook_url=notebook)  # sdl_notebook_url
    C.run()
