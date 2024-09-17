import threading
import uuid

from rest_framework.request import Request
from rest_framework.response import Response

from common.services.redis import get_value_from_redis
from users.models import WebSiteVisitor
from datetime import datetime

current_date = datetime.now().strftime("%Y-%m-%d")


def calculate_site_visitors(request, visitor_id):
    user_agent = request.META.get('HTTP_USER_AGENT')
    username = request.META.get('USERNAME')

    if added_date := get_value_from_redis(visitor_id):
        print(added_date)
        print(current_date)
        if added_date == current_date:
            return None
        print('visitors!!!')
    WebSiteVisitor.objects.create(visitor_id=visitor_id, username=username, user_agent=user_agent)


def visitor_web_site(request: Request, response: Response):
    cookies = request.COOKIES
    visitor_id = cookies.get('visitor_id')

    if not visitor_id:
        print("new visitors")
        visitor_id = str(uuid.uuid4())
        response.set_cookie(key="visitor_id", value=visitor_id, httponly=True, samesite=None, secure=True)

    threading.Thread(target=calculate_site_visitors, args=[request, visitor_id]).start()
    return response
