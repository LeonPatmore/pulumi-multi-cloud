import enum

from pulumi_multi_cloud.aws.bucket import AwsBucketGenerator
from pulumi_multi_cloud.aws.function import AwsFunctionGenerator
from pulumi_multi_cloud.aws.permissions import AwsPermissionsGenerator
from pulumi_multi_cloud.common import MultiCloudResourceType, CloudProvider
from pulumi_multi_cloud.gcp.bucket import GcpBucketGenerator
from pulumi_multi_cloud.gcp.function import GcpFunctionGenerator


class DefaultTypes(enum.Enum):

    Bucket = MultiCloudResourceType({
        CloudProvider.AWS: AwsBucketGenerator,
        CloudProvider.GCP: GcpBucketGenerator
    })

    Permissions = MultiCloudResourceType({
        CloudProvider.AWS: AwsPermissionsGenerator
    })

    Function = MultiCloudResourceType({
        CloudProvider.AWS: AwsFunctionGenerator,
        CloudProvider.GCP: GcpFunctionGenerator
    })
