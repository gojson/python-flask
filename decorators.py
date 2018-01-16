#-*- encoding:utf-8 -*-

from functools import wraps
from flask import session
from flask import redirect,url_for

#登录限制
def login_required(func):
    @wraps(func)
    def wapper(*args,**kwargs):
        if session.get('user_id'):
            return func(*args,**kwargs)
        else:
            return redirect(url_for('login'))
    return wapper
