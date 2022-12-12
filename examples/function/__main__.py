import sys
sys.path.append('../..')
import pulumi
from pulumi import AssetArchive, FileArchive

from pulumi_multi_cloud.common import CloudProvider, CloudRegion, MultiCloudResourceFactory
from pulumi_multi_cloud.resources.function import FunctionHandler, FunctionRuntime, FunctionHttpTrigger
from pulumi_multi_cloud.resources.types import DefaultTypes
from pulumi_multi_cloud.azure.common import AzureResourceFactory
from pulumi_multi_cloud.azure.resource_group import azure_resource_group

code = AssetArchive({".": FileArchive("my_function")})


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


my_cool_exposed_function(MultiCloudResourceFactory(region=CloudRegion.EU, provider=CloudProvider.AWS))
my_cool_exposed_function(MultiCloudResourceFactory(region=CloudRegion.EU, provider=CloudProvider.GCP))
# my_cool_exposed_function(AzureResourceFactory(azure_resource_group("function-example"), region=CloudRegion.EU))
