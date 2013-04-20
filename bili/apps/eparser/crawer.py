'''
Crawer
'''
import httplib
import urllib


class Crawer(object):
    '''
    Generic crawer, should be pluginable
    '''
    DEFAULT_HEADERS = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.17 \
                    (KHTML, like Gecko) Chrome/24.0.1312.56 Safari/537.17',
    }
    def __init__(self, host):
        self.host = host
        self.conn = httplib.HTTPConnection(host, timeout=5)
        self.conn.connect()
        self.headers = Crawer.DEFAULT_HEADERS

    def set_header(self, headers):
        self.headers = headers

    def do_get(self, url):
        self.conn.request('GET', url, headers=self.headers)
        return self.conn.getresponse()
        # return res.status, res.read()
