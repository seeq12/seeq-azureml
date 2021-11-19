<p align="center">
  <a href="https://www.seeq.com" rel="nofollow">
    <img src="https://seeq12.github.io/seeq-azureml/_static/logos_handshake.png" alt="N|Scheme" width="80%">
  </a>
</p>


<p align="center">
  <a href="https://seeq12.github.io/seeq-azureml/index.html" rel="nofollow">
    <img src="https://seeq12.github.io/seeq-azureml/_static/UI_complete_investigate.png" alt="N|Scheme" width="500">
  </a>
</p>

----

# Introduction

**seeq-azureml** provides an example framework that allows a data scientist working in Azure ML Studio and a plant
engineer or subject matter expert (SME) working in Seeq to collaborate and develop an effective, sustainable solution
for high value problems in manufacturing.

This python module integrates with Microsoft Azure Machine Learning (AML) models as a web service and can be installed
as a Seeq Add-on in Seeq Workbench. The plant engineer and/or SME interacts with the module through an easy to use UI
from which they can accomplish critical activities such as ad hoc/historical evaluations, model deployment in real time,
scaling to other assets, etc.

The Seeq Add-on is distributed as an example of a collaborative workflow between data scientists (model builders) and
plant engineers/SMEs (model consumers). Users are encouraged to fork the repo and make the necessary
modifications/enhancements that addresses the specific needs/workflows of their organization.

[![N|Scheme](https://seeq12.github.io/seeq-azureml/_static/workflow_collabo.png)](https://seeq12.github.io/seeq-azureml/introduction/introduction.html)


----

# Documentation

The documentation for **seeq-azureml** can be found [here](https://seeq12.github.io/seeq-azureml/index.html).

----

# User Guide

[**seeq-azureml** User Guide](https://seeq12.github.io/seeq-azureml/user_guide/user_guide.html) provides a more in-depth
explanation of how this Seeq Add-on enables engineers and SMEs in OT to directly interface with models built by data
science teams in Azure ML Studio and that have been registered and deployed in an AML endpoint as a cloud service.

For additional details on the Data Scientist workflow, take a look at 
[**this video**](https://user-images.githubusercontent.com/28580105/140426302-8135c859-f3af-4bc0-a8b1-486a786f5b3b.mp4).

For additional details on the Engineering workflow, take a look at
[**this video**](https://user-images.githubusercontent.com/28580105/140426286-1df1aa16-3782-4f22-9f26-ebd06a51e854.mp4).

----

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

----

# Development

We welcome new contributors of all experience levels.

## Important links

* Official source code repo: https://github.com/seeq12/seeq-azureml
* Issue tracker: https://github.com/seeq12/seeq-azureml/issues

## Source code

You can get started by cloning the repository with the command:

```shell
git clone git@github.com:seeq12/seeq-azureml.git
```

## Installation from source

For development work, it is highly recommended creating a python virtual environment and install the package in that
working environment. If you are not familiar with python virtual environments, you can take a
look [here](https://docs.python.org/3.8/tutorial/venv.html)

Once your virtual environment is activated, you can install **seeq-azureml** from source with:

```shell
python setup.py install
```

----

# Changelog

The changelog can be found [**here**](https://seeq12.github.io/seeq-azureml/changelog/changelog.html)

----

# Support

Code related issues (e.g. bugs, feature requests) can be created in the
[issue tracker](https://github.com/seeq12/seeq-azureml/issues)

Maintainer: Seeq

----

# Citation

Please cite this work as:

```shell
seeq-azureml
Seeq Corporation, 2021
https://github.com/seeq12/seeq-azureml
```








