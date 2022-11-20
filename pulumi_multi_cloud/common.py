import enum

from pulumi_multi_cloud.resources.resource import MultiCloudResource


class CloudRegion(enum.Enum):

    EU = "eu"
    US = "us"


class CloudProvider(enum.Enum):

    AWS = enum.auto()
    GCP = enum.auto()
    AZURE = enum.auto()


DEFAULT_REGION = CloudRegion.EU
DEFAULT_PROVIDER = CloudProvider.AWS


class MultiCloudResourceCreation:

    def __init__(self,
                 main_resource: MultiCloudResource,
                 secondary_resources: list[type(MultiCloudResource)] = None):
        if secondary_resources is None:
            secondary_resources = []
        self.main_resource = main_resource
        self.secondary_resources = secondary_resources

    def with_resource(self, resource: MultiCloudResource):
        if self.secondary_resources is None:
            self.secondary_resources = []
        self.secondary_resources.append(resource)
        return self


class ProviderCloudResourceGenerator:

    def __init__(self, name: str, region: CloudRegion):
        self.name = name
        self.region = region

    def generate_resources(self) -> MultiCloudResourceCreation:
        raise NotImplementedError()


class MultiCloudResourceType:

    def __init__(self, provider_map: dict[CloudProvider, type(ProviderCloudResourceGenerator)]):
        self.provider_map = provider_map


class MultiCloudResourceFactory:

    def __init__(self,
                 region: CloudRegion = DEFAULT_REGION,
                 provider: CloudProvider = DEFAULT_PROVIDER,
                 provider_global_attributes: dict = None):
        if provider_global_attributes is None:
            provider_global_attributes = {}
        self.region = region
        self.provider = provider
        self.provider_global_attributes = provider_global_attributes

    def create(self,
               resource_type: MultiCloudResourceType,
               name: str,
               fail_on_unknown: bool = True,
               **kwargs) -> type(MultiCloudResourceCreation):
        provider_resource_generator = resource_type.provider_map.get(self.provider)
        if provider_resource_generator is None:
            if fail_on_unknown:
                raise RuntimeError(f"Not sure how to generate resource [ {name} ] for provider [ {self.provider} ]")
            return MultiCloudResourceCreation(None)
        final_kwargs = kwargs | self.provider_global_attributes
        return provider_resource_generator(name, self.region, **final_kwargs).generate_resources()
