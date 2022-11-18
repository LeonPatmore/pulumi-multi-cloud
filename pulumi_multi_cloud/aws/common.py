from pulumi_multi_cloud.resources.resource import MultiCloudResource


class AwsCloudResource(MultiCloudResource):

    def get_id(self) -> str:
        return self.arn
