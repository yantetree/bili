# -*- coding=utf-8 -*-
import simplejson as json

from django.http import HttpResponse

def fixed_login_required(func):
    '''
    Fixed login required function for RESTful api
    '''
    def wrap(request, *args, **kwords):
        if not request.user.is_authenticated():
            context = {'status' : 200, 
                       'data' : {
                           'success' : False, 
                           'errors' : [u'您尚未登录'],
                        },
                      }
            return HttpResponse(
                    json.dumps(context),
                    mimetype=u'application/json',
            )
        else:
            return func(request, *args, **kwords)
    return wrap

class MethodCheckError(Exception):
    '''
    Error raised when method is illegal
    '''
    pass

def check_method(method):
    '''
    Check method
    '''
    METHODS = ['POST', 'GET', 'DELETE', 'PUT']
    if method.upper() not in METHODS:
        raise MethodCheckError('Illegal method %s' % method)
    def wrap(func):
        def _wrap(request, *args, **kwords):
            if request.method != method.upper():
                context = {'status' : 404, 'data' : {}}
                return HttpResponse(
                        json.dumps(context),
                        mimetype=u'application/json'
                )
            else:
                return func(request, *args, **kwords)
        return _wrap
    return wrap
