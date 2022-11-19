import pulumi

from pulumi_multi_cloud.resources.resource import MultiCloudResource


class AwsCloudResource(MultiCloudResource):

    def get_id(self) -> str:
        return self.arn

    @staticmethod
    def given(resource: pulumi.Resource):
        resource.__class__ = AwsCloudResource
        return resource
