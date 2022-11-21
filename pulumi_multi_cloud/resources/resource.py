import pulumi
from pulumi import Output


class MultiCloudResource:

    def __init__(self, resource: type(pulumi.Resource)):
        self.resource = resource

    def get_id(self) -> Output:
        raise NotImplementedError()
