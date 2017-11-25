# -*- coding: utf-8 -*-
from django.conf.urls import url

from account.views import *

urlpatterns = [
    url(r'^sign_up/$', sign_up, name="sign_up"),
    url(r'^get_sign_up_token/$', sign_up_token, name="sign_up"),
    url(r'^sign_in/$', sign_in, name="login"),
    url(r'^sign_out/$', sign_out, name="logout"),
    url(r'^reset_password/$', reset_password, name="reset_password"),
    url(r'^get_reset_password_token/$', reset_password_token, name="reset_password_token"),
    url(r'^change_password/$', change_password, name="change_password"),
    url(r'^get_user_info/$', user_info, name="get_user_info"),

    url(r'^user/$', get_user),
]
