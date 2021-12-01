import json
from pathlib import Path
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


def mocked_response(url: str, headers: str):
    base_url = 'https://management.azure.com/subscriptions/subscription_id/resourceGroups/resource_group/providers' \
               '/Microsoft.MachineLearningServices/workspaces/workspace_name/'

    if url.endswith("onlineEndpoints?api-version=2021-03-01-preview"):
        with open("data/onlineEnpoints_response.json") as f:
            return MockResponse(json.load(f), 200)
    elif url.endswith("listKeys?api-version=2021-03-01-preview"):
        return MockResponse({"primaryKey": "p-key", "secondaryKey": "s-key"}, 200)
    elif '/seeq-simple-demo/' in url:
        with open("data/deployment_seeq-simple-demo.json") as f:
            return MockResponse(json.load(f), 200)
    elif '/seeq-simple-demo-2/' in url:
        with open("data/deployment_seeq-simple-demo-2.json") as f:
            return MockResponse(json.load(f), 200)
    elif '/seeq-simple-demo-3/' in url:
        with open("data/deployment_seeq-simple-demo-3.json") as f:
            return MockResponse(json.load(f), 200)
    elif url.endswith("/regressor:6"):
        with open("data/aml_model_regressor6_response.json") as f:
            return MockResponse(json.load(f), 200)
    elif url.endswith("/regressor:3"):
        with open("data/aml_model_regressor3_response.json") as f:
            return MockResponse(json.load(f), 200)
    elif url.endswith("/regressor:2"):
        with open("data/aml_model_regressor2_response.json") as f:
            return MockResponse(json.load(f), 200)
    else:
        with open("data/deployment_null.json") as f:
            return MockResponse(json.load(f), 200)
