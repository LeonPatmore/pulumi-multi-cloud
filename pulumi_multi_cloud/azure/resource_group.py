from pulumi_azure_native import resources
from pulumi_azure_native.resources import ResourceGroup


def azure_resource_group(name: str) -> ResourceGroup:
    return resources.ResourceGroup(name)
