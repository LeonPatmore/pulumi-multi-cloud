from pulumi_azure_native.resources import ResourceGroup

from pulumi_multi_cloud.common import MultiCloudResourceFactory, CloudRegion, DEFAULT_REGION


class AzureResourceFactory(MultiCloudResourceFactory):

    def __init__(self, resource_group: ResourceGroup, region: CloudRegion = DEFAULT_REGION):
        super().__init__(region=region, provider_global_attributes={
            "resource_group": resource_group
        })
