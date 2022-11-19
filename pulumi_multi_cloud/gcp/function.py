import pulumi
from pulumi_gcp import storage
from pulumi_gcp.cloudfunctions import Function, FunctionIamMember

from pulumi_multi_cloud.gcp.common import GcpCloudResource
from pulumi_multi_cloud.resources.function import FunctionRuntime, ProviderFunctionResourceGenerator, \
    MultiCloudFunctionCreation

GCP_RUNTIME = {
    FunctionRuntime.Python39: "python39"
}


class GcpFunctionCreation(MultiCloudFunctionCreation):

    def http_url(self) -> pulumi.Output[str]:
        return self.main_resource.https_trigger_url


class GcpFunctionGenerator(ProviderFunctionResourceGenerator):

    def _upload_gcp_code(self) -> tuple:
        bucket = storage.Bucket(f"{self.name}-code", location=self.region.name)
        code_object = storage.BucketObject("python-zip", bucket=bucket.name, source=self.files)
        return bucket, code_object

    def generate_resources(self) -> MultiCloudFunctionCreation:
        bucket, code_object = self._upload_gcp_code()
        function = Function(self.name,
                            runtime=GCP_RUNTIME[self.runtime],
                            entry_point=self.function_handler.method,
                            source_archive_bucket=bucket.name,
                            source_archive_object=code_object.name,
                            trigger_http=self.http_trigger is not None,
                            region="europe-west2")
        creation = GcpFunctionCreation(GcpCloudResource.given(function))\
            .with_resource(GcpCloudResource.given(bucket))\
            .with_resource(GcpCloudResource.given(code_object))

        if self.http_trigger is not None and self.http_trigger.public:
            iam = FunctionIamMember("public",
                                    project=function.project,
                                    cloud_function=function.name,
                                    region="europe-west2",
                                    role="roles/cloudfunctions.invoker",
                                    member="allUsers")
            creation.with_resource(GcpCloudResource.given(iam))
        return creation
