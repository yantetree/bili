#-*- coding=utf-8 -*-
'''
Filters for all the models.
A filter always starts with a 'check_' prefix and then appends the model name(lower case)
A filter always return True if there're no invalid fields in the form,
or return a dict contains field name and error message.
'''

from bili.models import User
from sqlalchemy.orm.exc import NoResultFound

__all__ = ['check_user',]


def check_user(handler, username, email, password):
    '''
    check whether fields of the User form is valid.
    '''
    errors = {}
    if not username or len(username) < 6 or len(username) > 30:
        errors['username'] = u'用户名格式有误'
    else:
        try:
            user = handler.application.db.query(User).filter_by(username=username).one()
        except NoResultFound:
            pass
        else:
            errors['username'] = u'该用户名已存在'
    if not email or '@' not in email:
        errors['email'] = u'邮箱不正确'
    else:
        try:
            user = handler.application.db.query(User).filter_by(email=email).one()
        except NoResultFound:
            pass
        else:
            errors['email'] = u'该邮箱已被注册'
    if not password or len(password) < 6 or len(password) > 30:
        errors['password'] = u'密码格式有误'

    return (errors == {}), errors
