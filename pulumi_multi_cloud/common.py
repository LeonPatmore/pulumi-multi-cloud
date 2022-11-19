import enum
import logging

from pulumi_multi_cloud.aws.common import AwsCloudResource
from pulumi_multi_cloud.gcp.common import GcpCloudResource


class CloudRegion(enum.Enum):

    EU = "eu"
    US = "us"


class CloudProvider(enum.Enum):

    AWS = "aws"
    GCP = "gcp"


DEFAULT_REGION = CloudRegion.EU
DEFAULT_PROVIDER = CloudProvider.AWS


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

    def __init__(self,
                 region: CloudRegion = DEFAULT_REGION,
                 provider: CloudProvider = DEFAULT_PROVIDER):
        self.region = region
        self.provider = provider

    def create(self,
               resource_type: type(MultiCloudResourceType),
               name: str,
               **kwargs):
        p_class = resource_type.gcp_type if self.provider == CloudProvider.GCP else resource_type.aws_type
        if p_class is None:
            logging.info(f"Skipping this resource [ {name} ] of type [ {resource_type} ] "
                         f"because there no abstraction for provider [ {self.provider.name} ]")
            return None
        resource_factory = resource_type(name=name, region=self.region, **kwargs)
        props = resource_factory.gcp_kwargs if self.provider == CloudProvider.GCP else resource_factory.aws_kwargs

        pulumi_resource = p_class(resource_name=name, **props())
        pulumi_resource.__class__ = resource_type.gcp_multi_cloud_type \
            if self.provider == CloudProvider.GCP \
            else resource_type.aws_multi_cloud_type
        return pulumi_resource
