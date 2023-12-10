from rest_framework import status


class CustomApiException(Exception):

    def __init__(self, error_message, error_code=None, status=status.HTTP_400_BAD_REQUEST):
        self.error_message = error_message
        self.error_code = error_code
        self.status = status

    def __dict__(self):
        resp = {
            'error_message': self.error_message,
        }
        if self.error_code:
            resp['error_code'] = self.error_code
        return resp
