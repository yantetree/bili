#-*- coding=utf-8 -*-
from bili.auth.decorators import login_required
from bili.utils.session import session
from tornado import web

__all__ = ['HomeHandler',]

class HomeHandler(web.RequestHandler):
    @session
    @login_required
    def get(self):
        return self.render("home.html", title='比利')
