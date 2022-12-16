import hashlib
import json

import pulumi
import pulumi_aws
from pulumi import ResourceOptions, Output
from pulumi_aws import apigateway, lambda_
from pulumi_aws.apigateway import RestApi
from pulumi_aws.iam import PolicyAttachment, Policy
from pulumi_aws.lambda_ import Function, EventSourceMapping

from pulumi_multi_cloud.aws.common import AwsCloudResource
from pulumi_multi_cloud.resources.function import FunctionRuntime, ProviderFunctionResourceGenerator, \
    MultiCloudFunction, FunctionQueueTrigger

AWS_RUNTIME = {
    FunctionRuntime.Python39: "python3.9"
}


class AwsFunction(AwsCloudResource, MultiCloudFunction):

    def http_url(self) -> pulumi.Output[str]:
        return self.secondary_resources[1].resource.invoke_url


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
                },
                "/": {
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
                                           opts=ResourceOptions(depends_on=[api]),
                                           triggers={
                                               "redeployment": api.body.apply(lambda body: json.dumps(body)).apply(
                                                   lambda to_json: hashlib.sha1(to_json.encode()).hexdigest()),
                                           })
        invoke_permission = lambda_.Permission("api-lambda-permission",
                                               action="lambda:invokeFunction",
                                               function=func.name,
                                               principal="apigateway.amazonaws.com",
                                               source_arn=api.arn.apply(get_execution_arn),
                                               opts=ResourceOptions(depends_on=[api]))
        return api, deployment, invoke_permission

    def _add_queue_trigger(self, func: Function, trigger: FunctionQueueTrigger):
        policy = Policy(f"receive_message_{trigger.name}",
                        path="/",
                        description=f"can receive sqs messages from {trigger.name}",
                        policy=trigger.queue.resource.arn.apply(lambda arn: json.dumps({
                            "Version": "2012-10-17",
                            "Statement": [{
                                "Action": [
                                    "sqs:ReceiveMessage",
                                    "sqs:DeleteMessage",
                                    "sqs:DeleteMessageBatch",
                                    "sqs:GetQueueAttributes"
                                ],
                                "Effect": "Allow",
                                "Resource": arn,
                            }],
                        })))
        attachment = PolicyAttachment(f"receive_message_{trigger.name}_attachment",
                                      roles=[self.permissions.resource.name],
                                      policy_arn=policy.arn)
        event_source_mapping = EventSourceMapping(f"{self.name}-mapping",
                                                  event_source_arn=trigger.queue.resource.arn,
                                                  function_name=func.arn)
        return policy, attachment, event_source_mapping

    def generate_resources(self) -> MultiCloudFunction:
        function = Function(self.name,
                            code=self.files,
                            runtime=AWS_RUNTIME[self.runtime],
                            handler=f"{self.function_handler.file}.{self.function_handler.method}",
                            role=self.permissions.resource.arn)
        creation = AwsFunction(function)
        if self.http_trigger:
            api, deployment, invoke_permission = self._expose_http(function)
            creation.with_child_resource(AwsCloudResource(api))\
                .with_child_resource(AwsCloudResource(deployment))\
                .with_child_resource(AwsCloudResource(invoke_permission))
        for queue_trigger in self.queue_triggers:
            policy, attachment, event_source_mapping = self._add_queue_trigger(function, queue_trigger)
            creation.with_child_resource(AwsCloudResource(policy))\
                .with_child_resource(AwsCloudResource(attachment))\
                .with_child_resource(AwsCloudResource(event_source_mapping))
        return creation
