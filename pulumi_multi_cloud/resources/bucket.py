from pulumi_multi_cloud.aws.bucket import AwsBucketGenerator
from pulumi_multi_cloud.common import MultiCloudResourceType, CloudProvider
from pulumi_multi_cloud.gcp.bucket import GcpBucketGenerator

MULTI_CLOUD_BUCKET_TYPE = MultiCloudResourceType({
    CloudProvider.AWS: AwsBucketGenerator,
    CloudProvider.GCP: GcpBucketGenerator
})
