# -*- coding:utf-8 -*-
'''
eshop parser
'''
from pyquery import PyQuery

#from crawer import Crawer

import urllib

__all__ = ['TmallParser', 'AmazonParser', 'get_parser', 'QueryException']


class QueryException(Exception):
    '''
    Raised when query failed
    '''
    pass

class BaseParser(object):
    '''
    Base parser
    '''



    def parse(self, name):
        '''
        Should be implemented
        '''
        pass

    @staticmethod
    def to_gbk(origin_str):
        '''
        encode the string in gbk charset
        '''
#        try:
#            # avoid the string is not in unicode
#            origin_str = origin_str.decode('utf8')
#        except Exception:
#            pass
        return origin_str.encode('gbk')


    @staticmethod
    def clean_price(price):
        '''
        return the clean price
        '''
        return price.strip(u' $¥￥')



class TmallParser(BaseParser):
    '''
    Parser for tmall
    '''
    HOST = 'http://list.tmall.com'
    SUFFIX = '/search_product.htm?q={q}&s={s}&sort=p'

    # The pyquery parse pattern
    PATTERN = '.product-iWrap .productPrice em'
    def __init__(self):
        self.host = TmallParser.HOST

    def parse(self, name):
        name = urllib.quote(BaseParser.to_gbk(name))
        url = self.host + TmallParser.SUFFIX.format(q=name, s=0)

        try:
            dom = PyQuery(url=url)
        except Exception as e:
            raise QueryException(e.message)
        return BaseParser.clean_price(dom(TmallParser.PATTERN)[0].text)


class AmazonParser(BaseParser):
    '''
    Parser for amazon.cn
    '''
    HOST = 'http://www.amazon.cn'
    SUFFIX = '/s?ie=UTF8&page=1&rh=i%3Aaps%2Ck%3A{q}'
    #SUFFIX = '/mn/search/ajax/ref=nb_sb_noss?field-keywords={q}'

    DEFAULT_HEADERS = [
            ('Host', 'www.amazon.cn'),
            ('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) \
                    AppleWebKit/537.17 (KHTML, like Gecko)  \
                    Chrome/24.0.1312.56 Safari/537.17'),
            ]

    PATTERN = '#result_0 .newPrice span'

    def __init__(self):
        self.host = AmazonParser.HOST

    def parse(self, name):
        url = self.host + AmazonParser.SUFFIX.format(q=name.encode('utf8'))
        opener = urllib.URLopener()
        for key, value in AmazonParser.DEFAULT_HEADERS:
            opener.addheader(key, value)

        try:
            dom = PyQuery(url=url, opener=opener.open)
        except Exception as e:
            raise QueryException(e.message)
        return BaseParser.clean_price(dom(AmazonParser.PATTERN)[0].text)

_PARSERS_DICT = {
        'tmall'     :   TmallParser, 
        'amazon'    :   AmazonParser,
}

def get_parser(name):
    return _PARSERS_DICT.get(name.lower(), None)

def test():
    '''
    only for test
    '''
    tmall_parser = TmallParser()
    amazon_parser = AmazonParser()
    print tmall_parser.parse(u'嫌疑人x的獻身')
    print amazon_parser.parse(u'嫌疑人x的獻身')

if __name__ == '__main__':
    test()
