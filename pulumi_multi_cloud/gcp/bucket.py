from pulumi_gcp.storage import bucket

from pulumi_multi_cloud.common import ProviderCloudResourceGenerator, MultiCloudResource
from pulumi_multi_cloud.gcp.common import GcpCloudResource


class GcpBucketGenerator(ProviderCloudResourceGenerator):

    def generate_resources(self) -> MultiCloudResource:
        return GcpCloudResource(bucket.Bucket(self.name, location=self.region.name))
