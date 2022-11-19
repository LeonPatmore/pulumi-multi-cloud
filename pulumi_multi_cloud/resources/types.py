import enum

from pulumi_multi_cloud.resources.bucket import MULTI_CLOUD_BUCKET_TYPE
from pulumi_multi_cloud.resources.permissions import MULTI_CLOUD_PERMISSIONS_TYPE


class DefaultTypes(enum.Enum):

    Bucket = MULTI_CLOUD_BUCKET_TYPE
    Permissions = MULTI_CLOUD_PERMISSIONS_TYPE
