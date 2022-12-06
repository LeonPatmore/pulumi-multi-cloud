class HttpRequest:

    def __init__(self, body: str):
        self.body = body


class HttpResponse:

    def __init__(self):
        pass


class ProviderHandler:

    def supports(self, **kwargs) -> bool:
        raise NotImplementedError

    def generate_request(self, **kwargs) -> HttpRequest:
        raise NotImplementedError
