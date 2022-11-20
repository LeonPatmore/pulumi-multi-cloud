
def handle_aws(event, context):
    return {
        "isBase64Encoded": True,
        "statusCode": 200,
        "body": "hi there!"
    }


def handle_gcp(request):
    return "hi there!"
