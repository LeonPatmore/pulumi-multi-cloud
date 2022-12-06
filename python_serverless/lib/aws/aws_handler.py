from ..serverless_http import ProviderHttpHandler, HttpRequest, HttpResponse


class AwsHandler(ProviderHttpHandler):

    def generate_request(self, **kwargs) -> HttpRequest:
        event = kwargs["event"]
        return HttpRequest(event["body"])

    def convert_to_response(self, response: HttpResponse):
        return {
            "isBase64Encoded": True,
            "statusCode": response.status,
            "body": response.body
        }

    def supports(self, **kwargs) -> bool:
        return "event" in kwargs and "context" in kwargs
