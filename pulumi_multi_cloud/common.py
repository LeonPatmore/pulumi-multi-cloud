import enum

import pulumi

from pulumi_multi_cloud.resources.resource import MultiCloudResource


class CloudRegion(enum.Enum):

    EU = "eu"
    US = "us"


class CloudProvider(enum.Enum):

    AWS = "aws"
    GCP = "gcp"


DEFAULT_REGION = CloudRegion.EU
DEFAULT_PROVIDER = CloudProvider.AWS


class ProviderCloudResource:

    def __init__(self, resource: pulumi.Resource, target_class: MultiCloudResource):
        self.resource = resource
        self.target_class = target_class


class ProviderCloudResourceGenerator:

    def __init__(self, name: str, region: CloudRegion):
        self.name = name
        self.region = region

    def generate_resources(self) -> list[ProviderCloudResource]:
        raise NotImplementedError()


class MultiCloudResourceType:

    def __init__(self, provider_map: dict[CloudProvider, type[ProviderCloudResourceGenerator]]):
        self.provider_map = provider_map


class MultiCloudResourceCreation:

    def __init__(self,
                 main_resource: MultiCloudResource or None,
                 secondary_resources: list[MultiCloudResource] = None):
        if secondary_resources is None:
            secondary_resources = []
        self.main_resource = main_resource
        self.secondary_resources = secondary_resources


class MultiCloudResourceFactory:

    def __init__(self,
                 region: CloudRegion = DEFAULT_REGION,
                 provider: CloudProvider = DEFAULT_PROVIDER):
        self.region = region
        self.provider = provider

    def create(self, resource_type: MultiCloudResourceType, name: str, **kwargs) -> MultiCloudResourceCreation:
        provider_resource_generator = resource_type.provider_map.get(self.provider)
        if provider_resource_generator is None:
            return MultiCloudResourceCreation(None)
        provider_resources = provider_resource_generator(name, self.region, **kwargs).generate_resources()
        for provider_response in provider_resources:
            if provider_response is None:
                continue
            provider_response.resource.__class__ = provider_response.target_class
        main_resource = provider_resources[0].resource if len(provider_resources) > 0 else None
        return MultiCloudResourceCreation(main_resource, [x.resource for x in provider_resources[1:]])
