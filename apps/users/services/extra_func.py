from rest_framework.exceptions import APIException
from rest_framework.request import Request


def auth_check(request):
    auth_check = request.headers.get('authorization')
    if not auth_check:
        raise APIException(detail='Токен аутентификации отсутствует в заголовках!')


class RESTException(APIException):

    def __init__(self, status_code=400, detail=None, code=None, **kwargs):
        super().__init__(detail, code)
        self.status_code = status_code
        if not detail:
            self.detail = kwargs


def get_user_by_request(request: Request):
    cookies = request.COOKIES
    visitor_id = cookies.get('visitor_id')
    user_id = request.user.id
    return visitor_id, user_id
