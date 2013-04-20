'''
Make the store system pluginable
'''

__all__ = ['RedisStore']

class BaseStore(object):
    '''
    Base class for all the store implementation
    '''
    def get(self, k, default=None):
        '''
        Find and return the given key's corresponding value, 
        or return the default value.
        SHOULD be overridden
        '''
        pass

    def set(self, k, v):
        '''
        Set key-value pair
        SHOULD be overridden
        '''
        pass
    
    def delete(self, *keys):
        '''
        Delete the given key
        SHOULD be overridden
        '''
        pass

class DictStore(BaseStore):
    def __init__(self):
        self._d = dict()

    def get(self, k, default=None):
        self._d.get(k, default)

    def set(self, k, v):
        self._d[k] = v

    def delete(self, *keys):
        for k in keys:
            try:
                del self._d[k]
            except KeyError:
                pass


class RedisStore(BaseStore):
    '''
    Redis backend for the session module
    '''
    def __init__(self, redis_conn):
        self.conn = redis_conn

    def get(self, k):
        return self.conn.get(k)
    
    def set(self, k, v):
        self.conn.set(k, v)

    def delete(self, *keys):
        self.conn.delete(*keys)

