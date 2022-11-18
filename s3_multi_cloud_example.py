import pulumi
from pulumi import AssetArchive, FileArchive

from pulumi_multi_cloud.common import CloudProvider, CloudRegion, MultiCloudResourceFactory
from pulumi_multi_cloud.resources.bucket import MultiCloudBucketType
from pulumi_multi_cloud.resources.function import FunctionRuntime, MultiCloudFunctionType
from pulumi_multi_cloud.resources.permissions import MultiCloudPermissionsType

generator = MultiCloudResourceFactory(default_region=CloudRegion.EU, default_provider=CloudProvider.AWS)


aws_bucket = generator.create(MultiCloudBucketType, "leon-multicloud")
gcp_bucket = generator.create(MultiCloudBucketType, "leon-multicloud", provider=CloudProvider.GCP)

code = AssetArchive({".": FileArchive("./example")})
permissions = generator.create(MultiCloudPermissionsType, name="function-permissions")

aws_function = generator.create(MultiCloudFunctionType, "leon-function", runtime=FunctionRuntime.Python39, files=code, permissions=permissions)

gcp_function = generator.create(MultiCloudFunctionType, "leon-function", runtime=FunctionRuntime.Python39, files=code, permissions=permissions, provider=CloudProvider.GCP)

pulumi.export("aws_bucket_id", aws_bucket.get_id())
pulumi.export("gcp_bucket_id", gcp_bucket.get_id())
pulumi.export("aws_function_id", aws_function.get_id())
pulumi.export("gcp_function_id", gcp_function.get_id())
