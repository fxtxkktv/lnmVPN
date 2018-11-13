#!/usr/bin/env python
#coding=utf-8
import os,sys,json,re,logging
from bottle import request,route,error,run,default_app
from bottle import template,static_file,redirect,abort
import bottle,hashlib
from MySQL import writeDb,readDb
from Functions import wrtlog,AppServer,LoginCls,cmdhandle

keys = AppServer().getConfValue('keys','passkey')

# login add warnning num to top.tpl
errnum = cmdhandle().envCheck('errnum')

def checkLogin(fn):
    """验证登陆，如果没有登陆，则跳转到login页面"""
    def BtnPrv(*args,**kw):
        s = request.environ.get('beaker.session')
        if not s.get('userid',None):
            return redirect('/login')
        return fn(*args,**kw)
    return BtnPrv

def checkAccess(fn):
    """验证权限，如果非管理员权限，则返回404页面"""
    def BtnPrv(*args,**kw):
        s = request.environ.get('beaker.session')
        if not s.get('userid',None):
            return redirect('/login')
        elif s.get('access',None) != 1:
            abort(404)
        return fn(*args,**kw)
    return BtnPrv

@route('/project')
@checkLogin
def index():
    s = request.environ.get('beaker.session')
    return template('index',message='',session=s,info={})

@route('/login')
def login():
    """用户登陆"""
    s = request.environ.get('beaker.session')
    s['sitename'] = AppServer().getConfValue('site','sitename')
    return template('login',session=s,message='')

@route('/login',method='POST')
def do_login():
    s = request.environ.get('beaker.session')
    s['sitename'] = AppServer().getConfValue('site','sitename')
    """用户登陆过程，判断用户帐号密码，保存SESSION"""
    username = request.forms.get('username').strip()
    passwd = request.forms.get('passwd').strip()
    if not username or not passwd:
        message = u'帐号或密码不能为空！'
        return template('login',message=message)

    m_encrypt = LoginCls().encode(keys,passwd)
    auth_sql = '''
        SELECT
            id,username,access
        FROM
            user
        WHERE
            username=%s and passwd=%s
        '''
    auth_user = readDb(auth_sql,(username,m_encrypt))
    if auth_user:
       s['webhost'] = request.environ.get('HTTP_HOST')
       s['clientip'] = request.environ.get('REMOTE_ADDR')
       s['username'] = username
       s['userid'] = auth_user[0]['id']
       s['access'] = auth_user[0]['access']
       # session中添加系统环境检测警报
       s['admemail'] = 'master@lnmos.com'
       s['errnum'] = errnum
       s['PayInfo'] = AppServer().getPayinfo()
       s.save()
       wrtlog('Login','登录成功',username,s['clientip'])
    else:
       clientip = request.environ.get('REMOTE_ADDR')
       wrtlog('Login','登录失败',username,clientip)
       message = u'帐号或密码错误！'
       return template('login',message=message,session=s)
    if auth_user[0]['access'] == 0 :
       return redirect('/project')
    return redirect('/')

@route('/logout')
def logout():
    """退出系统"""
    s = request.environ.get('beaker.session')
    user = s.get('user',None)
    try:
        s.delete()
    except Exception:
        pass
    return redirect('/login')


if __name__ == '__main__' :
   sys.exit()
