# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.sessions.middleware import SessionMiddleware


class CustomSessionMiddleware(SessionMiddleware):
    def process_request(self, request):
        sessionid = request.GET.get("sessionid", "")
        session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME) or sessionid
        request.session = self.SessionStore(session_key)
