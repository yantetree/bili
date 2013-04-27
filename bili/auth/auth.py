import pickle

from bili.models import User
from bili.filters import check_user
from sqlalchemy.orm.exc import NoResultFound
from tornado import httpserver, ioloop, web, options

__all__ = ['get_user', 'is_login', 'login', 'register', 'logout']

#class AuthBaseHandler(web.RequestHandler):
#    def get_curr_user(self):

def get_user(handler):
    '''
    Get current login user
    '''
    # Because session is implemented by decorator,
    # we cannot check session implementation in another decorator.
    #assert hasattr(handler, 'session'), \
    #        "Should implement session extension first"
    assert hasattr(handler.application, 'db'), \
            "Should implement database api first"
    assert hasattr(handler.application, 'store'), \
            "Should implement store api first"
    try:
        return handler.session['user']
    except KeyError or NoResultFound:
        return None

def is_login(handler):
    '''
    Check whether the current request has been logined
    '''
    if get_user(handler):
        return True
    else:
        return False

def login(handler, account, password):
    '''
    Try login and set the login session,
    both username and email can be regarded as the account.
    '''
    if not account or not password:
        return None
    try:
        user = handler.application.db.query(User).filter_by(username=account, 
                password=User.encrypt(password)).one()
    except NoResultFound:
        try:
            user = handler.application.db.query(User).filter_by(email=account, 
                    password=User.encrypt(password)).one()
        except:
            return None
    handler.session.set('user', user)
    return user

def logout(handler):
    handler.session.delete('user')

def register(handler, username, email, password):
    '''
    Register new user.
    The register method is not responsible for the form validation.
    You should check the existence and other stuff in your form module.
    '''
    user = User(username, email, password)
    handler.application.db.add(user)
    handler.application.db.commit()
    return user

