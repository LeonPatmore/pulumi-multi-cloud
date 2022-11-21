from pulumi_azure_native import storage
from pulumi_azure_native.resources import ResourceGroup

from pulumi_multi_cloud.azure.common import AzureCloudResource
from pulumi_multi_cloud.common import ProviderCloudResourceGenerator, MultiCloudResourceCreation, CloudRegion


class AzureBucketGenerator(ProviderCloudResourceGenerator):

    def __init__(self, name: str, region: CloudRegion, resource_group: ResourceGroup):
        super().__init__(name, region)
        self.resource_group = resource_group

    def azure_compatible_name(self):
        return self.name.replace("-", "").lower()

    def generate_resources(self) -> MultiCloudResourceCreation:
        storage_account = storage.StorageAccount(self.azure_compatible_name(),
                                                 kind=storage.Kind.STORAGE_V2,
                                                 resource_group_name=self.resource_group.name,
                                                 sku=storage.SkuArgs(name=storage.SkuName.STANDARD_LRS))
        return MultiCloudResourceCreation(AzureCloudResource(storage_account))
