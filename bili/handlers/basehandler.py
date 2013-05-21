from tornado.web import RequestHandler
from bili.auth import get_user

class BaseRequestHandler(RequestHandler):
    '''
    Base request, add some authentication feature
    '''
    def get_current_user(self):
        return get_user(self)
