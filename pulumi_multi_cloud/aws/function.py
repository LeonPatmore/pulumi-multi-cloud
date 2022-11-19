import json

import pulumi
import pulumi_aws
from pulumi import ResourceOptions
from pulumi_aws import apigateway, lambda_
from pulumi_aws.apigateway import RestApi
from pulumi_aws.lambda_ import Function

from pulumi_multi_cloud.aws.common import AwsCloudResource
from pulumi_multi_cloud.common import MultiCloudResourceCreation
from pulumi_multi_cloud.resources.function import FunctionRuntime, ProviderFunctionResourceGenerator, \
    MultiCloudFunctionCreation

AWS_RUNTIME = {
    FunctionRuntime.Python39: "python3.9"
}


class AwsFunctionCreation(MultiCloudFunctionCreation):

    def http_url(self) -> pulumi.Output[str]:
        return self.secondary_resources[1].invoke_url


class AwsFunctionGenerator(ProviderFunctionResourceGenerator):

    @staticmethod
    def _generate_spec(arn: str):
        lambda_uri = f"arn:aws:apigateway:{pulumi_aws.get_region().id}:lambda:path/2015-03-31/functions/{arn}/invocations"
        return {
            "swagger": "2.0",
            "info": {"title": "api", "version": "1.0"},
            "paths": {
                "/{proxy+}": {
                    "x-amazon-apigateway-any-method": {
                        "x-amazon-apigateway-integration": {
                            "uri": lambda_uri,
                            "passthroughBehavior": "when_no_match",
                            "type": "aws_proxy",
                            "httpMethod": "POST"
                        }
                    }
                }
            }
        }

    def _expose_http(self, func: Function) -> tuple:

        def get_execution_arn(arn: str):
            gw_id = arn.split("/")[-1]
            return f"arn:aws:execute-api:{pulumi_aws.get_region().id}:{pulumi_aws.get_caller_identity().account_id}:{gw_id}/*/*/*"

        api = RestApi(f"{self.name}-api",
                      body=func.arn.apply(lambda arn: json.dumps(self._generate_spec(arn))))
        deployment = apigateway.Deployment("api-deployment",
                                           rest_api=api.id,
                                           stage_name="Prod",
                                           opts=ResourceOptions(depends_on=[api]))
        invoke_permission = lambda_.Permission("api-lambda-permission",
                                               action="lambda:invokeFunction",
                                               function=func.name,
                                               principal="apigateway.amazonaws.com",
                                               source_arn=api.arn.apply(get_execution_arn),
                                               opts=ResourceOptions(depends_on=[api]))
        return api, deployment, invoke_permission

    def generate_resources(self) -> MultiCloudResourceCreation:
        function = Function(self.name,
                            code=self.files,
                            runtime=AWS_RUNTIME[self.runtime],
                            handler=f"{self.function_handler.file}.{self.function_handler.method}",
                            role=self.permissions.arn)
        creation = AwsFunctionCreation(AwsCloudResource.given(function))
        if self.http_trigger:
            api, deployment, invoke_permission = self._expose_http(function)
            creation.with_resource(AwsCloudResource.given(api))\
                .with_resource(AwsCloudResource.given(deployment))\
                .with_resource(AwsCloudResource.given(invoke_permission))
        return creation
