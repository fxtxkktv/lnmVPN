# -*- coding: utf-8 -*-
'''
+-----------------------------------------------------------------------+
|Author: Cheng Wenfeng <277546922@qq.com>                               |
+-----------------------------------------------------------------------+
'''
import os,sys
pro_path = os.path.split(os.path.realpath(__file__))[0]
sys.path.append('%s/../libs' % pro_path)

import Global as gl
#定义初始目录
gl._init()
gl.set_value('wkdir',pro_path)
gl.set_value('confdir','%s/../config' % pro_path)
gl.set_value('certdir','%s/../certs' % pro_path)
gl.set_value('plgdir','%s/../plugins' % pro_path)
gl.set_value('tempdir','%s/../template' % pro_path)
gl.set_value('assets','%s/../assets' % pro_path)
gl.set_value('vwdir','%s/../views' % pro_path)

from Functions import getAPIData,netModule,wrtlog

netmod=netModule()
API=getAPIData()

if __name__ == '__main__' :
   #获取用户策略ID [VPN]
   if sys.argv[1] == 'API' and sys.argv[2] == 'getUserLineID':
      print API.getUserLineID(sys.argv[3])
   #重置管理员密码接口
   elif sys.argv[1] == 'API' and sys.argv[2] == 'resetAdminPass':
      print API.resetAdminPass(sys.argv[3])
   #操作日志写入接口
   elif sys.argv[1] == 'API' and sys.argv[2] == 'wrtvpnlogin':
      print wrtlog(sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6])
   #获取设备接口状态
   elif sys.argv[1] == 'API' and sys.argv[2] == 'getnistatus':
      print netmod.getNistatus(sys.argv[3])
   #获取设备接口网关
   elif sys.argv[1] == 'API' and sys.argv[2] == 'getgw':
      print netmod.getIfGW(sys.argv[3])
   #获取接口权重值
   elif sys.argv[1] == 'API' and sys.argv[2] == 'getniweight':
      print netmod.getNiWeight(sys.argv[3])
   #获取接口名称
   elif sys.argv[1] == 'API' and sys.argv[2] == 'getniname':
      print netmod.getNiname(sys.argv[3])
   #获取接口区域
   elif sys.argv[1] == 'API' and sys.argv[2] == 'getnizone':
      print netmod.getNizone(sys.argv[3])
   #获取接口网络地址
   elif sys.argv[1] == 'API' and sys.argv[2] == 'getniaddr':
      print netmod.getNiaddr(sys.argv[3])
   #获取本机外网地址
   elif sys.argv[1] == 'API' and sys.argv[2] == 'getnetip':
      print netmod.NetIP()
   #获取VPN客户端网段路由
   elif sys.argv[1] == 'API' and sys.argv[2] == 'getVPNautoroute':
      print API.getVPNautoroute(sys.argv[3])
   else:
      sys.exit()
