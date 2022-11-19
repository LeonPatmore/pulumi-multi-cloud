from pulumi_multi_cloud.aws.permissions import AwsPermissionsGenerator
from pulumi_multi_cloud.common import MultiCloudResourceType, CloudProvider

MULTI_CLOUD_PERMISSIONS_TYPE = MultiCloudResourceType({
    CloudProvider.AWS: AwsPermissionsGenerator
})
