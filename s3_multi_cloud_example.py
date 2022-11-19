import pulumi
from pulumi import AssetArchive, FileArchive

from pulumi_multi_cloud.common import CloudProvider, CloudRegion, MultiCloudResourceFactory
from pulumi_multi_cloud.resources.function import FunctionHandler, FunctionRuntime
from pulumi_multi_cloud.resources.types import DefaultTypes

code = AssetArchive({".": FileArchive("./example")})


def my_cool_exposed_function(gen: MultiCloudResourceFactory):
    bucket = gen.create(DefaultTypes.Bucket.value, "leon-multicloud").main_resource
    permissions = gen.create(DefaultTypes.Permissions.value, name="function-permissions").main_resource
    function_handler = FunctionHandler(method="handle_aws" if gen.provider == CloudProvider.AWS else "handle_gcp")
    function = gen.create(DefaultTypes.Function.value,
                          "leon-function",
                          runtime=FunctionRuntime.Python39,
                          files=code,
                          function_handler=function_handler,
                          permissions=permissions).main_resource

    pulumi.export(f"bucket_id_{gen.provider.name}", bucket.get_id())
    pulumi.export(f"function_id_{gen.provider.name}", function.get_id())


my_cool_exposed_function(MultiCloudResourceFactory(region=CloudRegion.EU, provider=CloudProvider.AWS))
my_cool_exposed_function(MultiCloudResourceFactory(region=CloudRegion.EU, provider=CloudProvider.GCP))
