# -*- coding:utf-8 -*-
from bili.auth import is_login, login, logout, register
from bili.filters import check_user
from bili.handlers.basehandler import BaseRequestHandler
from bili.utils.session import session
from tornado import web

__all__ = ['LoginHandler', 'RegisterHandler', 'LogoutHandler']

class LoginHandler(BaseRequestHandler):
    @session
    def get(self):
        context = {'errors':{}, 'title':u'登陆', 'request':self, 'username':''}
        next_url = self.get_argument('next', default='/home/')
        context['next'] = next_url
        if is_login(self):
            # if the request has been logined, redirect to the next page
            self.redirect(next_url)
        else: 
            return self.render('auth/login.html', **context)

    @session
    def post(self):
        '''
        Login action
        '''
        context = {'errors':{}, 'title':u'登陆', 'request':self}
        next_url = self.get_argument('next', default='/home/')
        context['next'] = next_url
        if is_login(self):
            # if the request has been logined, redirect to the next page
            self.redirect(next_url)
        else:
            username = self.get_argument('u', default='')
            password = self.get_argument('p', default='')
            user = login(self, username, password)
            if not user:
                context['username'] = username
                context['errors']['username'] = u'用户名或密码错误'
                return self.render('auth/login.html', **context)
            else:
                self.redirect(next_url)


class LogoutHandler(BaseRequestHandler):
    @session
    def get(self):
        next_url = self.get_argument('next', default='/home/')
        logout(self)
        self.redirect(next_url)


class RegisterHandler(BaseRequestHandler):
    @session
    def get(self):
        context = {'errors':{}, 'title':u'注册', 'request':self, 
                'username':'', 'email':''}
        next_url = self.get_argument('next', default='/home/')
        context['next_url'] = next_url
        context['title'] = u'注册'
        context['title'] = self
        return self.render('auth/register.html', **context)

    @session
    def post(self):
        context = {'errors':{}, 'title':u'注册', 'request':self}
        next_url = self.get_argument('next', default='/home/')
        context['next_url'] = next_url
        username = self.get_argument('u', default='')
        email = self.get_argument('e', default='')
        password = self.get_argument('p', default='')
        context['username'], context['email'] = username, email
        chk_res, context['errors'] = check_user(self, username=username, 
                email=email, password=password)
        if chk_res:
            user = register(self, username=username, email=email, 
                    password=password)
            login(self, user.username, user.password)
            self.redirect(next_url)
        else:
            return self.render('auth/register.html', **context)

            
