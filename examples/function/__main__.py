import sys
sys.path.append('../..')
import pulumi
from pulumi import AssetArchive, FileArchive

from pulumi_multi_cloud.common import CloudProvider, CloudRegion, MultiCloudResourceFactory
from pulumi_multi_cloud.resources.function import FunctionHandler, FunctionRuntime, FunctionHttpTrigger
from pulumi_multi_cloud.resources.types import DefaultTypes

code = AssetArchive({".": FileArchive("../../example")})


def my_cool_exposed_function(gen: MultiCloudResourceFactory):
    permissions = gen.create(DefaultTypes.Permissions.value, name="function-permissions").main_resource
    function_handler = FunctionHandler(method="handle_aws" if gen.provider == CloudProvider.AWS else "handle_gcp")
    function_trigger = FunctionHttpTrigger(public=True)
    function = gen.create(DefaultTypes.Function.value,
                          "leon-function",
                          runtime=FunctionRuntime.Python39,
                          files=code,
                          function_handler=function_handler,
                          permissions=permissions,
                          http_trigger=function_trigger)

    pulumi.export(f"function_id_{gen.provider.name}", function.main_resource.get_id())
    pulumi.export(f"function_url_{gen.provider.name}", function.http_url())


my_cool_exposed_function(MultiCloudResourceFactory(region=CloudRegion.EU, provider=CloudProvider.AWS))
my_cool_exposed_function(MultiCloudResourceFactory(region=CloudRegion.EU, provider=CloudProvider.GCP))