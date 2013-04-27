# -*- coding:utf-8 -*-
from bili.auth import is_login, login, logout, register
from bili.filters import check_user
from bili.utils.session import session
from tornado import web

__all__ = ['LoginHandler', 'RegisterHandler', 'LogoutHandler']

class LoginHandler(web.RequestHandler):
    @session
    def get(self):
        context = {'errors':{}}
        next_url = self.get_argument('next', default='/home')
        context['next_url'] = next_url
        if is_login(self):
            # if the request has been logined, redirect to the next page
            self.redirect(next_url)
        else: 
            return self.render('auth/login.html', context=context,
                    title='登录')

    @session
    def post(self):
        '''
        Login action
        '''
        context = {'errors':{}}
        next_url = self.get_argument('next', default='/home')
        context['next'] = next_url
        if is_login(self):
            # if the request has been logined, redirect to the next page
            self.redirect(next_url)
        else:
            username = self.get_argument('u', default=None)
            password = self.get_argument('p', default=None)
            user = login(self, username, password)
            if not user:
                context['username'] = username
                context['errors']['username'] = u'用户名或密码错误'
                return self.render('auth/login.html', context=context,
                        title='登录',)
            else:
                self.redirect(next_url)


class LogoutHandler(web.RequestHandler):
    pass

class RegisterHandler(web.RequestHandler):
    @session
    def get(self):
        context = {'errors':{}}
        next_url = self.get_argument('next', default='/home')
        context['next_url'] = next_url
        return self.render('auth/register.html', context=context,
                title=u'注册')

    @session
    def post(self):
        context = {'errors':{}}
        next_url = self.get_argument('next', default='/home')
        context['next_url'] = next_url
        username = self.get_argument('u', default=None)
        email = self.get_argument('e', default=None)
        password = self.get_argument('p', default=None)
        chk_res, context['errors'] = check_user(self, username=username, 
                email=email, password=password)
        if chk_res:
            user = register(self, username=username, email=email, 
                    password=password)
            login(self, user.username, user.password)
            self.redirect(next_url)
        else:
            return self.render('auth/register.html', context=context,
                    title=u'注册')

            
