# -*- coding=utf-8 -*-
from django.contrib.auth import login, logout, authenticate 
from django.contrib.auth.models import User
from django.http import HttpResponse

from eparser import get_parser, QueryException
from utils.decorators import check_method

import simplejson as json

#@fixed_login_required
@check_method('GET')
def get_price(request, ename):
    '''
    search the price in the specific eshop
    '''
    context = {'status' : 200}
    data = {'errors': []}
    context['data'] = data
    parser = get_parser(ename)()
    keyword = request.GET.get('k', None)
    if not parser or not keyword:
        data['success'] = False
        data['errors'].append(u'参数错误')
    else:
        try:
            price = parser.parse(keyword)
        except QueryException:
            data['success'] = False
            data['errors'].append(u'查询失败')
        else:
            data['price'] = price

    return HttpResponse(
            json.dumps(context),
            mimetype=u'application/json',
    )

