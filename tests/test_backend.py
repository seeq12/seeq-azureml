import pytest
import mock
import json
import requests
from typing import Optional
from seeq.addons.azureml import backend
from . import test_common

test_worksheet_url: Optional[str] = None


@pytest.mark.unit
def test_amlmodel_asset_paths():
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
def test_amlmodel_signal_ids():
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
def test_online_deployment():
    with open(test_common.DATA_DIR.joinpath("deployment_seeq-simple-demo-3.json")) as f:
        response = test_common.MockResponse(json.load(f), 200)
    deployment = backend.OnlineDeployment.deserialize_aml_deployment_response(response.json())[0]
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
def test_online_endpoint():
    with open(test_common.DATA_DIR.joinpath("onlineEndpoints_response.json")) as f:
        response = test_common.MockResponse(json.load(f), 200)
    oes = backend.OnlineEndpoint.deserialize_aml_endpoint_response(response.json())
    assert isinstance(oes, list)
    assert len(oes) == 4
    for endpoint in oes:
        assert endpoint.type == 'Microsoft.MachineLearningServices/workspaces/onlineEndpoints'
        assert endpoint.name in ['seeq-simple-demo', 'seeq-simple-demo-2', 'seeq-simple-demo-3', 'jrd-test']
        assert len(endpoint.deployment) == 0


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
