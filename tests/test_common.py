import json
from pathlib import Path
from functools import partial

import seeq.sdk
from seeq.spy.workbooks import Analysis
from seeq import spy

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.joinpath('data')
TEST_CONFIG_FILE = BASE_DIR.joinpath('test_config.ini')


def login(url=None, credentials_file=None, data_dir=None):
    if not credentials_file:
        credentials_file = get_server_data_folder(data_dir=data_dir).joinpath('keys', 'agent.key')
    if isinstance(credentials_file, str):
        credentials_file = Path(credentials_file)
    if not credentials_file.is_file():
        raise ValueError(f'Could not find file {credentials_file} to get login credentials'
                         f'You can try passing the Seeq data directory as a "data_dir" kwarg')
    credentials = open(credentials_file, "r").read().splitlines()
    spy.login(credentials[0], credentials[1], url=url)


def get_server_data_folder(data_dir=None):
    if data_dir is not None:
        return data_dir
    cwd = Path().absolute()
    return Path(cwd.drive).joinpath('/ProgramData', 'Seeq', 'data')


def create_worksheet_for_tests():
    workbook = Analysis({
        'Name': 'tests_azureml_project'
        })

    worksheet = workbook.worksheet('azureml tests worksheet')
    worksheet.display_range = {
        'Start': '2019-01-01T00:00Z',
        'End': '2019-01-02T00:00Z'
        }
    spy.workbooks.push(workbook)

    return workbook


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


def mock_200_response_from_file(data_dir: Path, file: str):
    with open(data_dir.joinpath(file)) as f:
        return MockResponse(json.load(f), 200)


def mocked_aml_response(url: str, headers: str):
    """
    This is function to mock the responses from the Azure ML API calls.

    Parameters
    ----------
    url: str
        The URL of the management service
    headers: str
        The headers of the management service. See note below.

    Returns
    -------
    response: MockResponse
        The mocked response of the Azure ML API call.


    Note
    ----
    The parameter `headers` is not used within this function but it is needed in
    the signature of the function, since that's the signature of the actual
    functions we are mocking. Those are `requests.get(url, headers)` and
    `request.post(url, headers)` in `AmlOnlineEndpointService`

    """

    mock_200_from_file = partial(mock_200_response_from_file, DATA_DIR)

    if url.endswith("onlineEndpoints?api-version=2021-03-01-preview"):
        return mock_200_from_file("onlineEndpoints_response.json")
    elif url.endswith("listKeys?api-version=2021-03-01-preview"):
        return MockResponse({"primaryKey": "p-key", "secondaryKey": "s-key"}, 200)
    elif '/seeq-simple-demo/' in url:
        return mock_200_from_file("deployment_seeq-simple-demo.json")
    elif '/seeq-simple-demo-2/' in url:
        return mock_200_from_file("deployment_seeq-simple-demo-2.json")
    elif '/seeq-simple-demo-3/' in url:
        return mock_200_from_file("deployment_seeq-simple-demo-3.json")
    elif url.endswith("/regressor:6"):
        return mock_200_from_file("aml_model_regressor6_response.json")
    elif url.endswith("/regressor:3"):
        return mock_200_from_file("aml_model_regressor3_response.json")
    elif url.endswith("/regressor:2"):
        return mock_200_from_file("aml_model_regressor2_response.json")
    else:
        return mock_200_from_file("deployment_null.json")


def mocked_get_tree_api_response(id):
    with open(DATA_DIR.joinpath("seeq_asset_trees_seeq-simple-demo-3.json")) as f:
        trees = json.load(f)
    for tree in trees['trees']:
        if tree['id'] == id:
            tree['value']['children'] = [seeq.sdk.models.TreeItemOutputV1(**x) for x in
                                         tree['value']['children']]
            tree['value']['item']['ancestors'] = [seeq.sdk.models.ItemPreviewV1(**x) for x in
                                                  tree['value']['item']['ancestors']]
            tree['value']['item'] = seeq.sdk.models.ItemPreviewWithAssetsV1(**tree['value']['item'])
            return seeq.sdk.models.asset_tree_output_v1.AssetTreeOutputV1(**tree['value'])


def mocked_get_signal_api_response(id):
    with open(DATA_DIR.joinpath("seeq_signals_seeq-simple-demo-3.json")) as f:
        signals = json.load(f)
    for signal in signals['signals']:
        if signal['id'] == id:
            return seeq.sdk.models.signal_output_v1.SignalOutputV1(**signal)
