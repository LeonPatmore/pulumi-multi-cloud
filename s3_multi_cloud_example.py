import pulumi
from pulumi import AssetArchive, FileArchive

from pulumi_multi_cloud.common import CloudProvider, CloudRegion, MultiCloudResourceFactory
from pulumi_multi_cloud.resources.bucket import MultiCloudBucketType
from pulumi_multi_cloud.resources.function import FunctionRuntime, MultiCloudFunctionType
from pulumi_multi_cloud.resources.permissions import MultiCloudPermissionsType

code = AssetArchive({".": FileArchive("./example")})


def my_cool_exposed_function(gen: MultiCloudResourceFactory):
    bucket = gen.create(MultiCloudBucketType, "leon-multicloud")
    permissions = gen.create(MultiCloudPermissionsType, name="function-permissions")
    function = gen.create(MultiCloudFunctionType,
                          "leon-function",
                          runtime=FunctionRuntime.Python39,
                          files=code,
                          permissions=permissions)
    pulumi.export(f"bucket_id_{gen.provider.name}", bucket.get_id())
    pulumi.export(f"function_id_{gen.provider.name}", function.get_id())


my_cool_exposed_function(MultiCloudResourceFactory(region=CloudRegion.EU, provider=CloudProvider.AWS))
my_cool_exposed_function(MultiCloudResourceFactory(region=CloudRegion.EU, provider=CloudProvider.GCP))

