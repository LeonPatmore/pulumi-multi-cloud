from pulumi_aws import s3

from pulumi_multi_cloud.aws.common import AwsCloudResource
from pulumi_multi_cloud.common import ProviderCloudResourceGenerator
from pulumi_multi_cloud.resources.resource import MultiCloudResource


class AwsBucketGenerator(ProviderCloudResourceGenerator):

    def generate_resources(self) -> MultiCloudResource:
        return AwsCloudResource(s3.Bucket(self.name))
