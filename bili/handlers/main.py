#-*- coding=utf-8 -*-
from bili.auth.decorators import login_required
from bili.auth import get_user
from bili.handlers.basehandler import BaseRequestHandler
from bili.utils.session import session
from tornado import web

__all__ = ['HomeHandler',]

class HomeHandler(BaseRequestHandler):
    @session
    @login_required
    def get(self):
        user = get_user(self)
        return self.render("home.html", title='比利', request=self)
