import enum

import pulumi


class CloudRegion(enum.Enum):

    EU = "eu"
    US = "us"


class CloudProvider(enum.Enum):

    AWS = "aws"
    GCP = "gcp"


class MultiCloudResource(pulumi.CustomResource):

    gcp_type = None
    aws_type = None

    def __init__(self,
                 provider: CloudProvider,
                 region: CloudRegion,
                 name: str):
        self.region = region
        t = self.gcp_type if provider == CloudProvider.GCP else self.aws_type
        kwargs = self.gcp_kwargs if provider == CloudProvider.GCP else self.aws_kwargs
        super(MultiCloudResource, self).__init__(t, name, props=kwargs())

    def gcp_kwargs(self) -> dict:
        return {}

    def aws_kwargs(self) -> dict:
        return {}


class MultiCloudResourceFactory:

    def __init__(self, default_region: CloudRegion, default_provider: CloudProvider):
        self.default_region = default_region
        self.default_provider = default_provider

    def create(self,
               resource_type: type(MultiCloudResource),
               name: str,
               provider: CloudProvider = None,
               region: CloudRegion = None) -> MultiCloudResource:
        if provider is None:
            provider = self.default_provider
        if region is None:
            region = self.default_region
        return resource_type(name=name, provider=provider, region=region)
