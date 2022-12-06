from lib.serverless import HttpRequest
from lib.serverless_function import serverless_function


@serverless_function
def function_example(request: HttpRequest):
    return request.body


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
    assert "hello" == function_example(event=event, context=context)
