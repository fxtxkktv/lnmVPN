# -*- coding: utf-8 -*-
'''
+-----------------------------------------------------------------------+
|Author: Cheng Wenfeng <277546922@qq.com>                               |
+-----------------------------------------------------------------------+
'''
import os,sys
from Functions import getAPIData,netModule

netmod=netModule()
API=getAPIData()

if __name__ == '__main__' :
   if sys.argv[1] == 'API' and sys.argv[2] == 'getUserLineID':
      print API.getUserLineID(sys.argv[3])
   elif sys.argv[1] == 'API' and sys.argv[2] == 'wrtvpnlogin':
      print wrtlog(sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6])
   elif sys.argv[1] == 'API' and sys.argv[2] == 'getgw':
      print netmod.getIfGW(sys.argv[3])
   elif sys.argv[1] == 'API' and sys.argv[2] == 'getniaddr':
      print netmod.getNiaddr(sys.argv[3])
   elif sys.argv[1] == 'API' and sys.argv[2] == 'getnetip':
      print netmod.NetIP()
   else:
      sys.exit()
