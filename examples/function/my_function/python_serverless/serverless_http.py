class HttpRequest:

    def __init__(self, body: str):
        self.body = body


class HttpResponse:

    def __init__(self, status: int, body: str):
        self.status = status
        self.body = body


class ProviderHttpHandler:

    def supports(self, **kwargs) -> bool:
        raise NotImplementedError

    def generate_request(self, **kwargs) -> HttpRequest:
        raise NotImplementedError

    def convert_to_response(self, response: HttpResponse):
        raise NotImplementedError
