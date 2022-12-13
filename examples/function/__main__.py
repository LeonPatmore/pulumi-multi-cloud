import sys
sys.path.append('../..')
import pulumi
from pulumi import AssetArchive, FileArchive

from pulumi_multi_cloud.common import CloudProvider, CloudRegion, MultiCloudResourceFactory
from pulumi_multi_cloud.resources.function import FunctionHandler, FunctionRuntime, FunctionHttpTrigger
from pulumi_multi_cloud.resources.types import DefaultTypes
from pulumi_multi_cloud.multi_cloud_generator import multi_cloud_generator

code = AssetArchive({".": FileArchive("my_function")})


@multi_cloud_generator(gens=[MultiCloudResourceFactory(region=CloudRegion.EU, provider=CloudProvider.AWS),
                             MultiCloudResourceFactory(region=CloudRegion.EU, provider=CloudProvider.GCP)])
def my_cool_exposed_function(gen: MultiCloudResourceFactory):
    permissions = gen.create(DefaultTypes.Permissions.value, name="function-permissions").main_resource
    function_handler = FunctionHandler()
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
