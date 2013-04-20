from tornado import web
from bili.utils.session import session

__all__ = ['HomeHandler',]

class HomeHandler(web.RequestHandler):
    @session
    def get(self):
        return self.render("home.html", title='Home')

