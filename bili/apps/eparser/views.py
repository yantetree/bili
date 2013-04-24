# -*- coding=utf-8 -*-
from django.contrib.auth import login, logout, authenticate 
from django.contrib.auth.models import User
from django.http import HttpResponse

from eparser import get_parser, QueryError, PARSERS_DICT, parse
#import gevent
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
    keyword = request.GET.get('k', None)
    if not keyword:
        data['success'] = False
        data['errors'].append(u'关键词不能为空')
    else:
        try:
            value = parse(ename, keyword)
        except QueryError:
            data['success'] = False
            data['errors'].append(u'查询失败')
        else:
            data['success'] = True
            data[ename]['value'] = value

    return HttpResponse(
            json.dumps(context),
            mimetype=u'application/json',
    )

#@fixed_login_required
@check_method('GET')
def get_single_price(request):
    '''
    search the price in single eshop
    '''
    context = {'status' : 200}
    data = {'errors': []}
    context['data'] = data
    keyword = request.GET.get('k', None)
    ename = list(
            (set(request.GET.keys())).intersection(PARSERS_DICT.keys()))[0]
    if not keyword:
        data['success'] = False
        data['errors'].append(u'关键词不能为空')
    else:
        try:
            value = parse(ename, keyword)
        except QueryError:
            data['success'] = False
            data['errors'].append(u'查询失败')
        else:
            data['success'] = True
            data.update({ename : {'value': value}})

    return HttpResponse(
            json.dumps(context),
            mimetype=u'application/json',
    )
