import sys
sys.path.append('../..')

import pulumi

from pulumi_multi_cloud.multi_cloud_generator import multi_cloud_generator
from pulumi_multi_cloud.common import MultiCloudResourceFactory, CloudRegion, CloudProvider
from pulumi_multi_cloud.resources.types import DefaultTypes


@multi_cloud_generator(gens=[MultiCloudResourceFactory(region=CloudRegion.EU, provider=CloudProvider.AWS),
                             MultiCloudResourceFactory(region=CloudRegion.EU, provider=CloudProvider.GCP)])
def my_bucket(gen: MultiCloudResourceFactory):
    bucket = gen.create(DefaultTypes.Bucket.value, "leon-example-2")
    pulumi.export(f"bucket_id_{gen.provider.name}", bucket.get_id())
