from pulumi_multi_cloud.common import MultiCloudResourceFactory


def multi_cloud_generator(gens: list[MultiCloudResourceFactory]):

    def decorator_multi_cloud_generator(func: callable):
        for gen in gens:
            func(gen)
        return None

    return decorator_multi_cloud_generator
