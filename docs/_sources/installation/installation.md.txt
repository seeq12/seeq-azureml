# Installation

The backend of **seeq-azureml** requires **Python >3.7** or later.

## Dependencies

See [`requirements.txt`](https://github.com/seeq12/seeq-azureml/tree/master/requirements.txt) file for a list of
dependencies and versions. Additionally, you will need to install the `seeq` module with the appropriate version that
matches your Seeq server. For more information on the `seeq` module see [seeq at pypi](https://pypi.org/project/seeq/)

## User Installation Requirements (Seeq Data Lab)

If you want to install **seeq-azureml** as a Seeq Add-on Tool, you will need:

- Seeq Data Lab (> R50.5.0, >R51.1.0, or >R52.1.0)
- `seeq` module whose version matches the Seeq server version, and the version of SPy >= 182.25
- Seeq server admin access
- Enable Add-on Tools in the Seeq server

## User Installation (Seeq Data Lab)

The latest build of the project can be found [here](https://pypi.org/project/seeq-azureml/)
as a wheel file. The file is published as a courtesy and does not imply any guarantee or obligation for support from the
publisher.

1. Create a **new** Seeq Data Lab project and open the **Terminal** window
2. Run `pip install seeq-azureml`
3. Run `python -m seeq.addons.azureml [--users <users_list> --groups <groups_list>]`
4. Create an `aml_config.ini` file in the `~/.seeq` folder of the Seeq Data Lab Project with the information required to
   connect to the Azure ML services. The file must contain the options specified
   in [here](https://github.com/seeq12/seeq-azureml/tree/master/aml_config.ini)

Note: If Step 3 gives an error make sure that the seeq module is >= a.b.c.182.**25** where a.b.c are explained
[here](https://pypi.org/project/seeq/#description)

