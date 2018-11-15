#!/usr/bin/env python
#coding=utf-8
import os,sys,json,re,logging,ConfigParser
from bottle import request,route,error,run,default_app
from bottle import template,static_file,redirect,abort
import bottle,hashlib

from MySQL import writeDb,readDb
from Functions import AppServer,LoginCls,writeVPNconf,wrtlog
from Login import checkLogin,checkAccess
import Login

keys = AppServer().getConfValue('keys','passkey')


policylist_sql = " select id,name from vpnpolicy "
plylist_result = readDb(policylist_sql,)

@route('/changepasswd')
@checkLogin
def user():
    s = request.environ.get('beaker.session')
    return template('changepasswd',session=s,msg={},info={})

@route('/changepasswd',method="POST")
@checkLogin
def user():
    s = request.environ.get('beaker.session')
    username = s.get('username')
    oldpwd = request.forms.get("oldpwd")
    newpwd = request.forms.get("newpwd")
    newpwds = request.forms.get("newpwds")
    sql = " select passwd from user where username=%s "
    result = readDb(sql,(username,))
    if result[0].get('passwd') != LoginCls().encode(keys,oldpwd) :
       msg = {'color':'red','message':u'旧密码验证失败，请重新输入'}
       return template('changepasswd',session=s,msg=msg,info={})
    if newpwd != newpwds :
       msg = {'color':'red','message':u'密码两次输入不一致，请重新输入'}
       return template('changepasswd',session=s,msg=msg,info={})
    m_encrypt = LoginCls().encode(keys,newpwd)
    sql2 = " update user set passwd=%s where username=%s "
    result = writeDb(sql2,(m_encrypt,username))
    if result == True :
       wrtlog('User','更改密码成功',username,s.get('clientip'))
       msg = {'color':'green','message':u'密码更新成功,后续请以新密码登录系统'}
       return template('changepasswd',session=s,msg=msg,info={})
    else:
       wrtlog('User','更改密码失败',username,s.get('clientip'))
       msg = {'color':'red','message':u'密码更新失败,请核对错误'}
       return template('changepasswd',session=s,msg=msg,info={})

@route('/administrator')
@checkAccess
def user():
    s = request.environ.get('beaker.session')
    return template('admin',session=s,msg={},plylist_result=plylist_result)

@route('/user')
@checkAccess
def user():
    s = request.environ.get('beaker.session')
    return template('user',session=s,msg={},plylist_result=plylist_result)

@route('/adduser',method="POST")
@checkAccess
def adduser():
    s = request.environ.get('beaker.session')
    username = request.forms.get("username")
    passwd = request.forms.get("passwd")
    policy = request.forms.get("policy")
    access = request.forms.get("access")
    comment = request.forms.get("comment")
    #把密码进行md5加密码处理后再保存到数据库中
    m_encrypt = LoginCls().encode(keys,passwd)
    #检查表单长度
    if len(username) < 4 or (len(passwd) > 0 and len(passwd) < 8) :
       message = "用户名或密码长度不符要求！"
       return '-2'
    #检测表单各项值，如果出现为空的表单，则返回提示
    if not (username and policy and access):
        message = "表单不允许为空！"
        return '-2'
    sql = """
            INSERT INTO
                user(username,passwd,policy,access,comment)
            VALUES(%s,%s,%s,%s,%s)
        """
    data = (username,m_encrypt,policy,access,comment)
    result = writeDb(sql,data)
    if result:
       wrtlog('User','新增用户成功:%s' % username,s['username'],s.get('clientip'))
       return '0'
    else:
       wrtlog('User','新增用户失败:%s' % username,s['username'],s.get('clientip'))
       return '-1'

@route('/changeuser/<id>')
@checkAccess
def changeuser(id):
    s = request.environ.get('beaker.session')
    sql = "select username,policy,access,status,comment from user where id = %s"
    result = readDb(sql,(id,))
    return template('changeuser',session=s,info=result[0],plylist_result=plylist_result)

@route('/changeuser/<id>',method="POST")
@checkAccess
def do_changeuser(id):
    s = request.environ.get('beaker.session')
    username = request.forms.get("username")
    passwd = request.forms.get("passwd")
    policy = request.forms.get("policy")
    access = request.forms.get("access")
    comment = request.forms.get("comment")
    #把密码进行加密处理后再保存到数据库中
    if not passwd :
       sql = "select passwd from user where id = %s"
       m_encrypt = readDb(sql,(id,))[0].get('passwd')
    else:
       m_encrypt = LoginCls().encode(keys,passwd)
    # 判断用户表单跳转
    if int(access) == 0:
       formaddr='user'
    else :
       formaddr='admin'
    #检查表单长度
    if len(username) < 4 or (len(passwd) > 0 and len(passwd) < 8) :
        msg = {'color':'red','message':'用户名或密码长度错误，提交失败!'}
        return template(formaddr,session=s,msg=msg,plylist_result=plylist_result)
    if not (username and policy):
        msg = {'color':'red','message':'必填字段为空，提交失败!'}
        return template(formaddr,session=s,msg=msg,plylist_result=plylist_result)
    sql = """
            UPDATE user SET
            username=%s,passwd=%s,policy=%s,access=%s,comment=%s
            WHERE id=%s
        """
    data = (username,m_encrypt,int(policy),access,comment,id)
    result = writeDb(sql,data)
    if result == True:
       wrtlog('User','更新用户成功:%s' % username,s['username'],s.get('clientip'))
       msg = {'color':'green','message':'更新成功!'}
       writeVPNconf(action='uptuser')
       return template(formaddr,session=s,msg=msg,plylist_result=plylist_result)
    else:
       wrtlog('User','更新用户失败:%s' % username,s['username'],s.get('clientip'))
       msg = {'color':'red','message':'更新失败!'}
    return template(formaddr,session=s,msg=msg)

@route('/deluser',method="POST")
@checkAccess
def deluser():
    s = request.environ.get('beaker.session')
    id = request.forms.get('str').rstrip(',')
    if not id:
        return '-1'
    # 禁止删除ADMIN账户
    if id == '1':
       return '-1'
    for i in id.split(','):
        if id == '1':
           return '-1'
        sql = "delete from user where id in (%s) "
        result = writeDb(sql,(i,))
    if result:
       wrtlog('User','删除用户成功',s['username'],s.get('clientip'))
       return '0'
    else:
       wrtlog('User','删除用户失败',s['username'],s.get('clientip'))
       return '-1'

@route('/api/getuser',method=['GET', 'POST'])
@checkAccess
def getuser():
    sql = """
    SELECT
    U.id,
    U.username,
    D.name as policy,
    U.access,
    U.comment,
    date_format(U.adddate,'%%Y-%%m-%%d') as adddate
    FROM
    user as U
    LEFT OUTER JOIN vpnpolicy as D on U.policy=D.id
    WHERE access = 0
    order by username
    """
    userlist = readDb(sql,)
    return json.dumps(userlist)

@route('/api/getadmin',method=['GET', 'POST'])
@checkAccess
def getuser():
    sql = """
    SELECT
    U.id,
    U.username,
    D.name as policy,
    U.access,
    U.comment,
    date_format(U.adddate,'%%Y-%%m-%%d') as adddate
    FROM
    user as U
    LEFT OUTER JOIN vpnpolicy as D on U.policy=D.id
    WHERE access = 1
    order by username
    """
    userlist = readDb(sql,)
    return json.dumps(userlist)

# 帮助菜单
@route('/clientdownload')
@checkLogin
def systeminfo():
    """客户端下载项"""
    s = request.environ.get('beaker.session')
    return template('filedown',session=s,message='',info={})

@route('/support')
@checkLogin
def policyconf():
    """问题反馈页"""
    s = request.environ.get('beaker.session')
    return template('support',session=s,msg={})

@route('/support',method="POST")
@checkLogin
def policyconf():
    """问题反馈页"""
    from Functions import sendmail
    s = request.environ.get('beaker.session')
    subject = request.forms.get("subject")
    content = request.forms.get("content")
    if subject == '' and content == '':
        msg = {'color':'red','message':'主题或内容不能为空'}
        return template('support',session=s,msg=msg)
    result = sendmail(subject,content)
    if result == 1:
        msg = {'color':'red','message':'服务器连接失败，请检查配置!'}
        return template('support',session=s,msg=msg)
    elif result == 2:
        msg = {'color':'red','message':'用户名密码验证失败，请检查配置!'}
        return template('support',session=s,msg=msg)
    else:
        msg = {'color':'green','message':'邮件发送成功，请等待回复...'}
        return template('support',session=s,msg=msg)

if __name__ == '__main__' :
   sys.exit()
