import pytest
from seeq.addons.azureml import _config
from . import test_common


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
    test_worksheet_url = wb.worksheets[0].url
    return test_worksheet_url
