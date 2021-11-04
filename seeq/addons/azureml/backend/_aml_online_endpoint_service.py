import requests
from datetime import datetime, timedelta
from ._aml_response_models import OnlineDeployment, OnlineEndpoint, AmlModel
from seeq.addons.azureml.utils import AzureMLException


class AmlOnlineEndpointService:
    """
    Provides a service to connect to Azure ML Studio and get endpoints that are
    tagged with `{Seeq: true}` and their associated deployments and models.

    Methods
    -------
    list_online_endpoints()
        Returns a list containing online endpoints tagged with `{Seeq: true}` in Azure ML Studio

    """

    def __init__(self, tenant_id, app_id, app_secret, subscription_id, resource_group, workspace_name) -> None:
        self._tenant_id = tenant_id
        self._app_id = app_id
        self._app_secret = app_secret
        self._subscription_id = subscription_id
        self._resource_group = resource_group
        self._workspace_name = workspace_name
        self._token = None
        self._token_expires_on = None

    def _authorize(self):

        """
        Private method to authenticate to https://login.microsoftonline.com

        Returns
        -------
        token: str
            Authentication token

        """

        if self._token is not None:
            if self._token_expires_on is not None:
                if datetime.now() < self._token_expires_on:
                    return self._token

        url = f"https://login.microsoftonline.com/{self._tenant_id}/oauth2/token?api-version=1.0"
        payload = f"client_secret={self._app_secret}&grant_type=client_credentials&resource=https%3A%2F%2Fmanagement." \
                  f"core.windows.net%2F&client_id={self._app_id}"
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        response = requests.post(url, headers=headers, data=payload)

        if response.status_code != 200:
            raise AzureMLException(code=response.status_code, reason=response.reason, message="Azure Login Failed")

        token_info = response.json()
        self._token = token_info['access_token']
        self._token_expires_on = datetime.now() + timedelta(minutes=59)
        return self._token

    def _get_base_mgmt_url(self):
        """
        Private method to get the base management URL

        Returns
        -------
        url, headers: tuple (str, str)
            URL and headers of the management service

        """
        url = f"https://management.azure.com/subscriptions/{self._subscription_id}/resourceGroups/" \
              f"{self._resource_group}/providers/Microsoft.MachineLearningServices/workspaces/{self._workspace_name}/"
        headers = {'Authorization': f'Bearer {self._authorize()}'}
        return url, headers

    def _get_models(self, deployment: OnlineDeployment):
        """
        Private method to get models associated with a given deployment
        in Azure ML Studio and attach them to the OnlineDeployment object

        Parameters
        ----------
        deployment: seeq.addons.azureml.backend.OnlineDeployment

        Returns
        -------
        -: None

        """
        path = deployment.modelId.replace('/versions/', ':')
        url = f"https://ml.azure.com/api/{deployment.location}/modelmanagement/v1.0{path}"
        headers = {'Authorization': f'Bearer {self._authorize()}'}

        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise AzureMLException(code=response.status_code, reason=response.reason, message="Error getting models")

        model = AmlModel.deserialize_aml_model_response(response.json())
        deployment.model = model

    def _add_deployments_to_endpoint(self, endpoint: OnlineEndpoint):
        """
        Private method to get the associated deployments for an online endpoint
        in Azure ML Studio and attach them to the OnlineEndpoint object

        Parameters
        ----------
        endpoint: seeq.addons.azureml.backend.OnlineEndpoint

        Returns
        -------
        -: None

        """

        url_base, headers = self._get_base_mgmt_url()

        url = f"{url_base}onlineEndpoints/{endpoint.name}/deployments?api-version=2021-03-01-preview"
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise AzureMLException(code=response.status_code, reason=response.reason,
                                   message="Error getting deployments")

        deployments = OnlineDeployment.deserialize_aml_deployment_response(response.json())

        for d in deployments:
            self._get_models(d)
            endpoint.add_deployment(d)
        return endpoint

    def _add_keys_to_endpoint(self, endpoint: OnlineEndpoint):
        """
        Private method to attach the primary and secondary keys to a given
        OnlineEndpoint object

        Parameters
        ----------
        endpoint: seeq.addons.azureml.backend.OnlineEndpoint

        Returns
        -------
        -: None

        """

        base_url, headers = self._get_base_mgmt_url()

        url = f"{base_url}onlineEndpoints/{endpoint.name}/listKeys?api-version=2021-03-01-preview"

        response = requests.post(url, headers=headers)

        if response.status_code != 200:
            raise AzureMLException(code=response.status_code, reason=response.reason,
                                   message=f"Error listing keys for endpoint. Endpoint name: {endpoint.name}")
        keys = response.json()
        endpoint.primaryKey = keys['primaryKey']
        endpoint.secondaryKey = keys['secondaryKey']

    def _get_online_endpoints(self):
        """
        Private method to get a list of endpoints tagged with `{Seeq: true}` in
        Azure ML Studio and attach the associated deployments and models in
        the endpoint to each OnlineEndpoint object

        Returns
        -------
        oes: list
            List of OnlineEndpoint objects with deployments and models attached
            to each object
        """
        url_base, headers = self._get_base_mgmt_url()
        url = f"{url_base}onlineEndpoints?api-version=2021-03-01-preview"
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            raise AzureMLException(code=response.status_code, reason=response.reason, message="Error getting endpoints")

        oes = OnlineEndpoint.deserialize_aml_endpoint_response(response.json())
        for oe in oes:
            self._add_keys_to_endpoint(oe)
            self._add_deployments_to_endpoint(oe)
        return oes

    def list_online_endpoints(self):
        """
        Public method to get a list of endpoints tagged with `{Seeq: true}` in
        Azure ML Studio and attach the associated deployments and models in
        the endpoint to each OnlineEndpoint object.

        Returns
        -------
        oes: list
            List of OnlineEndpoint objects with deployments and models attached
            to each object
        """
        return self._get_online_endpoints()


def exception_message(message, code, reason):
    return f'{message}. Return code: {str(code)} with reason: {str(reason)}'
