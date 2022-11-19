import pulumi

from pulumi_multi_cloud.resources.resource import MultiCloudResource


class GcpCloudResource(MultiCloudResource):

    def get_id(self) -> str:
        return self.name

    @staticmethod
    def given(resource: pulumi.Resource):
        resource.__class__ = GcpCloudResource
        return resource
