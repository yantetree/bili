# -*- coding:utf-8 -*-
'''
eshop parser
'''
from pyquery import PyQuery

#from crawer import Crawer

import urllib 
__all__ = ['TmallParser', 'AmazonParser', 'get_parser', 'QueryException', 
           'PARSERS_DICT']


class QueryError(Exception):
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
    PRICE_PATTERN = '.product-iWrap .productPrice em'
    HREF_PATTERN = '.product-iWrap .productImg-wrap a'
    IMG_PATTERN = '.product-iWrap .productImg-wrap a img'
    def __init__(self):
        self.host = TmallParser.HOST

    def parse(self, name):
        name = urllib.quote(BaseParser.to_gbk(name))
        url = self.host + TmallParser.SUFFIX.format(q=name, s=0)

        try:
            dom = PyQuery(url=url)
        except Exception as e:
            raise QueryError(e.message)
        return {'price':
                BaseParser.clean_price(dom(TmallParser.PRICE_PATTERN)[0].text),
                'img':
                dom(TmallParser.IMG_PATTERN)[0].attrib['data-ks-lazyload'],
                'href':
                dom(TmallParser.HREF_PATTERN)[0].attrib['href'],
        }


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

    PRICE_PATTERN = '#result_0 .newPrice span'
    IMG_PATTERN = '#result_0 .productImage img'
    HREF_PATTERN = '#result_0 .productImage a'

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
            raise QueryError(e.message)
        return {'price' : 
                BaseParser.clean_price(dom(AmazonParser.PRICE_PATTERN)[0].text),
                'img':
                dom(AmazonParser.IMG_PATTERN)[0].attrib['src'],
                'href':
                dom(AmazonParser.HREF_PATTERN)[0].attrib['href'],
               }

PARSERS_DICT = {
        'tmall'     :   TmallParser, 
        'amazon'    :   AmazonParser,
}

def get_parser(name):
    try:
        return PARSERS_DICT[name.lower()]
    except KeyError:
        raise QueryError('parser %s not found' % name)

def parse(ename, keyword):
    '''
    search the specific keyword in specific eshop
    '''
    parser = get_parser(ename)()
    return parser.parse(keyword)
