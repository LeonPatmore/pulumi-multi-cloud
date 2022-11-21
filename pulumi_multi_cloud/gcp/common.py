from pulumi_multi_cloud.resources.resource import MultiCloudResource


class GcpCloudResource(MultiCloudResource):

    def get_id(self) -> str:
        return self.resource.name
