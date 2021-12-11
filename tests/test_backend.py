import pytest
import mock
import json
import requests
import pandas as pd
from seeq import spy
from seeq.addons.azureml import backend
from seeq.addons.azureml import _config
from . import test_common


@pytest.mark.unit
def test_amlmodel_asset_paths(unit_test_config):
    with open(test_common.DATA_DIR.joinpath("aml_model_regressor6_response.json")) as f:
        response = test_common.MockResponse(json.load(f), 200)
    model = backend.AmlModel.deserialize_aml_model_response(response.json())
    assert model.name == 'regressor'
    assert model.id == 'regressor:6'
    assert model.framework == 'ScikitLearn'
    assert model.frameworkVersion == '0.24.2'
    assert model.version == 6
    assert model.input_ids == {}
    assert model.asset_path_ids == ['2407642C-0169-4ED0-A25C-321E29DC975B',
                                    'AA1E42AE-90BD-4CF7-9449-F8CC81625E8F']
    assert model.asset_input_names == {
        '2': 'Optimizer',
        '3': 'Wet Bulb',
        '4': 'Temperature',
        '1': 'Relative Humidity'
        }
    assert model.sample_rate == '2min'


@pytest.mark.unit
def test_amlmodel_signal_ids(unit_test_config):
    with open(test_common.DATA_DIR.joinpath("aml_model_regressor3_response.json")) as f:
        response = test_common.MockResponse(json.load(f), 200)
    model = backend.AmlModel.deserialize_aml_model_response(response.json())
    assert model.name == 'regressor'
    assert model.id == 'regressor:3'
    assert model.framework == 'ScikitLearn'
    assert model.frameworkVersion == '0.24.2'
    assert model.version == 3
    assert model.input_ids == {
        '2': '62E6F850-E523-408D-AD10-0C87E65F996B',
        '4': 'F8E053D1-A4D5-4671-9969-1D5D7D4F27DD',
        '1': '4E9416E8-9C75-426A-8E0A-4D07432CAC5D',
        '3': 'CD732D0B-C3BA-496F-B69E-55543944B5F1'
        }
    assert model.asset_path_ids == []
    assert model.asset_input_names == {}
    assert model.sample_rate == '2min'


@pytest.mark.unit
def test_online_deployment(unit_test_config):
    with open(test_common.DATA_DIR.joinpath("deployment_seeq-simple-demo-3.json")) as f:
        response = test_common.MockResponse(json.load(f), 200)
    deployment = backend.OnlineDeployment.deserialize_aml_deployment_response(response.json(), "Managed")[0]
    assert deployment.id == '/subscriptions/<SUBSCRIPTION_ID>/resourceGroups/<RESOURCE_GROUP>/providers/Microsoft' \
                            '.MachineLearningServices/workspaces/<WORKSPACE_NAME>/onlineEndpoints/seeq-simple-demo-3' \
                            '/deployments/indigo'
    assert deployment.name == 'indigo'
    assert deployment.modelId == '/subscriptions/<SUBSCRIPTION_ID>/resourceGroups/<RESOURCE_GROUP>/providers' \
                                 '/Microsoft.MachineLearningServices/workspaces/<WORKSPACE_NAME>/models/regressor' \
                                 '/versions/6'
    assert deployment.traffic is None
    assert deployment.model is None
    assert deployment.location == 'canadacentral'


@pytest.mark.unit
def test_online_managed_endpoint(unit_test_config):
    with open(test_common.DATA_DIR.joinpath("onlineEndpoints_response.json")) as f:
        response = test_common.MockResponse(json.load(f), 200)
    oes = backend.OnlineEndpoint.deserialize_managed_endpoint_response(response.json())
    assert isinstance(oes, list)
    assert len(oes) == 4
    for endpoint in oes:
        assert endpoint.type == 'Microsoft.MachineLearningServices/workspaces/onlineEndpoints'
        assert endpoint.name in ['seeq-simple-demo', 'seeq-simple-demo-2', 'seeq-simple-demo-3', 'jrd-test']
        assert len(endpoint.deployment) == 0


@pytest.mark.unit
def test_online_unmanaged_endpoint(unit_test_config):
    with open(test_common.DATA_DIR.joinpath("onlineEndpoints_aci_response.json")) as f:
        response = test_common.MockResponse(json.load(f), 200)
    oes = backend.OnlineEndpoint.deserialize_unmanaged_endpoint_response(response.json())
    assert isinstance(oes, list)
    assert len(oes) == 1
    endpoint = oes[0]
    assert endpoint.type == 'Microsoft.MachineLearningServices/workspaces/onlineEndpoints'
    assert endpoint.name == 'regressor-v6-svc'
    assert len(endpoint.deployment) == 1
    assert endpoint.deployment[0].name == 'regressor-v6-svc'


@pytest.mark.unit
def test_list_online_endpoints(unit_test_config):
    instance_ = backend.AmlOnlineEndpointService("tenant_id", "app_id", "app_secret", "subscription_id",
                                                 "resource_group",
                                                 "workspace_name")

    with mock.patch.object(backend.AmlOnlineEndpointService, '_authorize', return_value="token"), \
            mock.patch.object(instance_._http, 'get', side_effect=test_common.mocked_aml_response), \
            mock.patch.object(instance_._http, 'post', side_effect=test_common.mocked_aml_response):

        oes = instance_.list_online_endpoints()

    assert isinstance(oes, list)
    assert len(oes) == 5
    for endpoint in oes:
        assert endpoint.type == 'Microsoft.MachineLearningServices/workspaces/onlineEndpoints'
        assert endpoint.name in ['seeq-simple-demo', 'seeq-simple-demo-2', 'seeq-simple-demo-3', 'regressor-v6-svc',
                                 'jrd-test']
        if endpoint.name == 'jrd-test':
            assert len(endpoint.deployment) == 0
        else:
            assert len(endpoint.deployment) == 1


@pytest.mark.unit
def test_model_inputs_provider_asset_path_ids(unit_test_config):
    selected_endpoint = 'seeq-simple-demo-3'
    with mock.patch.object(backend.AmlOnlineEndpointService, '_authorize', return_value="token"), \
            mock.patch.object(backend._aml_online_endpoint_service.requests.Session, 'get',
                              side_effect=test_common.mocked_aml_response), \
            mock.patch.object(backend._aml_online_endpoint_service.requests.Session, 'post',
                              side_effect=test_common.mocked_aml_response), \
            mock.patch.object(backend._seeq_inputs_provider.TreesApi, 'get_tree',
                              side_effect=test_common.mocked_get_tree_api_response), \
            mock.patch.object(_config, 'validate_configuration_file', return_value=None):
        assert _config.get('azure', 'TENANT_ID') is None
        inputs_provider = backend.ModelInputsProvider()
        assert inputs_provider.asset_paths is None
        inputs_provider.update_assets_from_endpoint(inputs_provider.endpoints[selected_endpoint])
        assert inputs_provider.asset_paths == {
            'Example >> Cooling Tower 1 >> Area A': '2407642C-0169-4ED0-A25C-321E29DC975B',
            'Example >> Cooling Tower 1 >> Area B': 'AA1E42AE-90BD-4CF7-9449-F8CC81625E8F'
            }

        inputs_provider.update_signal_inputs_from_endpoint(inputs_provider.endpoints[selected_endpoint],
                                                           inputs_provider.asset_paths[
                                                               'Example >> Cooling Tower 1 >> Area A'])

        assert inputs_provider.model_signal_inputs == {
            'Relative Humidity': '4E9416E8-9C75-426A-8E0A-4D07432CAC5D',
            'Optimizer': '62E6F850-E523-408D-AD10-0C87E65F996B',
            'Wet Bulb': 'CD732D0B-C3BA-496F-B69E-55543944B5F1',
            'Temperature': 'F8E053D1-A4D5-4671-9969-1D5D7D4F27DD'
            }


@pytest.mark.unit
def test_model_inputs_provider_signal_ids(unit_test_config):
    with mock.patch.object(backend.AmlOnlineEndpointService, '_authorize', return_value="token"), \
            mock.patch.object(requests, 'get', side_effect=test_common.mocked_aml_response), \
            mock.patch.object(requests, 'post', side_effect=test_common.mocked_aml_response), \
            mock.patch.object(backend._seeq_inputs_provider.TreesApi, 'get_tree',
                              side_effect=test_common.mocked_get_tree_api_response), \
            mock.patch.object(backend._seeq_inputs_provider.SignalsApi, 'get_signal',
                              side_effect=test_common.mocked_get_signal_api_response), \
            mock.patch.object(_config, 'validate_configuration_file', return_value=None):
        selected_endpoint = 'seeq-simple-demo'

        assert _config.get('azure', 'TENANT_ID') is None
        inputs_provider = backend.ModelInputsProvider()
        assert inputs_provider.asset_paths is None
        inputs_provider.update_assets_from_endpoint(inputs_provider.endpoints[selected_endpoint])
        assert inputs_provider.asset_paths is None
        inputs_provider.update_signal_inputs_from_endpoint(inputs_provider.endpoints[selected_endpoint])
        assert inputs_provider.asset_path_from_signals == {
            'Example >> Cooling Tower 1 >> Area A': '2407642C-0169-4ED0-A25C-321E29DC975B'
            }

        assert inputs_provider.model_signal_inputs == {
            'Relative Humidity': '4E9416E8-9C75-426A-8E0A-4D07432CAC5D',
            'Optimizer': '62E6F850-E523-408D-AD10-0C87E65F996B',
            'Wet Bulb': 'CD732D0B-C3BA-496F-B69E-55543944B5F1',
            'Temperature': 'F8E053D1-A4D5-4671-9969-1D5D7D4F27DD'
            }


@pytest.mark.system
def test_run_investigation(system_test_config, system_test_setup):
    # This test mocks the Azure ML response but interacts with the Seeq server
    relative_humidity_id = spy.search(
        {
            "Name": "Relative Humidity",
            "Path": "Example >> Cooling Tower 1 >> Area A"
            })['ID'][0]
    optimizer_id = spy.search(
        {
            "Name": "Optimizer",
            "Path": "Example >> Cooling Tower 1 >> Area A"
            })['ID'][0]
    wet_bulb_id = spy.search(
        {
            "Name": "Wet Bulb",
            "Path": "Example >> Cooling Tower 1 >> Area A"
            })['ID'][0]
    temperature_id = spy.search(
        {
            "Name": "Temperature",
            "Path": "Example >> Cooling Tower 1 >> Area A"
            })['ID'][0]

    backend._run_investigation.urllib.request.urlopen = mock.Mock(
        spec=backend._run_investigation.urllib.request.urlopen)
    response = backend._run_investigation.urllib.request.urlopen()
    response.read.return_value = b'"{\\"Predicted_Compressor_Power\\":{\\"2021-12-06T20:14:00.000Z\\":10.2795732894,' \
                                 b'\\"2021-12-06T20:16:00.000Z\\":9.9859015583,' \
                                 b'\\"2021-12-06T20:18:00.000Z\\":10.6125521012,' \
                                 b'\\"2021-12-06T20:20:00.000Z\\":10.054556658,' \
                                 b'\\"2021-12-06T20:22:00.000Z\\":11.406334309,' \
                                 b'\\"2021-12-06T20:24:00.000Z\\":11.4476420238,' \
                                 b'\\"2021-12-06T20:26:00.000Z\\":10.8616664569,' \
                                 b'\\"2021-12-06T20:28:00.000Z\\":10.5899078439,' \
                                 b'\\"2021-12-06T20:30:00.000Z\\":11.0406563365,' \
                                 b'\\"2021-12-06T20:32:00.000Z\\":9.5797677494,' \
                                 b'\\"2021-12-06T20:34:00.000Z\\":8.5796331215,' \
                                 b'\\"2021-12-06T20:36:00.000Z\\":10.8224287375,' \
                                 b'\\"2021-12-06T20:38:00.000Z\\":12.7681512296,' \
                                 b'\\"2021-12-06T20:40:00.000Z\\":11.7027756377,' \
                                 b'\\"2021-12-06T20:42:00.000Z\\":10.8839378666,' \
                                 b'\\"2021-12-06T20:44:00.000Z\\":11.8359484297,' \
                                 b'\\"2021-12-06T20:46:00.000Z\\":14.8992703312,' \
                                 b'\\"2021-12-06T20:48:00.000Z\\":13.4492002505,' \
                                 b'\\"2021-12-06T20:50:00.000Z\\":14.5131224303,' \
                                 b'\\"2021-12-06T20:52:00.000Z\\":10.6856899759,' \
                                 b'\\"2021-12-06T20:54:00.000Z\\":10.0665961322,' \
                                 b'\\"2021-12-06T20:56:00.000Z\\":8.2384170083,' \
                                 b'\\"2021-12-06T20:58:00.000Z\\":9.6797227084,' \
                                 b'\\"2021-12-06T21:00:00.000Z\\":11.8286076236,' \
                                 b'\\"2021-12-06T21:02:00.000Z\\":11.3403269874,' \
                                 b'\\"2021-12-06T21:04:00.000Z\\":12.0153475087,' \
                                 b'\\"2021-12-06T21:06:00.000Z\\":12.519534538,' \
                                 b'\\"2021-12-06T21:08:00.000Z\\":12.3288283771,' \
                                 b'\\"2021-12-06T21:10:00.000Z\\":12.7558601744,' \
                                 b'\\"2021-12-06T21:12:00.000Z\\":11.8204852874}}"'
    investigation = backend.RunInvestigation(input_signals={
        'Relative Humidity': relative_humidity_id,
        'Optimizer': optimizer_id,
        'Wet Bulb': wet_bulb_id,
        'Temperature': temperature_id
        },
        result_name='result_signal',
        az_model_name='regressor',
        az_model_version='6',
        start=pd.Timestamp('2021-12-06 14:13:46-0600', tz='America/Chicago'),
        end=pd.Timestamp('2021-12-06 15:13:46-0600', tz='America/Chicago'),
        grid='2min',
        workbook='1EB101EE-189F-4D1F-BBAA-F6EDDE28BB99',
        worksheet='test_worksheet',
        endpoint_uri='https://<MODEL_NAME>.canadacentral.inference.ml.azure.com/score',
        aml_primary_key='<PRIMARY_KEY>',
        quiet=True)
    investigation.run()
    assert isinstance(investigation.result_signal, pd.DataFrame)
    investigation.push_to_seeq()
    assert isinstance(investigation.pushed_df, pd.DataFrame)
    assert investigation.pushed_df['Push Result'][0] == "Success"
