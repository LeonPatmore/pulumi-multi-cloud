from pulumi_multi_cloud.common import CloudProvider, MultiCloudResourceFactory, CloudRegion
from pulumi_multi_cloud.resources.bucket import MultiCloudBucket

factory = MultiCloudResourceFactory(default_region=CloudRegion.EU, default_provider=CloudProvider.AWS)

factory.create(MultiCloudBucket, "leon-multicloud")
factory.create(MultiCloudBucket, "leon-multicloud", provider=CloudProvider.GCP)
