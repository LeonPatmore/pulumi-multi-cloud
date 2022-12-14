from pulumi_aws import iam
from pulumi_aws.iam import Role

from pulumi_multi_cloud.aws.common import AwsCloudResource
from pulumi_multi_cloud.common import ProviderCloudResourceGenerator
from pulumi_multi_cloud.resources.resource import MultiCloudResource


class AwsPermissionsGenerator(ProviderCloudResourceGenerator):

    def generate_resources(self) -> MultiCloudResource:
        role = Role(self.name, assume_role_policy=iam.get_policy_document(statements=[
            iam.GetPolicyDocumentStatementArgs(
                actions=["sts:AssumeRole"],
                principals=[iam.GetPolicyDocumentStatementPrincipalArgs(identifiers=["lambda.amazonaws.com"],
                                                                        type="Service")]
            )
        ]).json)
        return AwsCloudResource(role)
