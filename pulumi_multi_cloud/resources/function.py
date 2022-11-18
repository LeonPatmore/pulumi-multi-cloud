import enum

from pulumi import Archive
from pulumi_aws import lambda_
from pulumi_gcp import cloudfunctions, storage

from pulumi_multi_cloud.common import CloudRegion, MultiCloudResourceType
from pulumi_multi_cloud.resources.resource import MultiCloudResource


class FunctionRuntime(enum.Enum):

    Python39 = enum.auto()


GCP_RUNTIME = {
    FunctionRuntime.Python39: "python39"
}

AWS_RUNTIME = {
    FunctionRuntime.Python39: "python3.9"
}


class MultiCloudFunctionType(MultiCloudResourceType):

    aws_type = lambda_.function.Function
    gcp_type = cloudfunctions.Function

    def __init__(self,
                 region: CloudRegion,
                 name: str,
                 runtime: FunctionRuntime,
                 files: Archive,
                 permissions: MultiCloudResource):
        super().__init__(region, name)
        self.permissions = permissions
        self.runtime = runtime
        self.files = files

    def aws_kwargs(self) -> dict:
        return {
            "code": self.files,
            "runtime": AWS_RUNTIME[self.runtime],
            "handler": f"main.handle",
            "role": self.permissions.arn
        }

    def _upload_gcp_code(self) -> tuple:
        bucket = storage.Bucket(f"{self.name}-code", location=self.region.name)
        code_object = storage.BucketObject("python-zip", bucket=bucket.name, source=self.files)
        return bucket, code_object

    def gcp_kwargs(self) -> dict:
        bucket, code_object = self._upload_gcp_code()
        return {
            "runtime": GCP_RUNTIME[self.runtime],
            "entry_point": "handle",
            "source_archive_bucket": bucket.name,
            "source_archive_object": code_object.name,
            "trigger_http": True,
            "region": "europe-west2"
        }
