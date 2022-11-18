import enum

from pulumi_multi_cloud.aws.common import AwsCloudResource
from pulumi_multi_cloud.gcp.common import GcpCloudResource


class CloudRegion(enum.Enum):

    EU = "eu"
    US = "us"


class CloudProvider(enum.Enum):

    AWS = "aws"
    GCP = "gcp"


class MultiCloudResourceType:

    gcp_type = None
    gcp_multi_cloud_type = GcpCloudResource
    aws_type = None
    aws_multi_cloud_type = AwsCloudResource

    def __init__(self, region: CloudRegion, name: str):
        self.region = region
        self.name = name

    def gcp_kwargs(self) -> dict:
        return {}

    def aws_kwargs(self) -> dict:
        return {}


class MultiCloudResourceFactory:

    def __init__(self, default_region: CloudRegion, default_provider: CloudProvider):
        self.default_region = default_region
        self.default_provider = default_provider

    def create(self,
               resource_type: type(MultiCloudResourceType),
               name: str,
               provider: CloudProvider = None,
               region: CloudRegion = None,
               **kwargs):
        if provider is None:
            provider = self.default_provider
        if region is None:
            region = self.default_region

        p_class = resource_type.gcp_type if provider == CloudProvider.GCP else resource_type.aws_type
        resource_factory = resource_type(name=name, region=region, **kwargs)
        props = resource_factory.gcp_kwargs if provider == CloudProvider.GCP else resource_factory.aws_kwargs

        pulumi_resource = p_class(resource_name=name, **props())
        pulumi_resource.__class__ = resource_type.gcp_multi_cloud_type \
            if provider == CloudProvider.GCP \
            else resource_type.aws_multi_cloud_type
        return pulumi_resource
