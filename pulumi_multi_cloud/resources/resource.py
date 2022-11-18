import pulumi
from pulumi import Output


class MultiCloudResource(pulumi.CustomResource):

    def get_id(self) -> Output:
        raise NotImplementedError()
