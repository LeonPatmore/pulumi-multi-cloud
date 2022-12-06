from lib.aws.aws_handler import AwsHandler

AWS_HANDLER = AwsHandler()


def serverless_function(func: callable):

    def generic_func(**kwargs):
        request = AWS_HANDLER.generate_request(**kwargs)
        return func(request)

    return generic_func
