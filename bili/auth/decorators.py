from bili.auth.auth import *
from tornado.web import HTTPError

def login_required(func):
    '''
    Decorator for checking whether the request has been already logined
    '''
    def wrapper(handler, *args, **kwargs):
        user = get_user(handler)
        print user
        if not user:
            handler.request.headers
            handler.send_error(403)
        else:
            setattr(handler, 'user', user)
            return func(handler, *args, **kwargs)
    return wrapper

