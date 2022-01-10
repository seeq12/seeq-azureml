import pickle
from seeq import spy
from seeq.sdk import *
from seeq.addons.azureml.backend import AmlOnlineEndpointService, OnlineEndpoint
from seeq.addons.azureml.utils import AzureMLException
from seeq.addons.azureml import _config


class ModelInputsProvider:
    """
    Provides the Seeq and AmlOnlineEndpointService inputs to the Azure ML model
    based upon user selections

    Attributes
    ----------
    endpoint_svc: seeq.addons.azureml.backend.AmlOnlineEndpointService
        An instance of the AmlOnlineEndpointService to make the necessary calls
        to Azure ML services.
    endpoints: dict
        Dictionary with endpoint names as keys and OnlineEndpoint(s) as values.
    deployment: seeq.addons.azureml.backend.OnlineDeployment
        Deployment associated with the selected OnlineEndpoint.
    asset_paths: dict
        Dictionary containing the valid Seeq asset trees on which the model may
        be applied. The name of the asset trees are the keys and asset tree IDs
        are the values.
    model_name: str
        Name of the Azure ML model for the selected OnlineDeployment.
    model_version: str
        Version of the Azure ML model for the selected OnlineDeployment.
    model_signal_inputs: dict
        Dictionary with the input signals for the Azure ML model which are
        pulled from Seeq. The name of the signals are the keys of the
        dict and the IDs of the signals are the values.
    model_sample_rate: str
        The sampling rate required by the Azure ML model for the input signals.
        For example, '2 min'.
    model_endpoint_uri: str
        The endpoint identifier of the AzureML model used to compute the result
        signal.
    asset_path_from_signals: dict
        This attribute is determined when the Azure ML model specifies signal
        IDs as inputs rather than asset path IDs. If the input signals belong
        to the same asset tree, then the name and ID of the asset tree are
        stored as a key-value pair, {name: ID}. Otherwise, this attribute will
        default to None.

    """
    def __init__(self, config_file=None):
        _config.validate_configuration_file(config_file)
        self.endpoint_svc = AmlOnlineEndpointService(tenant_id=_config.get('azure', 'TENANT_ID'),
                                                     app_id=_config.get('azure', 'APP_ID'),
                                                     app_secret=_config.get('azure', 'APP_SECRET'),
                                                     subscription_id=_config.get('azure', 'SUBSCRIPTION_ID'),
                                                     resource_group=_config.get('azure', 'RESOURCE_GROUP'),
                                                     workspace_name=_config.get('azure', 'WORKSPACE_NAME'))

        self.endpoints = self.get_endpoints()
        self.deployment = None
        self.asset_paths = None
        self.model_name = None
        self.model_version = None
        self.model_signal_inputs = None
        self.model_sample_rate = None
        self.model_endpoint_uri = None
        self.asset_path_from_signals = None
        self._model_primary_key = None

    def get_endpoints(self):
        names = [x.name for x in self.endpoint_svc.list_online_endpoints()]
        renames = _rename_duplicates(names)
        return dict(zip(renames, self.endpoint_svc.list_online_endpoints()))

    def update_deployment_from_endpoint(self, endpoint: OnlineEndpoint):
        deployments = [x for x in endpoint.deployment]
        if len(deployments) > 1:
            raise AzureMLException(code=None, reason=None,
                                   message=f"Only one deployment per endpoint is allowed. Got {len(deployments)}")
        if len(deployments) == 0:
            raise AzureMLException(code=None, reason=None,
                                   message=f'There are no deployments associated with endpoint "{endpoint.name}"')
        self.deployment = deployments[0]
        if self.deployment.model is not None:
            self.model_name = self.deployment.model.name
            self.model_version = self.deployment.model.version
            self.model_sample_rate = self.deployment.model.sample_rate
            self.model_endpoint_uri = endpoint.scoringUri
            self._model_primary_key = endpoint.primaryKey

    def update_assets_from_endpoint(self, endpoint: OnlineEndpoint):
        self.asset_paths = None
        trees_api = TreesApi(spy.client)
        self.update_deployment_from_endpoint(endpoint)
        if self.deployment.model is None:
            return
        if len(self.deployment.model.asset_path_ids) > 0:
            if len(self.deployment.model.asset_input_names) == 0:
                raise AzureMLException(code=None, reason=None,
                                       message=f"Path IDs were found in model {self.model_name}:{self.model_version}, "
                                               f"but the input signals for the model are not defined")
            asset_path_names = list()
            for idd in self.deployment.model.asset_path_ids:
                tree = trees_api.get_tree(id=idd)
                asset_path_names.append(f"{' >> '.join([x.name for x in tree.item.ancestors if x.type == 'Asset'])} >> "
                                        f"{tree.item.name}")
            asset_path_names = _rename_duplicates(asset_path_names)
            self.asset_paths = dict(zip(asset_path_names, self.deployment.model.asset_path_ids))

    def update_signal_inputs_from_endpoint(self, endpoint, asset_path_id=None):
        trees_api = TreesApi(spy.client)
        signals_api = SignalsApi(spy.client)
        self.update_deployment_from_endpoint(endpoint)
        if self.deployment.model is None:
            return
        if len(self.deployment.model.input_ids) > 0:  # if there are signals IDs for the model, then disregard assets

            # check if the inputs belong to the same asset path
            asset_paths = list()
            path_ids = list()
            signal_names = list()
            ordered_input_ids = _order_inputs(self.deployment.model.input_ids)

            for idd in ordered_input_ids:
                tree = trees_api.get_tree(id=idd)
                path = " >> ".join([x.name for x in tree.item.ancestors if x.type == "Asset"])
                path_ids.append(tree.item.ancestors[-1].id)
                asset_paths.append(path)
                signal_names.append(signals_api.get_signal(id=idd).name)
            if len(list(set(asset_paths))) == 1:
                self.asset_path_from_signals = {asset_paths[0]: path_ids[0]}
            else:
                self.asset_path_from_signals = None
            signal_names = _rename_duplicates(signal_names)
            self.model_signal_inputs = dict(zip(signal_names, ordered_input_ids))
            return

        elif asset_path_id is not None:
            ordered_input_names = _order_inputs(self.deployment.model.asset_input_names)
            tree = trees_api.get_tree(id=asset_path_id)
            signal_names = []
            signal_ids = []
            for child in tree.children:
                if child.name in ordered_input_names:
                    signal_names.append(child.name)
                    signal_ids.append(child.id)
            signal_names = _rename_duplicates(signal_names)
            model_signal_inputs = dict(zip(signal_names, signal_ids))

            # AD-1076
            self.model_signal_inputs = {k: model_signal_inputs[k] for k in ordered_input_names}

    def _serialize(self, filename='model_inputs.pk'):
        with open(filename, 'wb') as f:
            pickle.dump(self, f)


def _rename_duplicates(names: list) -> list:
    return [f"{name}{str(names[:i].count(name) + 1)}" if names.count(name) > 1 else name for i, name in
            enumerate(names)]


def _order_inputs(inputs: dict) -> list:
    input_numbers = list(map(str, range(1, len(inputs) + 1)))
    if not all(item in inputs.keys() for item in input_numbers):
        message = f'This model has an incomplete input signal specification. Expected {len(inputs)} input signals ' \
                  f'in sequential order but got inputs: {sorted(list(inputs.keys()))}'
        raise AzureMLException(code=None, reason=None, message=message)
    return [inputs[k] for k in input_numbers]
