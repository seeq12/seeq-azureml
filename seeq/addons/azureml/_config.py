import configparser
from pathlib import Path
from typing import Optional

DEFAULT_PATH = Path.home().joinpath('.seeq', 'aml_config.ini')
configuration_parser: Optional[configparser.ConfigParser] = None


def validate_configuration_file(configfile=None):
    """
    Reads a configuration file and sets the global variable configuration_parser

    Parameters
    ----------
    configfile: str or Path
        Full path to the configuration file. If None, the parser will to read
        the file ~/.seeq.aml_config.ini provided it exists.

    Returns
    -------
    -: None

    """
    if configfile is None:
        configfile = DEFAULT_PATH
    if not Path(configfile).exists():
        raise FileNotFoundError(f"File {configfile} could not be found.")
    config = configparser.ConfigParser(allow_no_value=True)
    config.read(configfile)
    global configuration_parser
    configuration_parser = config


def get(section: str, variable: str, fallback=None):
    """
    Retrieves the value of named option from the configuration_parser. If the
    configuration_parser is not set, a fallback value can be returned.

    Parameters
    ----------
    section: str
        Name of the section in the configuration file to retrieve the value from.
    variable: str
        Name of the option whose value will be retrieved.
    fallback: object
        Object to be retrieved if configuration_parser is not set.

    Returns
    -------
    value: str
        A string value for the named option.

    """
    if not configuration_parser:
        return fallback
    return configuration_parser.get(section, variable, fallback=fallback)
