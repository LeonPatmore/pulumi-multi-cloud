from pulumi_aws import sqs

from pulumi_multi_cloud.aws.common import AwsCloudResource
from pulumi_multi_cloud.resources.queue import ProviderQueueResourceGenerator
from pulumi_multi_cloud.resources.resource import MultiCloudResource


class AwsQueueGenerator(ProviderQueueResourceGenerator):

    def generate_resources(self) -> MultiCloudResource:
        return AwsCloudResource(sqs.Queue(self.name))
