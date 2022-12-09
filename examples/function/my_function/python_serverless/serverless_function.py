import functools

from python_serverless.aws.aws_handler import AwsHandler
from python_serverless.gcp.gcp_handler import GcpHandler

AWS_HANDLER = AwsHandler()
GCP_HANDLER = GcpHandler()
DEFAULT_HANDLERS = [AWS_HANDLER, GCP_HANDLER]


def serverless_function(handlers=None):
    if handlers is None:
        handlers = DEFAULT_HANDLERS

    def serverless_decorator(func: callable):
        @functools.wraps(func)
        def generic_func(**kwargs):

            for handler in handlers:
                if handler.supports(**kwargs):
                    request = handler.generate_request(**kwargs)
                    response = func(request)
                    return handler.convert_to_response(response)
            raise Exception("Not sure how to handle these kwargs: " + str(kwargs.keys()))
        return generic_func

    return serverless_decorator
