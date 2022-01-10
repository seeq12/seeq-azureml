# Installation

The backend of **seeq-azureml** requires **Python >3.7** or later.

## Dependencies

See [`requirements.txt`](https://github.com/seeq12/seeq-azureml/tree/master/requirements.txt) file for a list of
dependencies and versions. Additionally, you will need to install the `seeq` module with the appropriate version that
matches your Seeq server. For more information on the `seeq` module see [seeq at pypi](https://pypi.org/project/seeq/)

## User Installation Requirements (Seeq Data Lab)

If you want to install **seeq-azureml** as a Seeq Add-on Tool, you will need:

- Seeq Data Lab (> R50.5.0, >R51.1.0, >R52.1.0, or >=R53)
- `seeq` module whose version matches the Seeq server version, and the version of SPy >= 182.25
- Seeq server admin access
- Enable Add-on Tools in the Seeq server

## User Installation (Seeq Data Lab)

The latest build of the project can be found [here](https://pypi.org/project/seeq-azureml/)
as a wheel file. The file is published as a courtesy and does not imply any guarantee or obligation for support from the
publisher.

### Pre-requisites

Before installing the **seeq-azureml** Seeq Add-on, you will have to create an **Azure application** and **service
principal**. Follow the steps
in [here](https://docs.microsoft.com/en-us/azure/active-directory/develop/howto-create-service-principal-portal) to
create your application, and
choose [Option 2](https://docs.microsoft.com/en-us/azure/active-directory/develop/howto-create-service-principal-portal#option-2-create-a-new-application-secret)
for the `Authentication` method.

### Seeq Add-on Installation

Once the **Azure application** and **service principal** have been created. Follow these steps to install the Seeq
Add-on:

1. Create a **new** Seeq Data Lab project and open the **Terminal** window
2. Run `pip install seeq-azureml`
3. Run `python -m seeq.addons.azureml [--users <users_list> --groups <groups_list>]`
4. Create an `aml_config.ini` file in the `~/.seeq` folder of the Seeq Data Lab Project with the information required to
   connect to the Azure ML services. The following steps summarized how to create the `aml_config.ini` file in the
   correct Seeq Data Lab location and where to get the values required for the configuration.
    1. Download the `aml_config.ini` configuration file
       from [here](https://github.com/seeq12/seeq-azureml/tree/master/aml_config.ini)
    2. Upload the file to the Seeq Data Lab project using the `Upload` button located in the top-right corner of the
       home page of the project.
    3. From the Seeq Data Lab project home page, open the uploaded file and modify the fields appropriately:
        1. The `SUBSCRIPTION_ID`, `RESOURCE_GROUP`, and `WORKSPACE_NAME` can be obtained by logging into the Azure
           portal and clicking on
           the [Machine Learning service](https://portal.azure.com/#blade/HubsExtension/BrowseResource/resourceType/Microsoft.MachineLearningServices%2Fworkspaces)
           . Once in the Machine Learning service, click on the desired `WORKSPACE_NAME` from the list. The `Overview`
           tab will show a list of `Essentials` from which you can take the values for `SUBSCRIPTION_ID`
           and `RESOURCE_GROUP`.
        2. The `TENANT_ID`, `APP_ID`, and `APP_SECRET` are obtained when creating the Azure application in the
           section [Get tenant and app ID values for signing in](https://docs.microsoft.com/en-us/azure/active-directory/develop/howto-create-service-principal-portal#get-tenant-and-app-id-values-for-signing-in)
           , [Option 2](https://docs.microsoft.com/en-us/azure/active-directory/develop/howto-create-service-principal-portal#option-2-create-a-new-application-secret)
           .
        3. Save the `aml_config.ini` file.
    4. Back to the **Terminal** window from Steps 1 and 2, run the command `mv aml_config.ini .seeq/` to move
       the `aml_config.ini` file to the appropriate folder.

Note: If Step 3 gives an error make sure that the seeq module is >= a.b.c.182.**25** where a.b.c are explained
[here](https://pypi.org/project/seeq/#description)

