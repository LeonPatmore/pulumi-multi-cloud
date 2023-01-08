import pulumi
from pulumi import Output
from pulumi_azure_native import storage
from pulumi_azure_native.resources import ResourceGroup
from pulumi_azure_native.web import WebApp, SiteConfigArgs

from pulumi_multi_cloud.azure.bucket import AzureBucketGenerator
from pulumi_multi_cloud.azure.common import AzureResourceGenerator, AzureCloudResource
from pulumi_multi_cloud.resources.function import ProviderFunctionResourceGenerator, MultiCloudFunction


class AzureFunction(AzureCloudResource, MultiCloudFunction):

    def http_url(self) -> pulumi.Output[str]:
        return self.resource.default_host_name


class AzureFunctionGenerator(ProviderFunctionResourceGenerator, AzureResourceGenerator):

    def __init__(self, resource_group: ResourceGroup, **kwargs):
        super().__init__(**kwargs)
        AzureResourceGenerator.__init__(self, resource_group)

    def _upload_code(self) -> tuple:
        storage_account = AzureBucketGenerator(self.name, self.region, self.resource_group).generate_resources().resource
        container = storage.BlobContainer(f"{self.name}-code-container",
                                          resource_group_name=self.resource_group.name,
                                          account_name=storage_account.name)
        code_blob = storage.Blob(f"{self.name}-code",
                                 resource_group_name=self.resource_group.name,
                                 account_name=storage_account.name,
                                 container_name=container.name,
                                 source=self.files)
        return storage_account, container, code_blob

    def generate_resources(self) -> MultiCloudFunction:
        storage_account, container, code_blob = self._upload_code()
        storage_key = storage.list_storage_account_keys_output(
            resource_group_name=self.resource_group.name,
            account_name=storage_account.name).keys[0].value
        storage_connection_string = Output.all(storage_key, storage_account.name).apply(
            lambda args: f"DefaultEndpointsProtocol=https;AccountName={args[1]};AccountKey=${args[0]}")
        storage_token = storage.list_storage_account_service_sas_output(
            account_name=storage_account.name,
            shared_access_expiry_time="2030-01-01",
            shared_access_start_time="2021-01-01",
            resource=storage.SignedResource.C,
            protocols=storage.HttpProtocol.HTTPS,
            resource_group_name=self.resource_group.name,
            permissions=storage.Permissions.R,
            canonicalized_resource=Output.all(storage_account.name, container.name).apply(
                lambda args: f"/blob/{args[0]}/{args[1]}")
        ).service_sas_token
        code_url = Output.all(storage_account.name, container.name, code_blob.name, storage_token).apply(
            lambda args: f"https://{args[0]}.blob.core.windows.net/{args[1]}/{args[2]}?{args[3]}")

        function = WebApp(self.name,
                          resource_group_name=self.resource_group.name,
                          kind="functionapp",
                          site_config=SiteConfigArgs(
                              app_settings=[
                                  {
                                      "name": "runtime",
                                      "value": "python"
                                  },
                                  {
                                      "name": "FUNCTIONS_EXTENSION_VERSION",
                                      "value": "~4"
                                  },
                                  {
                                      "name": "FUNCTIONS_WORKER_RUNTIME",
                                      "value": "python"
                                  },
                                  {
                                      "name": "WEBSITE_RUN_FROM_PACKAGE",
                                      "value": code_url
                                  }
                              ]
                          ))
        return AzureFunction(function, [
            AzureCloudResource(storage_account),
            AzureCloudResource(container),
            AzureCloudResource(code_blob)
        ])
