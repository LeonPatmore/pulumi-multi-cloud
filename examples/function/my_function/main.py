from python_serverless.serverless_function import serverless_function
from python_serverless.serverless_http import HttpResponse, HttpRequest


@serverless_function()
def handle(request: HttpRequest):
    return HttpResponse(status=202, body=f"hello {request.body}")
