import sys

import pulumi
from pulumi_aws import s3

sys.path.append('../..')

from pulumi_multi_cloud.azure.resource_group import azure_resource_group
from pulumi_multi_cloud.common import CloudRegion, MultiCloudResourceFactory
from pulumi_multi_cloud.resources.types import DefaultTypes

# resource_group = azure_resource_group("storage-example")
# gen = AzureResourceFactory(resource_group, region=CloudRegion.EU)
gen = MultiCloudResourceFactory()

bucket = gen.create(DefaultTypes.Bucket.value, "leon-example-2")

bucket2 = s3.Bucket("leon-example-3")

final_resource = bucket.main_resource
output_generic = final_resource.bucket_domain_name
print(type(output_generic))
pulumi.export("bucket_id", output_generic)
