from abc import ABC

import pulumi
from pulumi import Output


class MultiCloudResourceTemplate:

    def __init__(self, resource: type(pulumi.Resource), secondary_resources: list = None):
        if secondary_resources is None:
            secondary_resources = []
        self.resource = resource
        self.secondary_resources = secondary_resources

    def get_id(self) -> Output:
        raise NotImplementedError()


class MultiCloudResource(MultiCloudResourceTemplate, ABC):

    def __init__(self, resource: type(pulumi.Resource), secondary_resources: list[MultiCloudResourceTemplate] = None):
        super().__init__(resource, secondary_resources)

    def with_child_resource(self, resource: MultiCloudResourceTemplate):
        if self.secondary_resources is None:
            self.secondary_resources = []
        self.secondary_resources.append(resource)
        return self
