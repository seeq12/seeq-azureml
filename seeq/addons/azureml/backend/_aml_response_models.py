import re
from seeq import spy

TRAFFIC_SPLIT = 100


class AmlModel:
    """
    Gets the serialized response from the Azure ML model management endpoint
    and deserializes it

    Attributes
    ----------
    name : str
        Name of the Azure ML model
    id : str
        ID of the Azure ML model
    framework : str
        Framework used for the Azure ML model
    frameworkVersion : str
        Version of the framework used
    version : str
        Azure ML model version
    input_ids : list
        IDs of the Seeq signals that the Azure ML model takes as inputs. If
        provided, asset_path_ids and asset_input_names are disregarded.
    asset_path_ids : list
        IDs of the Seeq asset tree that the Azure ML model takes as inputs.
        This is used in conjunction with asset_input_names to specify the
        signals within the asset tree that are to be used as inputs for the ML
        model
    asset_input_names : list
        Names of the Seeq signals that are to be used as inputs for the ML model.
        These signals must be children of each of the asset trees specified in
        asset_path_ids
    sample_rate : str
        The sampling rate required by the Azure ML model for the input signals.

    Methods
    -------
    deserialize_aml_model_response(json)
        Deserializes the Azure ML response of the model management endpoint
    """

    def __init__(self, name, idd) -> None:
        """
        Parameters
        ----------
        name : str
            Name of the Azure ML model
        idd : str
            ID of the Azure ML model
        """

        self.name = name
        self.id = idd
        self.framework = None
        self.frameworkVersion = None
        self.version = None
        self.input_ids = list()
        self.asset_path_ids = list()
        self.asset_input_names = list()
        self.sample_rate = None

    @staticmethod
    def deserialize_aml_model_response(json):
        """
        Parameters
        ----------
        json: dict
            Serialized response of the Azure ML model management endpoint

        Returns
        -------
        model: seeq.addons.azureml.backend.AmlModel
            Azure ML model properties

        """
        model = AmlModel(json['name'], json['id'])
        model.framework = json['framework']
        model.frameworkVersion = json['frameworkVersion']
        model.version = json['version']
        tags = json['kvTags']
        if len(tags) > 0:
            model.input_ids = {re.search(r'(\d+)', k).group(): v for k, v in tags.items() if
                               k.lower().startswith('input') and spy.utils.is_guid(v)}
            model.asset_path_ids = [v for k, v in tags.items() if k.lower().startswith('path') and spy.utils.is_guid(v)]
            model.asset_input_names = {re.search(r'(\d+)', k).group(): v for k, v in tags.items() if
                                       k.lower().startswith('input') and not spy.utils.is_guid(v)}
            model.sample_rate = tags.get('SampleRate', )
        return model


class OnlineDeployment:
    """
    Gets the serialized response from the Azure ML deployments endpoint and
    deserializes it

    Attributes
    ----------
    id : str
        ID of the Azure ML deployment
    name : str
        Name of the Azure ML deployment
    modelId : str
        ID of the model associated with the Azure ML deployment
    traffic : str
        Allowed traffic to this deployment
    model : str
        Name of the model associated with the Azure ML deployment
    location : str
        Location of the Azure ML deployment

    Methods
    -------
    deserialize_aml_deployment_response(json)
        Deserializes the Azure ML response from the deployment endpoint
    """

    def __init__(self, name, idd, computeType) -> None:
        """
        Parameters
        ----------
        name : str
            Name of the Azure ML deployment
        idd : str or None
            ID of the Azure ML deployment
        """
        self.id = idd
        self.name = name
        self.computeType = computeType
        self.modelId = None
        self.traffic = None
        self.model = None
        self.model_version = None
        self.location = None

    @staticmethod
    def deserialize_aml_deployment_response(json, computeType):
        """
        Gets a serialized response from a given online endpoint in Azure ML and
        deserializes each deployment associated with the endpoint.

        Parameters
        ----------
        json: dict
            Serialized response of the Azure ML deployment endpoint
        computeType: str
            The type of compute: Managed, ACI, K8S

        Returns
        -------
        ods: list
            List of deployments associated with the endpoint

        """
        ods = list()
        for v in json['value']:
            od = OnlineDeployment(name=v['name'], idd=v['id'], computeType=computeType)
            od.modelId = v['properties']['model']['assetId']
            od.location = v['location']
            ods.append(od)
        return ods


class OnlineEndpoint:
    """
    Gets the serialized response from an Azure ML endpoint and
    deserializes it

    Attributes
    ----------
    id : str
        ID of the Azure ML endpoint
    name : str
        Name of the Azure ML endpoint
    type : str
        Type of the Azure ML endpoint
    description : str
        Description of the Azure ML endpoint
    scoringUri : str
        The identifier to access the model associated with the online endpoint
    authMode : str
        Type of authentication used by the endpoint
    provisioningState: str
        State of the endpoint
    createdBy: str
        Name of the user that created the endpoint
    lastModifiedAt: str
        Date of the last time the endpoint was modified
    tags: str
        Tags associated with the endpoint. The only valid tag for integration
        with Seeq is `{Seeq: true}`. If this tag does not exist, the endpoint
        will be disregarded as a Seeq compatible endpoint.
    kind: str
        The endpoint deployment target type (Managed, Container, AKS).
    location: str
        The Azure region that this endpoint is hosted in.
    traffic : str
        Percentage of traffic to each deployment contained within the endpoint.
    deployment: str
        Deployments associated with the endpoint
    primaryKey: str
        Primary access key for the endpoint
    secondaryKey: str
        Secondary access key for the endpoint

    Methods
    -------
    deserialize_unmanaged_endpoint_response(json)
        Deserializes the Azure ML response from the unmanaged online endpoints endpoint

    deserialize_managed_endpoint_response
        Deserializes the Azure ML response from the managed online endpoints endpoint

    add_deployment(seeq.addons.azureml.backend.OnlineDeployment)
        Adds an OnlineDeployment to the endpoint only if the traffic split
        requirement is met.
    """

    def __init__(self, name, idd) -> None:
        """
        Parameters
        ----------
        name : str
            Name of the Azure ML endpoint
        idd : str
            ID of the Azure ML endpoint
        """
        self.id = idd
        self.name = name
        self.type = None
        self.description = None
        self.scoringUri = None
        self.authMode = None
        self.provisioningState = None
        self.createdBy = None
        self.lastModifiedAt = None
        self.tags = None
        self.kind = None
        self.location = None
        self.traffic = None
        self.deployment = list()
        self.primaryKey = None
        self.secondaryKey = None

    @staticmethod
    def deserialize_unmanaged_endpoint_response(json):
        """
        Deserializes the Azure ML response services response for ACI models

        Parameters
        ----------
        json: dict
            Serialized response of the Azure ML online endpoints

        Returns
        -------
        oes: list
            List of endpoints with `{'Seeq': true}` tag

        """
        oes = list()
        for v in json['value']:
            if 'Seeq' not in v['kvTags']:
                continue
            oe = OnlineEndpoint(name=v['name'], idd=v['id'])
            oe.tags = v['kvTags']
            oe.type = "Microsoft.MachineLearningServices/workspaces/onlineEndpoints"
            oe.description = v['description']
            oe.scoringUri = v['scoringUri']
            oe.authMode = v['authEnabled']
            oe.kind = 'ACI'
            oe.createdBy = v['createdBy']['userName']
            oe.lastModifiedAt = v['updatedTime']
            oe.location = v['location']
            od = OnlineDeployment(oe.name, None, oe.type)
            od.location = oe.location
            od.model = (v['environmentImageRequest']['modelIds'][0]).split(':')[0]
            od.model_version = (v['environmentImageRequest']['modelIds'][0]).split(':')[1]
            od.traffic = 100
            oe.deployment.append(od)
            oes.append(oe)
        return oes


    @staticmethod
    def deserialize_managed_endpoint_response(json):
        """
        Deserializes the Azure ML response from the online endpoints endpoint

        Parameters
        ----------
        json: dict
            Serialized response of the Azure ML online endpoints

        Returns
        -------
        oes: list
            List of endpoints with `{'Seeq': true}` tag

        """
        oes = list()
        for v in json['value']:
            if 'Seeq' not in v['tags']:
                continue
            oe = OnlineEndpoint(name=v['name'], idd=v['id'])
            oe.tags = v['tags']
            oe.type = v['type']
            oe.description = v['properties']['description']
            oe.scoringUri = v['properties']['scoringUri']
            oe.authMode = v['properties']['authMode']
            oe.traffic = v['properties']['traffic']
            oe.provisioningState = v['properties']['provisioningState']
            oe.createdBy = v['systemData']['createdBy']
            oe.lastModifiedAt = v['systemData']['lastModifiedAt']
            oe.kind = v['kind']
            oe.location = v['location']
            oes.append(oe)
        return oes

    def add_deployment(self, deployment):
        """

        Parameters
        ----------
        deployment: seeq.addons.azureml.backend.OnlineDeployment
            A deserialized OnlineDeployment object

        Returns
        -------
        -: None

        """
        deployment.traffic = self.traffic.get(deployment.name)
        if deployment.traffic == TRAFFIC_SPLIT:
            self.deployment.append(deployment)
