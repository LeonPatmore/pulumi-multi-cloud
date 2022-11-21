from pulumi_gcp.storage import bucket

from pulumi_multi_cloud.common import ProviderCloudResourceGenerator, MultiCloudResourceCreation
from pulumi_multi_cloud.gcp.common import GcpCloudResource


class GcpBucketGenerator(ProviderCloudResourceGenerator):

    def generate_resources(self) -> MultiCloudResourceCreation:
        return MultiCloudResourceCreation(GcpCloudResource(bucket.Bucket(self.name, location=self.region.name)))
