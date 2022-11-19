from pulumi_aws.lambda_ import Function

from pulumi_multi_cloud.aws.common import AwsCloudResource
from pulumi_multi_cloud.common import MultiCloudResourceCreation
from pulumi_multi_cloud.resources.function import FunctionRuntime, ProviderFunctionResourceGenerator

AWS_RUNTIME = {
    FunctionRuntime.Python39: "python3.9"
}


class AwsFunctionGenerator(ProviderFunctionResourceGenerator):

    def generate_resources(self) -> MultiCloudResourceCreation:
        function = Function(self.name,
                            code=self.files,
                            runtime=AWS_RUNTIME[self.runtime],
                            handler=f"{self.function_handler.file}.{self.function_handler.method}",
                            role=self.permissions.arn)
        return MultiCloudResourceCreation(AwsCloudResource.given(function))
