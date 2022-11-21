from pulumi_aws import iam
from pulumi_aws.iam import Role

from pulumi_multi_cloud.aws.common import AwsCloudResource
from pulumi_multi_cloud.common import ProviderCloudResourceGenerator, MultiCloudResourceCreation


class AwsPermissionsGenerator(ProviderCloudResourceGenerator):

    def generate_resources(self) -> MultiCloudResourceCreation:
        role = Role(self.name, assume_role_policy=iam.get_policy_document(statements=[
            iam.GetPolicyDocumentStatementArgs(
                actions=["sts:AssumeRole"],
                principals=[iam.GetPolicyDocumentStatementPrincipalArgs(identifiers=["lambda.amazonaws.com"],
                                                                        type="Service")]
            )
        ]).json)
        return MultiCloudResourceCreation(AwsCloudResource(role))
