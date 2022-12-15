import sys
sys.path.append('../..')

from pulumi import AssetArchive, FileArchive

from pulumi_multi_cloud.resources.function import FunctionRuntime, FunctionHandler, FunctionQueueTrigger

import pulumi

from pulumi_multi_cloud.multi_cloud_generator import multi_cloud_generator
from pulumi_multi_cloud.common import MultiCloudResourceFactory, CloudRegion, CloudProvider
from pulumi_multi_cloud.resources.types import DefaultTypes


number_function_code = AssetArchive({".": FileArchive("number_function")})


@multi_cloud_generator(gens=[MultiCloudResourceFactory(region=CloudRegion.EU, provider=CloudProvider.AWS)])
def my_bucket(gen: MultiCloudResourceFactory):
    queue = gen.create(DefaultTypes.Queue.value, "test_queue")
    pulumi.export("queue_id", queue.get_id())

    permissions = gen.create(DefaultTypes.Permissions.value, name="function-permissions")
    function = gen.create(DefaultTypes.Function.value,
                          "number-function",
                          runtime=FunctionRuntime.Python39,
                          files=number_function_code,
                          function_handler=FunctionHandler(),
                          permissions=permissions,
                          queue_triggers=[FunctionQueueTrigger("sqs", queue)])
    pulumi.export(f"number_function_id_{gen.provider.name}", function.get_id())
