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
