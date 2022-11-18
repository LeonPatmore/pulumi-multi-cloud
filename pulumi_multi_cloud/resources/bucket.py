from pulumi_multi_cloud.common import MultiCloudResource


class MultiCloudBucket(MultiCloudResource):

    aws_type = "aws:s3/bucket:Bucket"
    gcp_type = "gcp:storage/bucket:Bucket"

    def gcp_kwargs(self) -> dict:
        return {
            "location": self.region.name
        }
