from pulumi_aws import iam
from pulumi_aws.iam import Role

from pulumi_multi_cloud.common import MultiCloudResourceType


class MultiCloudPermissionsType(MultiCloudResourceType):

    aws_type = Role

    def aws_kwargs(self) -> dict:
        return {
            "assume_role_policy": iam.get_policy_document(
                statements=[iam.GetPolicyDocumentStatementArgs(
                    actions=["sts:AssumeRole"],
                    principals=[iam.GetPolicyDocumentStatementPrincipalArgs(
                        identifiers=["lambda.amazonaws.com"],
                        type="Service",
                    )]
                )]).json
        }
