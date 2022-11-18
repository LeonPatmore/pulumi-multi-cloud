from pulumi_aws import s3
from pulumi_gcp.storage import bucket

from pulumi_multi_cloud.common import MultiCloudResourceType


class MultiCloudBucketType(MultiCloudResourceType):

    aws_type = s3.Bucket
    gcp_type = bucket.Bucket

    def gcp_kwargs(self) -> dict:
        return {
            "location": self.region.name
        }
