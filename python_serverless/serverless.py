import os


class HttpRequest:

    def __init__(self, body: str):
        pass


class HttpResponse:

    def __init__(self):
        pass


class ProviderHandler:

    def supports(self, **kwargs) -> bool:
        raise NotImplementedError

    def generate_request(self, **kwargs) -> HttpRequest:
        raise NotImplementedError


class Serverless:

    def generic_handle(self, **kwargs):
        print(os.environ)
        self.handle(**kwargs)

    def handle(self, req: HttpRequest, res: HttpResponse):
        raise NotImplementedError()
