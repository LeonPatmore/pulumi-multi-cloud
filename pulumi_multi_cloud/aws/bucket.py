from pulumi_aws import s3

from pulumi_multi_cloud.aws.common import AwsCloudResource
from pulumi_multi_cloud.common import ProviderCloudResourceGenerator, MultiCloudResourceCreation


class AwsBucketGenerator(ProviderCloudResourceGenerator):

    def generate_resources(self) -> MultiCloudResourceCreation:
        return MultiCloudResourceCreation(AwsCloudResource.given(s3.Bucket(self.name)))
