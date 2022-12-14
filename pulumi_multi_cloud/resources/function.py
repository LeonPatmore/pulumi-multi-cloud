import enum
from abc import ABC

import pulumi
from pulumi import Archive

from pulumi_multi_cloud.common import CloudRegion, ProviderCloudResourceGenerator
from pulumi_multi_cloud.resources.resource import MultiCloudResource


class FunctionRuntime(enum.Enum):

    Python39 = enum.auto()


class FunctionHandler:

    def __init__(self, file: str = "main", method: str = "handle"):
        self.file = file
        self.method = method


class FunctionHttpTrigger:

    def __init__(self, public: bool):
        self.public = public


class MultiCloudFunction(MultiCloudResource, ABC):

    def http_url(self) -> pulumi.Output[str]:
        raise NotImplementedError()


class ProviderFunctionResourceGenerator(ProviderCloudResourceGenerator):

    def __init__(self,
                 name: str,
                 region: CloudRegion,
                 runtime: FunctionRuntime,
                 function_handler: FunctionHandler,
                 files: Archive,
                 permissions: type(MultiCloudResource),
                 http_trigger: FunctionHttpTrigger = None):
        super().__init__(name, region)
        self.runtime = runtime
        self.function_handler = function_handler
        self.files = files
        self.permissions = permissions
        self.http_trigger = http_trigger

    def generate_resources(self) -> MultiCloudFunction:
        raise NotImplementedError()
