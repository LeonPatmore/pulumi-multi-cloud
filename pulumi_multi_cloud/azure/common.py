from pulumi_azure_native.resources import ResourceGroup

from pulumi_multi_cloud.common import MultiCloudResourceFactory, CloudRegion, DEFAULT_REGION, CloudProvider
from pulumi_multi_cloud.resources.resource import MultiCloudResource


class AzureResourceFactory(MultiCloudResourceFactory):

    def __init__(self, resource_group: ResourceGroup, region: CloudRegion = DEFAULT_REGION):
        super().__init__(region=region, provider=CloudProvider.AZURE, provider_global_attributes={
            "resource_group": resource_group
        })


class AzureResourceGenerator:

    def __init__(self, resource_group):
        self.resource_group = resource_group


class AzureCloudResource(MultiCloudResource):

    def get_id(self) -> str:
        return self.resource.identity
