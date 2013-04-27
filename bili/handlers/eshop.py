# -*- coding:utf-8 -*-
'''
Eshop modules.
TMall and Amazon-cn support implemented
'''

from bili.auth.decorators import login_required
from bili.eparser import get_parser, QueryError, PARSERS_DICT
from bili.utils.session import session
from tornado import web, gen
from tornado.httpclient import AsyncHTTPClient, HTTPRequest

__all__ = ['GetPrice',]

class GetPrice(web.RequestHandler):
    @session
    @login_required
    @web.asynchronous
    @gen.coroutine
    def get(self):
        context = {'status' : 200}
        data = {'errors': []}
        context['data'] = data
        try:
            keyword = self.get_argument('k')
        except web.HTTPError:
            data['success'] = False
            data['errors'].append(u'关键词不能为空')
        ename = None
        for key in PARSERS_DICT.keys():
            try:
                self.get_argument(key)
            except:
                pass
            else:
                ename = key
                break
        parser_cls = get_parser(ename)
        parser = parser_cls()
        headers = parser_cls.DEFAULT_HEADERS
        # The `follow_redirects` arguments must be true,
        # and the max_redirects must be larger then 0(default to 0),
        # or the SimpleHTTPClient will return a HTTPError if 3xx status code comes.
        request = HTTPRequest(parser.make_url(keyword), headers=headers, 
                follow_redirects=True, max_redirects=20)
        #AsyncHTTPClient.configure('tornado.curl_httpclient.CurlAsyncHTTPClient')
        client = AsyncHTTPClient()
        response = yield client.fetch(request)
        value = parser.parse(response.body)
        data['success'] = True
        data.update({ename : {'value': value}})

        self.write(context)
