<div><strong>This add-on has been deprecated</strong></div>
<hr style="width:100%", size="2", color=black>

# User Guide

Many data scientists are comfortable with Azure ML Studio for machine learning operations and model lifecycle
management, but are relatively unfamiliar with manufacturing-specific data and context. Plant and central group
engineers in the operational technology (OT) domain lack expertise in ML and are not typically exposed to
state-of-the-art solutions like Azure ML Studio. While there has historically been a disconnect between these two
groups (IT and OT), a successful ML project requires the active participation and collaboration between both sides - the
data scientists in IT and the plant & central group engineers in OT.

<br>
<table border="0" align="center">
 <tr>
    <td align="center"><img alt="image" src="../_static/workflow_collabo.png"></td>
 </tr>
 <tr>
    <td align="center">Figure 1 - Collaborative Workflow between Data Scientists & Plant Engineers</td>
 </tr>
</table>
<br><br>

This Seeq Add-on enables engineers and SMEs in OT to directly interface with models built by data science teams in Azure
ML Studio and that have been registered and deployed in an AML endpoint as a cloud service. One way for an engineer or
SME to interface with a model is to apply it in an ad-hoc fashion to generate inferences over a historical period of
interest, perhaps to validate the model's accuracy, or to acquire evidence in support of a hypothesis. Alternatively,
the engineer or SME may decide that the model is ready for scheduled inference, and bring the model "online" using the
Deploy functionality in the Add-on. This Add-on also enables users to scale ML innovations across their organization –
models can be evaluated and deployed in real time on many different assets and processes.

## Data Scientist Workflow

We assume that a Data Scientist has deployed a registered model through an AML endpoint. A brief summary of the 
workflow to register a model in AML is shown in the following video.

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
controls="controls" muted="muted" class="d-block rounded-bottom-2 width-fit" style="max-width:700px; background:transparent url('https://seeq12.github.io/seeq-azureml/_static/ds_workflow_poster.png') no-repeat 0 0;
-webkit-background-size:cover; -moz-background-size:cover; -o-background-size:cover; background-size:cover;"
webboost_found_paused="true" webboost_processed="true">
</video>
</details>

## Model Tagging Convention

When registering a model in Azure ML Studio as part of the Data Scientist workflow, several key pieces of information
may be attached to the model. One such key piece of information is the **tags**
arguement. Models may be "tagged" in one of two ways, which ultimately determine how the model may be applied. The first
convention uses key-value pairs where keys represent the input signals that the model was trained on, in order (e.g. -
input1, input2, etc.), and the values for those keys are the corresponding Seeq signal ID's as shown here:

```
tags = {
    'input1': '4E9416E8-9C75-426A-8E0A-4D07432CAC5D', 
    'input2': '62E6F850-E523-408D-AD10-0C87E65F996B',
    'input3': 'CD732D0B-C3BA-496F-B69E-55543944B5F1',
    'input4': 'F8E053D1-A4D5-4671-9969-1D5D7D4F27DD',
}
```

Selection of an endpoint model with this tag naming convention will NOT provide an option to specify a Seeq asset.

<br>
<table border="0" align="center">
 <tr>
    <td style="max-width: 500px;"><img alt="image" src="../_static/single-asset-endpoint-selection.png"></td>
 </tr>
 <tr>
    <td align="center">Figure 2 - Model Inputs with Tag Naming Convention 1</td>
 </tr>
</table>
<br><br>


Alternatively, if the model's tag naming convention uses **signal names** instead of ID's as values, then we can
leverage the Seeq Asset data structure and apply the model to Assets. The Data Scientist who trained the model will have
also added **Path** tags, specifying the valid Assets on which the model may be applied, as shown here:

```
tags = {
    'input1': 'Relative Humidity', 
    'input2': 'Optimizer',
    'input3': 'Wet Bulb',
    'input4': 'Temperature',
    'Path1': '2407642C-0169-4ED0-A25C-321E29DC975B',
    'Path2': 'AA1E42AE-90BD-4CF7-9449-F8CC81625E8F',
}
```

Selection of an endpoint model with this tag naming convention WILL provide a drop down menu that will allow you to
select the asset on which to apply the model.

<br>
<table border="0" align="center">
 <tr>
    <td style="width: 500px;"><img alt="image" src="../_static/multi-asset-endpoint-selection.png"></td>
 </tr>
 <tr>
    <td align="center">Figure 3 - Model Inputs with Tag Naming Convention 2</td>
 </tr>
</table>
<br><br>

## Engineer/SME Workflow

A brief description of the Engineering workflow is shown in the following video. Details are also provided in the 
sections below.

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
controls="controls" muted="muted" class="d-block rounded-bottom-2 width-fit" style="max-width:670px; background:transparent url('https://seeq12.github.io/seeq-azureml/_static/sme_workflow.png') no-repeat 0 0;
-webkit-background-size:cover; -moz-background-size:cover; -o-background-size:cover; background-size:cover;"
webboost_found_paused="true" webboost_processed="true">
</video>
</details>

## How to Use

The Seeq Add-on is launched from within Seeq Workbench by a user that would like to apply a ML model that has been
registered and deployed in a Microsoft Azure endpoint. A streamlined UI takes the user through a few simple setup steps
that will result in model inferences pushed back into the same Workbench analysis from which it was launched.

When you open the tool, under the Model Inputs section you will first want to *Select the model endpoint*
that contains the model of interest. Depending on how the model was tagged, you may or may not see a second drop down
to *Select asset to apply the model*.

### UI Workflow

* **Model Inputs**

    1. First, select the endpoint containing the model of interest (these would be named by the Data Scientist on the
       AML side during setup).
    2. Depending on how the model was tagged, optionally select the Asset to apply the model.

* **Model Action**

    1. Select either **Investigate** to apply the model in an ad-hoc manner, or select **Deploy** to generate inferences
       on a regular schedule.
        * If **Investigate**, enter a name for ther result signal and specify the **Start** and **End** date-time range
          of the investigation.
        * If **Deploy**, enter a name for ther result signal, provide a name for the scheduled **Job**, and specify the
          frequency of inferences in the form of a valid cron expression, i.e. - "every 15 minutes"
    2. Confirm that your selections for the model are correect in the **Model Summary** section at the bottom of the UI.
    3. Click **Submit**, and done.

### Example of Investigate Option

This setup results in a one-time scoring of historical data over a specific time range.

<br>
<table border="0" align="center">
 <tr>
    <td style="max-width: 480px;"><img alt="image" src="../_static/UI_complete_investigate.png"></td>
 </tr>
 <tr>
    <td align="center">Figure 4 - UI example of Investigate (ad-hoc)</td>
 </tr>
</table>
<br><br>

### Example of Deploy Option

This setup results in a recurring scheduled application of the model to new incoming data at a specified frequency.

<br>
<table border="0" align="center">
 <tr>
    <td style="max-width: 480px;"><img alt="image" src="../_static/UI_complete_deploy.png"></td>
 </tr>
 <tr>
    <td align="center">Figure 5 - UI example of Deploy (scheduled)</td>
 </tr>
</table>
<br><br>

## Output Predictions Pushed into Seeq

Upon submitting an **Investigate** run, results from the model will immediately be pushed into a new worksheet in the
same Seeq Workbench Analysis from which the UI was launched. Upon submitting a **Deploy** job, inferences from the model
will be pushed into the same Seeq Workbench Analysis from which the UI was launched once the amount of time specified in
the "Frequency" field has passed, and then every same period thereafter until the job is cancelled.

As an added benefit for traceability and repeatability, predictions come into Seeq carrying metadata that may be used to
associate the predictions with the source model. Items such as model name, version, and input signals are just a few
pieces of metadata that may be specified as below:

<br>
<table border="0" align="center">
 <tr>
    <td><img alt="image" src="../_static/output_details.png"></td>
 </tr>
 <tr>
    <td align="center">Figure 6 - Model Metadata attached to output predictions in Seeq (highlighted in yellow)</td>
 </tr>
</table>
<br><br>
