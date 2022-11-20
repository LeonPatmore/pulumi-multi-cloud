import pulumi
from pulumi import Output


class MultiCloudResource(pulumi.CustomResource):

    def get_id(self) -> Output:
        raise NotImplementedError()

    @staticmethod
    def given(resource: pulumi.Resource):
        resource.__class__ = MultiCloudResource
        return resource
