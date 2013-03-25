# -*- coding=utf-8 -*-
from django.contrib.auth import login, logout, authenticate 
from django.contrib.auth.models import User
from django.http import HttpResponse

from eparser import get_parser, QueryError, ParserNotFound
import gevent
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
            data[ename]['value'] = value

    return HttpResponse(
            json.dumps(context),
            mimetype=u'application/json',
    )


@check_method('GET')
def get_mul_price(request):
    '''
    search the price in the multiple eshop
    '''
    context = {'status' : 200}
    data = {'errors': []}
    context['data'] = data
    keyword = request.GET.get('k', None)
    if not keyword:
        data['success'] = False
        data['errors'].append(u'关键词不能为空')
    else:
        enames = (set(request.GET.keys())).intersection(PARSERS_DICT.keys())
        jobs = [gevent.spawn(parser.parse, ename, k) for ename in enames]
        gevent.joinall(jobs, time_out=5)
        for i in len(jobs):
            if jobs[i].exception:
                data[enames[i]]['error'] = jobs[i].exception.message
            else:
                data[enames[i]]['value'] = jobs[i].value
                
    return HttpResponse(
            json.dumps(context),
            mimetype=u'application/json',
    )


