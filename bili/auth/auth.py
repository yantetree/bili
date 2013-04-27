import pickle

from tornado import httpserver, ioloop, web, options
from sqlalchemy.orm.exc import NoResultFound
from bili.models import User

__all__ = ['get_user', 'login', 'register', 'logout']

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
        user = handler.session['user']
    except KeyError or NoResultFound:
        return None

def login(handler, account, password):
    '''
    Try login and set the login session,
    both username and email can be regarded as the account.
    '''
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

def logout(handler):
    handler.session.delete('user')
