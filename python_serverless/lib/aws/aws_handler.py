from ..serverless import ProviderHandler, HttpRequest


class AwsHandler(ProviderHandler):

    def generate_request(self, **kwargs) -> HttpRequest:
        event = kwargs["event"]
        return HttpRequest(event["body"])

    def supports(self, **kwargs) -> bool:
        return "event" in kwargs and "context" in kwargs
