'''
Add session support to tornado
'''
import base64
import pickle 
import M2Crypto

from store import RedisStore
from time import time


__all__ = ['Session', 'session']

class Session(dict):
    '''
    Dictionary-like session implementation
    '''
    def __init__(self, session_id, max_age=7200):
        self.session_id = session_id
        self.start_time = time()
        self.max_age = max_age

    def set(self, k, v):
        self.__setitem__(k, v)

    def delete(self, *keys):
        for k in keys:
            self.__delitem__(k)

def gen_session_id(num_bytes=16):
    '''
    Generate a random session id
    '''
    return base64.b64encode(M2Crypto.m2.rand_bytes(num_bytes))


def session(func):
    '''
    Add session attribute to the handler before the request begins.
    And save it to the store when request ends.
    NOTE:
        this decorator should always be at top of other decorators which
        use session(because of the decorator implementation.
    '''
    def wrapper(handler, *args, **kwargs):
        session_id = handler.get_secure_cookie("session_id")
        if not session_id:
            handler.set_secure_cookie("session_id", gen_session_id())
            session_id = handler.get_secure_cookie("session_id")

        _session = None
        raw_session = handler.application.store.get(session_id)
        if raw_session:
            _session = pickle.loads(raw_session)
            if _session.max_age < time() - _session.start_time:
                # Expire the session
                handler.application.store.delete(session_id)
                _session = None

        if not _session:
            _session = Session(session_id)

        setattr(handler, 'session', _session)

        res = func(handler, *args, **kwargs)

        handler.application.store.set(session_id, pickle.dumps(_session))
        return res
    return wrapper
