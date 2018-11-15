#!/usr/bin/env python
#coding=utf-8
import os,sys,json,re,logging
from bottle import request,route,error,run,default_app
from bottle import template,static_file,redirect,abort,TEMPLATE_PATH

import Global as gl

#定义assets路径，即静态资源路径，如css,js,及样式中用到的图片等
assets_path = gl.get_value('assets')
#定义模板路径
TEMPLATE_PATH.append(gl.get_value('vwdir'))
TEMPLATE_PATH.append('%s/base' % gl.get_value('vwdir'))
TEMPLATE_PATH.append('%s/networks' % gl.get_value('vwdir'))
TEMPLATE_PATH.append('%s/firewall' % gl.get_value('vwdir'))
TEMPLATE_PATH.append('%s/system' % gl.get_value('vwdir'))
TEMPLATE_PATH.append('%s/user' % gl.get_value('vwdir'))
TEMPLATE_PATH.append('%s/vpnserv' % gl.get_value('vwdir'))

@route('/assets/<filename:re:.*\.css|.*\.js|.*\.png|.*\.jpg|.*\.gif>')
#@checkAccess
def server_static(filename):
    """定义/assets/下的静态(css,js,图片)资源路径"""
    return static_file(filename, root=assets_path)

@route('/assets/<filename:re:.*\.ttf|.*\.otf|.*\.eot|.*\.woff|.*\.woff2|.*\.svg|.*\.map>')
#@checkAccess
def server_static(filename):
    """定义/assets/字体资源路径"""
    return static_file(filename, root=assets_path)

@error(404)
def error404(error):
    """定制错误页面"""
    errdata=dict(body=error.body, stcode=error.status_code)
    return template('error',message=errdata.get('body'),code=errdata.get('stcode'))

@error(500)
def error500(error):
    """定制错误页面"""
    errdata=dict(body=error.body, stcode=error.status_code)
    return template('error',message=errdata.get('body'),code=errdata.get('stcode'))

@error(405)
def error405(error):
    """定制错误页面"""
    errdata=dict(body=error.body, stcode=error.status_code)
    return template('error',message=errdata.get('body'),code=errdata.get('stcode'))

if __name__ == '__main__':
   sys.exit()
