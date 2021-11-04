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

For additional details on the Data Scientist workflow, take a look at following video
<details open="" class="details-reset border rounded-2">
  <summary class="px-3 py-2 border-bottom">
    <svg aria-hidden="true" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-device-camera-video">
    <path fill-rule="evenodd" d="M16 3.75a.75.75 0 00-1.136-.643L11 5.425V4.75A1.75 1.75 0 009.25 3h-7.5A1.75 1.75 0 000 4.75v6.5C0 12.216.784 13 1.75 13h7.5A1.75 1.75 0 0011 11.25v-.675l3.864 2.318A.75.75 0 0016 12.25v-8.5zm-5 5.075l3.5 2.1v-5.85l-3.5 2.1v1.65zM9.5 6.75v-2a.25.25 0 00-.25-.25h-7.5a.25.25 0 00-.25.25v6.5c0 .138.112.25.25.25h7.5a.25.25 0 00.25-.25v-4.5z"></path>
    </svg>
    <span aria-label="Video description Seeq_Data_Scientist_Rev_1.mp4" class="m-1">Data Scientist Workflow</span>
    <span class="dropdown-caret"></span>
  </summary>

<video src="https://user-images.githubusercontent.com/28580105/140426302-8135c859-f3af-4bc0-a8b1-486a786f5b3b.mp4"
poster="https://seeq12.github.io/seeq-azureml/_static/ds_workflow_poster.png"
controls="controls" muted="muted" class="d-block rounded-bottom-2 width-fit" style="max-width:700px;
background:transparent url('https://seeq12.github.io/seeq-azureml/_static/ds_workflow_poster.png') no-repeat 0 0;
-webkit-background-size:cover; -moz-background-size:cover; -o-background-size:cover; background-size:cover;"
webboost_found_paused="true" webboost_processed="true">
</video>
</details>

For additional details on the Engineering workflow, take a look at the following video
<details open="" class="details-reset border rounded-2">
  <summary class="px-3 py-2 border-bottom">
    <svg aria-hidden="true" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-device-camera-video">
    <path fill-rule="evenodd" d="M16 3.75a.75.75 0 00-1.136-.643L11 5.425V4.75A1.75 1.75 0 009.25 3h-7.5A1.75 1.75 0 000 4.75v6.5C0 12.216.784 13 1.75 13h7.5A1.75 1.75 0 0011 11.25v-.675l3.864 2.318A.75.75 0 0016 12.25v-8.5zm-5 5.075l3.5 2.1v-5.85l-3.5 2.1v1.65zM9.5 6.75v-2a.25.25 0 00-.25-.25h-7.5a.25.25 0 00-.25.25v6.5c0 .138.112.25.25.25h7.5a.25.25 0 00.25-.25v-4.5z"></path>
    </svg>
    <span aria-label="Video description Seeq_Data_Scientist_Rev_1.mp4" class="m-1">Engineering Workflow</span>
    <span class="dropdown-caret"></span>
  </summary>

<video src="https://user-images.githubusercontent.com/28580105/140426286-1df1aa16-3782-4f22-9f26-ebd06a51e854.mp4"
poster="https://seeq12.github.io/seeq-azureml/_static/sme_workflow.png"
controls="controls" muted="muted" class="d-block rounded-bottom-2 width-fit" style="max-width:670px;
background:transparent url('https://seeq12.github.io/seeq-azureml/_static/sme_workflow.png') no-repeat 0 0;
-webkit-background-size:cover; -moz-background-size:cover; -o-background-size:cover; background-size:cover;"
webboost_found_paused="true" webboost_processed="true">
</video>
</details>

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
3. Run `python -m seeq.addons.azureml [--users <users_list> --groups<groups_list>]`
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

----








