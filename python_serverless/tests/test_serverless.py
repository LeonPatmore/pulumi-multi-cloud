from lib.serverless_http import HttpRequest, HttpResponse
from lib.serverless_function import serverless_function


@serverless_function()
def function_example(request: HttpRequest) -> HttpResponse:
    return HttpResponse(200, f"{request.body} received, looks good!")


def test_aws():
    event = {
        "resource": "/",
        "path": "/",
        "httpMethod": "GET",
        "body": "hello"
    }
    context = {
        "function_name": "name"
    }
    response = function_example(event=event, context=context)

    assert "hello received, looks good!" == response["body"]
    assert response["isBase64Encoded"]
    assert 200 == response["statusCode"]
