from functools import wraps

from rest_framework.response import Response
from rest_framework import status

from conf.exceptions import CustomApiException


def common_response(func):
    @wraps(func)
    def func_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except CustomApiException as e:
            return Response(e.__dict__())
        except ValueError as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data={'error_message': str(e)})
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data={'error_message': str(e)})

    return func_wrapper
