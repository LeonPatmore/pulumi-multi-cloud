from pulumi_aws import s3

from pulumi_multi_cloud.aws.common import AwsCloudResource
from pulumi_multi_cloud.common import ProviderCloudResourceGenerator, ProviderCloudResource


class AwsBucketGenerator(ProviderCloudResourceGenerator):

    def generate_resources(self) -> list[ProviderCloudResource]:
        return [ProviderCloudResource(s3.Bucket(self.name), AwsCloudResource)]
