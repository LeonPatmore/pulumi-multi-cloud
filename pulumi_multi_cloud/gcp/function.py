import pulumi
from pulumi_gcp import storage
from pulumi_gcp.cloudfunctions import Function, FunctionIamMember

from pulumi_multi_cloud.gcp.common import GcpCloudResource
from pulumi_multi_cloud.resources.function import FunctionRuntime, ProviderFunctionResourceGenerator, MultiCloudFunction
from pulumi_multi_cloud.resources.resource import MultiCloudResource

GCP_RUNTIME = {
    FunctionRuntime.Python39: "python39"
}


class GcpFunction(GcpCloudResource, MultiCloudFunction):

    def http_url(self) -> pulumi.Output[str]:
        return self.resource.https_trigger_url


class GcpFunctionGenerator(ProviderFunctionResourceGenerator):

    def _upload_gcp_code(self) -> tuple:
        bucket = storage.Bucket(f"{self.name}-code", location=self.region.name)
        code_object = storage.BucketObject("python-zip", bucket=bucket.name, source=self.files)
        return bucket, code_object

    def generate_resources(self) -> MultiCloudResource:
        bucket, code_object = self._upload_gcp_code()
        function = Function(self.name,
                            runtime=GCP_RUNTIME[self.runtime],
                            entry_point=self.function_handler.method,
                            source_archive_bucket=bucket.name,
                            source_archive_object=code_object.name,
                            trigger_http=self.http_trigger is not None,
                            region="europe-west2")
        creation = GcpFunction(function)\
            .with_child_resource(GcpCloudResource(bucket))\
            .with_child_resource(GcpCloudResource(code_object))

        if self.http_trigger is not None and self.http_trigger.public:
            iam = FunctionIamMember("public",
                                    project=function.project,
                                    cloud_function=function.name,
                                    region="europe-west2",
                                    role="roles/cloudfunctions.invoker",
                                    member="allUsers")
            creation.with_child_resource(GcpCloudResource(iam))
        return creation
