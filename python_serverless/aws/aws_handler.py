from python_serverless.serverless import ProviderHandler, HttpRequest


class AwsHandler(ProviderHandler):

    def generate_request(self, **kwargs) -> HttpRequest:
        pass

    def supports(self, **kwargs) -> bool:
        return "event" in kwargs and "context" in kwargs
