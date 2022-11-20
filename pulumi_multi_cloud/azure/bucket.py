from pulumi_azure_native import storage
from pulumi_azure_native.resources import ResourceGroup

from pulumi_multi_cloud.common import ProviderCloudResourceGenerator, MultiCloudResourceCreation, CloudRegion
from pulumi_multi_cloud.resources.resource import MultiCloudResource


class AzureBucketGenerator(ProviderCloudResourceGenerator):

    def __init__(self, name: str, region: CloudRegion, resource_group: ResourceGroup):
        super().__init__(name, region)
        self.resource_group = resource_group

    def generate_resources(self) -> MultiCloudResourceCreation:
        storage_account = storage.StorageAccount(self.name,
                                                 kind=storage.Kind.STORAGE_V2,
                                                 resource_group_name=self.resource_group.name)
        return MultiCloudResourceCreation(MultiCloudResource.given(storage_account))
