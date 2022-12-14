from pulumi_multi_cloud.common import ProviderCloudResourceGenerator, CloudRegion
from pulumi_multi_cloud.resources.resource import MultiCloudResource


class ProviderQueueResourceGenerator(ProviderCloudResourceGenerator):

    def __init__(self,
                 name: str,
                 region: CloudRegion):
        super().__init__(name, region)

    def generate_resources(self) -> MultiCloudResource:
        raise NotImplementedError()
