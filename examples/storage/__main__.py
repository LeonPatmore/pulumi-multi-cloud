import sys

import pulumi

sys.path.append('../..')

from pulumi_multi_cloud.azure.common import AzureResourceFactory
from pulumi_multi_cloud.azure.resource_group import azure_resource_group
from pulumi_multi_cloud.common import CloudRegion
from pulumi_multi_cloud.resources.types import DefaultTypes

resource_group = azure_resource_group("storage-example")
gen = AzureResourceFactory(resource_group, region=CloudRegion.EU)

bucket = gen.create(DefaultTypes.Bucket.value, "leon-example")

pulumi.export("bucket_id", bucket.main_resource.get_id())
