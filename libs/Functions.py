#coding=utf-8
'''
+-----------------------------------------------------------------------+
|Author: Cheng Wenfeng <277546922@qq.com>                               |
+-----------------------------------------------------------------------+
'''
import os,sys,json,base64,re,time,logging,hashlib,platform,socket,psutil
from Crypto.Cipher import AES
import netifaces as ni
import ConfigParser
import subprocess
import requests
from netaddr import IPAddress,IPNetwork

import Global as gl

#支持中文配置读取
reload(sys)
sys.setdefaultencoding('utf-8')

PayPng="""data:image/png;base64,
iVBORw0KGgoAAAANSUhEUgAAAfAAAAHxCAYAAACS8O5DAAAAA3NCSVQICAjb4U/gAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsQ
AAA7EAZUrDhsAAAAhdEVYdENyZWF0aW9uIFRpbWUAMjAxODoxMDowMSAyMDo0NzozM68N/3sAAAzFSURBVHhe7dzBjuQ2EkDBmf3/f7aNhavgk9AsdKrzjS
IuA/hQoCiqH+hD/v7rH78AgJT//fsvABDyvoH//v37//+B7/G0/7ExfX7s57XT/Zn+/Wnb1m8/r53+Ptde++8GDgBBAg4AQQIOAEECDgBBAg4AQQIOAEECD
gBBAg4AQQIOAEECDgBBAg4AQR/PQt82y3eaWcHXps/DtvNpPd9r2/mv74/1t3y6P27gABAk4AAQJOAAECTgABAk4AAQJOAAECTgABAk4AAQJOAAECTgABAk
4AAQdNss9Pqs4/r+nK7n1PT+nPK+rtXXP23bea6rf4+nptf/+n03cAAIEnAACBJwAAgScAAIEnAACBJwAAgScAAIEnAACBJwAAgScAAIEnAACDIL/Yuetj+
nnrafp+up2/a+nrb/p7ad//r3fuqu/XEDB4AgAQeAIAEHgCABB4AgAQeAIAEHgCABB4AgAQeAIAEHgCABB4AgAQeAILPQv2h6f049bT1+/9q28zDt9HlPTe
/PtvNwqn7+p921P27gABAk4AAQJOAAECTgABAk4AAQJOAAECTgABAk4AAQJOAAECTgABAk4AAQdNss9Lr6/jxtFvGp6ff1tP2fXv+272tafX+832uf7o8bO
AAECTgABAk4AAQJOAAECTgABAk4AAQJOAAECTgABAk4AAQJOAAECTgABH08C51rp7N8p2cF+/1rfv+a37/m96+d/j7XXvvvBg4AQQIOAEECDgBBAg4AQQIO
AEECDgBBAg4AQQIOAEECDgBBAg4AQQIOAEHvWej8rPqs41P12cjb9n/b75+aPm919fPDDDdwAAgScAAIEnAACBJwAAgScAAIEnAACBJwAAgScAAIEnAACBJ
wAAgScAAIes9CNwv32tNmEW973lPb9ufUtvPjPFxzHr5X/X2d+vR53cABIEjAASBIwAEgSMABIEjAASBIwAEgSMABIEjAASBIwAEgSMABIEjAASDo41no06
Zn8z5t1u429f2fPp+nnrafp552Hk5Nr3/b+51ez13cwAEgSMABIEjAASBIwAEgSMABIEjAASBIwAEgSMABIEjAASBIwAEgSMABIOg9C/1p6rOdT03PCq7v5
9NmKW97X9v2/2n7M/2829S/3xc3cAAIEnAACBJwAAgScAAIEnAACBJwAAgScAAIEnAACBJwAAgScAAIEnAACFo7C33b7N/pbTJ7+XvVn3f6vJ2afl+npvdn
2/k8Zf3fa/p7P/Vajxs4AAQJOAAECTgABAk4AAQJOAAECTgABAk4AAQJOAAECTgABAk4AAQJOAAEfTwL/XTW67bZuVtn237Vtuf1+9f8/rXT3z9lP6897Tx
s8+n+uIEDQJCAA0CQgANAkIADQJCAA0CQgANAkIADQJCAA0CQgANAkIADQJCAA0DQexb66SzWU9Ozc09Nz9rdNvt3ej/rnM+fVf8enQf+a/p9vbiBA0CQgA
NAkIADQJCAA0CQgANAkIADQJCAA0CQgANAkIADQJCAA0CQgANA0HsWOteeNkt522zkbcd0+jyc2nZ+TtXP/7bzOW16f6bPw6mt79cNHACCBBwAggQcAIIEH
ACCBBwAggQcAIIEHACCBBwAggQcAIIEHACCBBwAgt6z0J82S3nbbFvrv1Y/n9Ocn2vOz7X6/tTPz6nX+t3AASBIwAEgSMABIEjAASBIwAEgSMABIEjAASBI
wAEgSMABIEjAASBIwAEg6D0L/dTTZhdvm4U77cNj8WX1/Zzen2lPO8+n/L36XtPr3/b36q6/D27gABAk4AAQJOAAECTgABAk4AAQJOAAECTgABAk4AAQJOA
AECTgABAk4AAQZBb6EvXZv6emz8O29ztt+n2dqu//075Hrm17v6/1uIEDQJCAA0CQgANAkIADQJCAA0CQgANAkIADQJCAA0CQgANAkIADQJCAA0CQWehfVJ
+NPL2eafXzMG3b+62fz6edt+n11L+vU3ftpxs4AAQJOAAECTgABAk4AAQJOAAECTgABAk4AAQJOAAECTgABAk4AAQJOAAE3TYL/dRds2SnPG1/tu3/qfr6T
9W/l23rOVVf/ynn53u91u8GDgBBAg4AQQIOAEECDgBBAg4AQQIOAEECDgBBAg4AQQIOAEECDgBBAg4AQR/PQj+1bVbtqfps5FP12cLOz7X6eZ5e/zb+Pnyv
+vf4+n03cAAIEnAACBJwAAgScAAIEnAACBJwAAgScAAIEnAACBJwAAgScAAIEnAACPpjZqE/bTbv9Pq3va+6+nmr27b/p6bf1/T3W//7sPX8uIEDQJCAA0C
QgANAkIADQJCAA0CQgANAkIADQJCAA0CQgANAkIADQJCAA0DQx7PQt83mPfW09df3c9rp/mzb/7r6+Tm17TzUz/O283PX/riBA0CQgANAkIADQJCAA0CQgA
NAkIADQJCAA0CQgANAkIADQJCAA0CQgANA0HsW+vQs3G2zduuzf09tmxV8qn4e6uftaftTf19c23aeT73W4wYOAEECDgBBAg4AQQIOAEECDgBBAg4AQQIOA
EECDgBBAg4AQQIOAEECDgBB71nop+6a9Tplev2ntj1vfT3181m37bxNq39fXNv698cNHACCBBwAggQcAIIEHACCBBwAggQcAIIEHACCBBwAggQcAIIEHACC
BBwAgm6bhb5tluypD7cpqz5Lefq8Pe08T69/2/f1tPc1vf/b9vPU1u/FDRwAggQcAIIEHACCBBwAggQcAIIEHACCBBwAggQcAIIEHACCBBwAggQcAIJum4U
+bdss3/p66s976mnv69T0/myz7fxPmz4/p5523j7lBg4AQQIOAEECDgBBAg4AQQIOAEECDgBBAg4AQQIOAEECDgBBAg4AQQIOAEHvWejbZimbRXxt2/Oapf
yzps+P83mt/rzT5+HU9H5uW/+n78sNHACCBBwAggQcAIIEHACCBBwAggQcAIIEHACCBBwAggQcAIIEHACCBBwAgt6z0Lk2PVv4lFnEP6v+2Tzt/JyuZ9v3f
qr+fqf9KX9/3MABIEjAASBIwAEgSMABIEjAASBIwAEgSMABIEjAASBIwAEgSMABIEjAASDoPQv9abOFtz3vqen9mea8XXPerm173vp5ru/nNnd9L27gABAk
4AAQJOAAECTgABAk4AAQJOAAECTgABAk4AAQJOAAECTgABAk4AAQ9PEs9FNPm4U7bXo/p2f51tcz7Wnfy7bzvO18nnKer9Xf12v9buAAECTgABAk4AAQJOA
AECTgABAk4AAQJOAAECTgABAk4AAQJOAAECTgABD08Sz0bbNkt9k2y3fb+3Xerm07P6eedv7rvz9t2/6c2vq+3MABIEjAASBIwAEgSMABIEjAASBIwAEgSM
ABIEjAASBIwAEgSMABIEjAASDotlno22b5Ts/O5dr0+Tm17TzXvxf7ee10PfzZPj1vbuAAECTgABAk4AAQJOAAECTgABAk4AAQJOAAECTgABAk4AAQJOAAE
CTgABD0noXOz3raLOhp9vNnbduf0/Wc2vZ+Pe+1P+V7dAMHgCABB4AgAQeAIAEHgCABB4AgAQeAIAEHgCABB4AgAQeAIAEHgCABB4Cg9yz06dm5TzM9a/ep
s3+/att53rb/287P9Hqmz8P0ejzvtW3Pexc3cAAIEnAACBJwAAgScAAIEnAACBJwAAgScAAIEnAACBJwAAgScAAIEnAACPp4FvrW2bBTtu3P9Ozfaaf7U5+
lPG3bedv2fk9tW8+p6fPsea/dtR43cAAIEnAACBJwAAgScAAIEnAACBJwAAgScAAIEnAACBJwAAgScAAIEnAACLptFvr0bNhT0+s//f1T296X83Dtaft/up
5t6vuz7fvaZtv3cuq1fjdwAAgScAAIEnAACBJwAAgScAAIEnAACBJwAAgScAAIEnAACBJwAAgScAAIMgv9i6b359T0flr/tW3rnz6f0887rX4eTm07P6fq5
/mu/XcDB4AgAQeAIAEHgCABB4AgAQeAIAEHgCABB4AgAQeAIAEHgCABB4AgAQeAILPQv2h6f6Zte7/b9ufUtuf1fX2vp73f6fdVN/1+P+UGDgBBAg4AQQIO
AEECDgBBAg4AQQIOAEECDgBBAg4AQQIOAEECDgBBAg4AQbfNQq+r74/1X3P+f9a293vqaedh2/cy/X5P3fX3xw0cAIIEHACCBBwAggQcAIIEHACCBBwAggQ
cAIIEHACCBBwAggQcAIIEHACCPp6FzrW7ZuF+VX1W8LRt+1/fn6epf+/T561+frZ9jy9u4AAQJOAAECTgABAk4AAQJOAAECTgABAk4AAQJOAAECTgABAk4A
AQJOAAEPSehQ4AdLiBA0CQgANAzq9ffwODf85Xb7kllQAAAABJRU5ErkJggg==
"""

# App Server Info
class AppServer:
      def getConfValue(self,vzone,vkey):
          config=ConfigParser.ConfigParser()
          config.read('%s/config.ini' % gl.get_value('confdir'))
          #返回的内容需要把配置文件中的单引号和双引号开头和结尾替换
          str=config.get(vzone,vkey)
          newstr=re.sub('^\'','',str)
          newstr1=re.sub('\'$','',newstr)
          newstr2=re.sub('^"','',newstr1)
          newstr3=re.sub('"$','',newstr2)
          return newstr3.encode('utf-8')

      def getVersion(self):
          version = '1.0.31'
          return version

      def getPayinfo(self):
          return PayPng

# set global vars
def _initglv():
    global _global_dict
    _global_dict = {}

def set_value(name, value):
    _global_dict[name] = value

def get_value(name, defValue=None):
    try:
       return _global_dict[name]
    except KeyError:
       return defValue

# file md5
def GetFileMd5(filename):
    if not os.path.isfile(filename) or os.path.getsize(filename)==0:
       return False
    myhash = hashlib.md5()
    f = file(filename,'rb')
    while True:
        b = f.read(8096)
        if not b :
            break
        myhash.update(b)
    f.close()
    return myhash.hexdigest()

# cmds
class cmdhandle:
      def gettuplerst(self,cmd):
          result = tuple()
          cmdsresult = ''
          subp=subprocess.Popen(cmd,shell=True,executable='/bin/bash',stdout=subprocess.PIPE,stderr=subprocess.STDOUT,close_fds=True)
          while subp.poll() == None:
                for i in subp.stdout.readlines():
                    if i != "":
                       cmdsresult += i
          result = (subp.returncode,cmdsresult.replace('\n\n','\n'))
          return result

      def getdictrst(self,cmd):
          cmdst,result = self.gettuplerst(cmd)
          info = dict()
          info['status'] = cmdst
          info['result'] = result
          return info 

      def syscmds(self,tool,serv):
          if tool == 'PING':
             cmdstatus,result=self.gettuplerst('ping %s -c 4 -W 1' % serv)
             return '查询结果:\n%s' % result
          elif tool == 'TRACE':
             cmdstatus,result=self.gettuplerst('traceroute %s -w 0.3' % serv)
             return '查询结果:\n%s' % result
          elif tool == 'IPLIB':
             status,result=self.gettuplerst('curl -s http://ip.taobao.com/service/getIpInfo.php?ip=%s' % serv)
             if status == 0 :
                data = json.loads(result).get('data')
                infos = '%s,%s,%s,%s' % (data.get('country'),data.get('region'),data.get('city'),data.get('isp'))
                return infos
             else :
                infos="信息无法查到"
                return infos
          elif tool == 'IP2PTR':
             return IPAddress(serv).reverse_dns
          else:
             return 'error'

      # 环境检测
      def envCheck(self,getid):
          envList = []
          servtoollist = ['iptables','ipset','dnsmasq','ocserv','openconnect']
          i=0
          for tool in servtoollist :
              envDict={}
              envDict['name'] = str(tool)
              status,result=self.gettuplerst('which %s' % tool)
              if status == 0:
                 envDict['value'] = '0'
              else:
                 envDict['value'] = '1'
                 i = i+1
              envList.append(envDict)
          pytoollist = ['netaddr','netifaces','subprocess','ConfigParser','Crypto.Cipher','MySQLdb']
          for pytool in pytoollist :
              envDict={}
              envDict['name'] = str('Python::%s' % pytool)
              from importlib import import_module # 此处不能直接用 'import  pytool' 
              try:
                 import_module(pytool)
                 envDict['value'] = '0'
              except ImportError:
                 envDict['value'] = '1'
                 i = i+1
              envList.append(envDict)
          # 返回分两种结果，不符合数和结果列表
          if getid == 'errnum' :
             return i
          else:
             return envList

      # 服务检测
      def servchk(self,port):
          status,result = self.gettuplerst('netstat -antu|grep "[tc|ud]p.*:%s\s.*"' % port)
          return status

      # 服务启动
      def servboot(self,svname,**opts):
          if svname == 'ocserv' :
             self.gettuplerst('%s/sbin/startvpn.sh restart' % gl.get_value('wkdir'))
          elif svname == 'vpnconn':
             self.gettuplerst('%s/sbin/startvpnconn.sh restart' % gl.get_value('wkdir'))
          elif svname == 'dnsmasq' :
             if opts.get('action') == 'stop' :
                self.gettuplerst('%s/sbin/startdns.sh stop' % gl.get_value('wkdir'))
             else :
                self.gettuplerst('echo "nameserver 127.0.0.1" > /etc/resolv.conf')
                self.gettuplerst('%s/sbin/startdns.sh restart' % gl.get_value('wkdir'))
          elif svname == 'networks' :
             self.gettuplerst('%s/sbin/startnetworks.sh restart >/dev/null 2>&1' % gl.get_value('wkdir'))
          elif svname == 'firewall' :
             self.gettuplerst('%s/sbin/startfw.sh restart' % gl.get_value('wkdir'))
             #防火墙重启后重新加载已连接的vpn用户策略
             from MySQL import readDb
             x,y=self.gettuplerst('occtl show users|awk \'/connected/{print $2,$5}\'')
             if x == 0 and 'error' not in y :
                for i in y.split('\n'):
                    if i != "":
                       sql = " select policy from user where username=%s union select organization as policy from certmgr where commonname=%s "
                       result =  readDb(sql,(i.split()[0],i.split()[0]))
                       try:
                          self.gettuplerst('ipset add vpnpolicy_src_%s %s' % (result[0].get('policy'),i.split()[1]))
                       except:
                          return True

cmds = cmdhandle()

# Login
class LoginCls:
    def encode(self,key,data):
        Formatkey = '\0'
        FormatStr = lambda s: s+(16 - len(s)%16)*Formatkey
        keyIV=key
        obj = AES.new(key, AES.MODE_CBC,keyIV)
        ciphertext = base64.b64encode(obj.encrypt(FormatStr(data)))
        return ciphertext

    def decode(self,key,data):
        keyIV=key
        obj2 = AES.new(key, AES.MODE_CBC,keyIV)
        try:
           newmesg = obj2.decrypt(base64.b64decode(data))
           return newmesg.replace('\0','')
        except  TypeError:
           return False

# Network
class netModule:
      def NetIP(self):
          try:
             ipContent = requests.get('http://pv.sohu.com/cityjson?ie=utf-8',timeout=1).text
             ipContentJson = json.loads('{'+re.findall(r'{(.+?)}',ipContent)[0]+"}")
             netip=ipContentJson.get('cip')
          except:
             netip='获取失败'
          return netip

      def NatIP(self):
          try:
             s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
             s.settimeout(1)
             s.connect(('223.5.5.5', 80))
             NAThost = s.getsockname()[0]
          except:
             NAThost = '获取失败'
          finally:
             s.close()  
          return NAThost
    
      def PhyInterfaces(self):
          nilist = dict()
          for x in ni.interfaces():
              s = re.match('^eth[0-9]$', x)
              if str(s) != 'None':
                 nilist[x] = ni.ifaddresses(x)[17][0]['addr']
                 continue
          return nilist

      def VtInterfaces(self):
          """ 显示所有的虚拟接口列表 """
          nilist = []
          for x in ni.interfaces():
              if 'tun' in x:
                 (nilist.append(x),)
                 continue
          return nilist

      def VpnInterfaces(self):
          """ 显示所有的VPN接口列表 """
          nilist = []
          for x in ni.interfaces():
              if 'vpn' in x:
                 (nilist.append(x),)
                 continue
          return nilist

      def getNiaddr(self,ifacename):
          try:
             info = ni.ifaddresses(ifacename)
          except:
             return False
          if ni.AF_INET not in info:
             return False
          return info[ni.AF_INET][0]['addr']

      def getIfGW(self,ifacename):
          """ 当ifacename=defaultgw时显示默认网关，当ifacename=接口名时显示为该接口的网关"""
          netRoutes = dict()
          netRoutes['defaultgw']=""
          for rlist in ni.gateways()[ni.AF_INET]:
              if rlist[2] == True:
                 netRoutes['defaultgw'] += '%s\t' % rlist[0]
              else:
                 netRoutes[rlist[1]] = rlist[0]
          return netRoutes.get(ifacename)

      def checkip(self,ip):
          if ip == '' :
             return False
          try:
             IPAddress(ip)
          except:
             return False
          return True

      def checkmask(self,mask):
          try:
             IPNetwork('1.1.1.0/%s' % mask)
          except:
             return False
          return True
    
      def checkipmask(self,ipnet):
          try:
             IPNetwork(ipnet)
          except:
             return False
          return True

      def checknet(self,xip,ip,mask):
          try:
             IPNetwork('%s/%s' % (ip,mask))
          except:
             return False
          try:
             IPAddress(xip) in IPNetwork('%s/%s' % (ip,mask))
          except:
             return False
          return True

      def is_port(self,port):
          try:
             int(port)
          except:
             return False
          if int(port) > 0 and int(port) < 65535 :
             return True
          else:
             return False

      def is_ValidMac(self,mac):
          if re.match(r"^\s*([0-9a-fA-F]{2,2}:){5,5}[0-9a-fA-F]{2,2}\s*$", mac): 
             return True
          return False

      def is_domain(self,domain):
          domain_regex = re.compile(r'(?:[A-Z0-9_](?:[A-Z0-9-_]{0,247}[A-Z0-9])?\.)+(?:[A-Z]{2,6}|[A-Z0-9-]{2,}(?<!-))\Z',re.IGNORECASE)
          return True if domain_regex.match(domain) else False

      def InitNIinfo(self):
          from MySQL import writeDb
          # 初始化物理接口
          sql = "INSERT INTO sysattr (attr, value,servattr) VALUES (%s,%s,'netiface') ON DUPLICATE KEY UPDATE attr=%s,value=%s,servattr='netiface'"
          niinfo=self.PhyInterfaces()
          for k, v in niinfo.items():
              data=(k,v,k,v)
              writeDb(sql,data)
          vtinfo=self.VtInterfaces()
          if 'tun1000' in vtinfo:
             sql = "INSERT INTO sysattr (attr,value,status,servattr) VALUES ('vpnrelay','tun1000','1','vpnrelay') ON DUPLICATE KEY UPDATE attr='vpnrelay',value='tun1000',servattr='vpnrelay',status='1'"
          else:
             sql = "INSERT INTO sysattr (attr,value,status,servattr) VALUES ('vpnrelay','tun1000','0','vpnrelay') ON DUPLICATE KEY UPDATE attr='vpnrelay',value='tun1000',servattr='vpnrelay',status='0'"
          writeDb(sql,)
          return True

      def Initrouteinfo(self):
          from MySQL import writeDb,readDb
          regexp = '(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)'
          cmd_status,cmd_result=cmds.gettuplerst("route -n|awk -v exnet='169.254.0.0' '/^%s/{if($1 != exnet) print $1,$3,$2,$8,$4}' " % regexp)
          sql = " INSERT INTO sysroute (type, dest, netmask, gateway, iface, fromtype) VALUES (%s,%s,%s,%s,%s,%s)"
          sql2 = " DELETE FROM sysroute WHERE fromtype=0 "
          writeDb(sql2,)
          for i in cmd_result.split('\n'):
              if i != "":
                 destnet = i.split(" ")[0]
                 netmask = i.split(" ")[1]
                 gateway = i.split(" ")[2]
                 ifacename = i.split(" ")[3]
                 data=('net',destnet,netmask,gateway,ifacename,0)
                 writeDb(sql,data)

      def getifaceData(self,strname):
          from MySQL import writeDb,readDb
          if strname == u'getni': 
             sql = " select ifacename from netiface "
             ifacelists = readDb(sql,)  
          else:
             sql = " select ifacename from netiface where id=%s "
             ifacelists = readDb(sql,(strname,))  
          for ifacelist in ifacelists :
              for x,phydev in ifacelist.items():
                  return_code,output = cmds.gettuplerst("ethtool " + phydev + " |grep detected")
                  if "no" in output:
                     ifacestatus = 'DOWN'
                     #continue
                  else:
                     ifacestatus = 'UP'
                  cst1,TXdata=cmds.gettuplerst('ip -s link show %s|awk "/TX:/{getline v;print v}"|awk \'{printf ("%%.0f",$1/1024/1024)}\' ' % phydev)
                  cst2,RXdata=cmds.gettuplerst('ip -s link show %s|awk "/RX:/{getline v;print v}"|awk \'{printf ("%%.0f",$1/1024/1024)}\' ' % phydev)
                  sql2 = " UPDATE netiface set status=%s,txdata=%s,rxdata=%s where ifacename=%s "
                  data=(ifacestatus,int(TXdata),int(RXdata),phydev)
                  writeDb(sql2,data)

netmod = netModule()

def mkcert(**kwargs):
    from MySQL import writeDb
    certdir = gl.get_value('certdir')
    createdate = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    if kwargs.get('ct') == 'server' :
       # 清除原有的所有证书数据
       cmds.gettuplerst('rm -rf %s/*.crt %s/*.pem' % (certdir,certdir))
       writeDb('TRUNCATE TABLE certmgr')
       # CA
       cmds.gettuplerst('certtool --generate-privkey --outfile %s/ca-key.pem' % certdir)
       tmpfile = open('/tmp/certtmp.txt','w+')
       ca_tmp1 = "cn='%s'\norganization='%s'\nserial=1\nexpiration_days=%s\nca\nsigning_key\ncert_signing_key\ncrl_signing_key\n" % (kwargs.get('cn'),kwargs.get('ou'),kwargs.get('ex'))
       tmpfile.write('%s' % ca_tmp1)
       tmpfile.close()
       cmds.gettuplerst('certtool --generate-self-signed --load-privkey %s/ca-key.pem --template /tmp/certtmp.txt --outfile %s/ca.crt' % (certdir,certdir))
       sql = """ INSERT INTO certmgr(commonname,certtype,organization,createdate,expiration,comment) VALUES('CA',%s,%s,%s,%s,%s) """
       data = (kwargs.get('cn'),kwargs.get('ou'),createdate,kwargs.get('ex'),kwargs.get('comment'))
       result = writeDb(sql,data)
       if result == False : 
          return False
       # Server
       cmds.gettuplerst('certtool --generate-privkey --outfile %s/server-key.pem' % certdir)
       tmpfile = open('/tmp/certtmp.txt','w+')
       serv_tmp1 = "cn='%s'\norganization='%s'\nexpiration_days=%s\nencryption_key\nsigning_key\ntls_www_server\n" % (kwargs.get('cn'),kwargs.get('ou'),kwargs.get('ex'))
       tmpfile.write('%s' % serv_tmp1)
       tmpfile.close()
       cmds.gettuplerst('certtool --generate-certificate --load-privkey %s/server-key.pem --load-ca-certificate %s/ca.crt --load-ca-privkey %s/ca-key.pem --template /tmp/certtmp.txt --outfile %s/server.crt' % (certdir,certdir,certdir,certdir))
       sql = """ INSERT INTO certmgr(commonname,certtype,organization,createdate,expiration,comment) VALUES('Server',%s,%s,%s,%s,%s) """
       data = (kwargs.get('cn'),kwargs.get('ou'),createdate,kwargs.get('ex'),kwargs.get('comment'))
       result = writeDb(sql,data)
       if result == False :
          return False
       # CRL 
       tmpfile = open('%s/crl.txt' % certdir,'w+')
       crl_tmp1 = "crl_next_update = 9999\ncrl_number = 1\n"
       tmpfile.write('%s' % crl_tmp1)
       tmpfile.close()
       cmds.gettuplerst('certtool --generate-crl --load-ca-privkey %s/ca-key.pem --load-ca-certificate %s/ca.crt --template %s/crl.txt --outfile %s/crl.pem' % (certdir,certdir,certdir,certdir))
       result = cmds.gettuplerst('rm -rf /tmp/certtmp*')
       if result :
          return 0
    elif kwargs.get('ct') == 'client':
       tmpfile = open('/tmp/certtmp.txt','w+')
       user_tmp1 = "cn=%s\nunit=%s\nexpiration_days='%s'\nsigning_key\ntls_www_client\n" % (kwargs.get('cn'),kwargs.get('ou'),kwargs.get('ex'))
       tmpfile.write('%s' % user_tmp1)
       tmpfile.close()
       cmds.gettuplerst('certtool --generate-privkey --outfile %s/%s.pem' % (certdir,kwargs.get('cn')))
       cmds.gettuplerst('certtool --generate-certificate --load-privkey %s/%s.pem --load-ca-certificate %s/ca.crt --load-ca-privkey %s/ca-key.pem --template /tmp/certtmp.txt --outfile %s/%s.crt' % (certdir,kwargs.get('cn'),certdir,certdir,certdir,kwargs.get('cn')))
       sql = """ INSERT INTO certmgr(commonname,certtype,organization,createdate,expiration,safekey,comment) VALUES(%s,'Client',%s,%s,%s,%s,%s) """
       data = (kwargs.get('cn'),kwargs.get('ou'),createdate,kwargs.get('ex'),kwargs.get('safekey'),kwargs.get('comment'))
       result = writeDb(sql,data)
       if result == False:
          return False
       return 0

def writeNIconf(**kwargs):
    from MySQL import readDb
    if kwargs.get('action') == 'uptconf':
       tfo = '%s/template/networks_template.conf' % gl.get_value('wkdir')
       newfo = '%s/plugins/networks/netiface.conf' % gl.get_value('wkdir')
       aaa = open(tfo,'r+').read()
       # 处理网卡配置写入
       sql = " SELECT id,ifacename,ifacetype,ipaddr,netmask,gateway,defaultgw,extip FROM netiface "
       result = readDb(sql,)
       newline = ''
       for data in result:
           ndata=(data.get('id'),data.get('id'),data.get('ifacename'),data.get('ifacetype'),data.get('ipaddr'),data.get('netmask'),data.get('gateway'),data.get('defaultgw'),data.get('extip').replace('\n',';'))
           result1 = 'netiface_%s=(id=%s ifacename=%s ifacetype=%s ipaddr=%s netmask=%s gateway=%s defaultgw=%s extip=%s)' % ndata
           newline = newline+'\n'+result1
       aaa = re.sub(r'nizone.*',newline, aaa)
       open(newfo,'w+').write(aaa)
       return True

def writeROUTEconf(**kwargs):
    from MySQL import readDb
    if kwargs.get('action') == 'uptconf':
       # route为什么要写配置文件？防止数据库故障且减小DB读写IO
       tfo = '%s/route_template.conf' % gl.get_value('tempdir')
       newfo = '%s/networks/route.conf' % gl.get_value('plgdir')
       aaa = open(tfo,'r+').read()
       # 处理静态路由
       sql = " SELECT id,type,dest,netmask,gateway,iface FROM sysroute where fromtype=1 "
       result = readDb(sql,)
       newline = ''
       for data in result:
           ndata=(data.get('id'),data.get('type'),data.get('dest'),data.get('netmask'),data.get('gateway'),data.get('iface'))
           result1 = 'stroute_%s=(type=%s dest=%s netmask=%s gateway=%s iface=%s)' % ndata
           newline = newline+'\n'+result1
       aaa = re.sub(r'syszone.*',newline, aaa)
       # 处理高级路由
       sql = " SELECT id,srcaddr,destaddr,pronum,iface FROM sysrouteadv"
       result = readDb(sql,)
       newline = ''
       for data in result:
           if data.get('srcaddr') == "" and data.get('destaddr') == "":
              rtattr = 'sys'
           else:
              rtattr = 'net'
           ndata = (data.get('id'),rtattr,data.get('pronum'),data.get('iface'))
           newline += 'advroute_%s=(rtattr=%s pronum=%s iface=%s)\n' % ndata
       #aaa = re.sub(r'advzone.*',newline, aaa)
       # 处理DNS防污染
       sql = " select value from sysattr where servattr='dnsmasq' and attr='dnsconf' "
       result = readDb(sql,)
       for data in result:
           idata = eval(data.get('value'))
           if idata.get('dnsrule') == "1" :
              idata.get('dnslist')
              newline += 'advroute_999=(pronum=99 dnsserver=%s iface=tun1000)\n' % idata.get('dnslist').replace('\n','-')
       aaa = re.sub(r'advzone.*',newline, aaa)
       open(newfo,'w+').write(aaa)
       cmds.servboot('networks')

def writeDNSconf(**kwargs):
    from MySQL import readDb
    if kwargs.get('action') == 'uptconf':
       tfo = '%s/dnsmasq_template.conf' % gl.get_value('tempdir')
       newfo = '%s/dnsmasq/dnsmasq.conf' % gl.get_value('plgdir')
       aaa = open(tfo,'r+').read()
       # 1.处理DNS配置
       sql = " SELECT value FROM sysattr where servattr='dnsmasq' and attr='dnsconf' "
       result = readDb(sql,)
       for data in result:
           idata = eval(data.get('value'))
           dnsrelay=idata.get('dnsrelay')
           dnsproxy=idata.get('dnsproxy')
           # write conf
           newlist = ''
           for list in idata.get('dnslist').split('\n'):
               strlist = 'server=%s' % list
               newlist = newlist+'\n'+strlist
           aaa = re.sub(r'server=.*',newlist, aaa)
       # 1.1处理 A records
       sql2 = " select domain,data from dnsrecord where dnstype='A' and action=1"
       newlist2 = ''
       result2 = readDb(sql2,)
       for data2 in result2:
           #write conf
           strlist2 = 'address=/%s/%s' % (data2.get('domain'),data2.get('data'))
           newlist2 = newlist2+'\n'+strlist2
       aaa = re.sub(r'address=.*',newlist2, aaa)
       # 1.2处理 MX records
       sql3 = " select domain,data,pronum from dnsrecord where dnstype='MX' and action=1"
       newlist3 = ''
       result3 = readDb(sql3,)
       for data3 in result3:
           #write conf
           strlist3 = 'mx-host=%s,%s,%s' % (data3.get('domain'),data3.get('data'),data3.get('pronum'))
           newlist3 = newlist3+'\n'+strlist3
       aaa = re.sub(r'mx-host=.*',newlist3, aaa)
       # 1.3处理 CNAME records
       sql4 = " select domain,data from dnsrecord where dnstype='CNAME' and action=1"
       newlist4 = ''
       result4 = readDb(sql4,)
       for data4 in result4:
           #write conf
           strlist4 = 'cname=%s,%s' % (data4.get('domain'),data4.get('data'))
           newlist4 = newlist4+'\n'+strlist4
       aaa = re.sub(r'cname=.*',newlist4, aaa)
       # 1.4处理 PTR records
       sql5 = " select domain,data from dnsrecord where dnstype='PTR' and action=1"
       newlist5 = ''
       result5 = readDb(sql5,)
       for data5 in result5:
           #write conf
           strlist5 = 'ptr-record=%s,%s' % (data5.get('domain'),data5.get('data'))
           newlist5 = newlist5+'\n'+strlist5
       aaa = re.sub(r'ptr-record=.*',newlist5, aaa)
       # 1.5处理 DNS relay server records
       sql6 = " select domain,data from dnsrecord where dnstype='NS' and action=1"
       newlist6 = ''
       result6 = readDb(sql6,)
       for data6 in result6:
           #write conf
           strlist6 = 'server=/%s/%s' % (data6.get('domain'),data6.get('data'))
           newlist6 = newlist6+'\n'+strlist6
       aaa = re.sub(r'dnsrelay=.*',newlist6, aaa)
       # 2.处理DHCP配置
       sql7 = " SELECT value FROM sysattr where servattr='dnsmasq' and attr='dhcpconf' "
       result7 = readDb(sql7,)
       ccc = ''
       try:
            idata = json.loads(result7[0].get('value'))
            if idata.get('dhcpenable') == '1':
               ccc = "dhcp-range=%s,%s,%sh\n" % (idata.get('startip'),idata.get('stopip'),idata.get('otime'))
               ccc += "dhcp-option=3,%s\n" % (idata.get('getgw'))
               ccc += "dhcp-option=option:dns-server,%s,%s\n" % (idata.get('getdns1'),idata.get('getdns2'))
               if idata.get('dhcplist') != "":
                  for i in idata.get('dhcplist').split('\n'):
                      ccc += "dhcp-host=%s\n" % i
       except:
            True
       # write conf
       aaa = re.sub(r'{dhcpzone}',ccc, aaa)
       open(newfo,'w+').write(aaa)
       # 判断服务是否重启
       if dnsrelay == '1':
          cmds.servboot('dnsmasq',action='restart')
       else :
          cmds.servboot('dnsmasq',action='stop')
    return  True
        
def writeVPNconf(**kwargs):
    from MySQL import readDb
    if kwargs.get('action') == 'addconf' or kwargs.get('action') == 'uptconf':
       sql = " SELECT value FROM sysattr WHERE attr='vpnserver' and status='1'"
       result = readDb(sql,)
       #sql = " SELECT id,servmode,authtype,ipaddr,servport,virip,virmask,maxclient,maxuser,authtimeout,authnum,locktime,comp,cisco,workstatus FROM vpnservconf "
       #result = readDb(sql,)
       for data in result :
           idata = eval(data.get('value'))
           idata['servmode'] = 'server'
           if idata.get('comp') == '0':
              comp = 'true'
           else:
              comp = 'false'
        
           if idata.get('cisco') == '0':
              cisco = 'true'
           else:
              cisco = 'false' 
           
           if idata.get('authtype') == '0':
              authtype = '\"certificate\"'
           elif idata.get('authtype') == '1':
              authtype = '\"plain[%s/ocserv/ocserv.auth]\"' % gl.get_value('plgdir')
           elif idata.get('authtype') == '2':
              authtype = '\"plain[%s/ocserv/ocserv.auth]\"\nenable-auth=\"certificate\"' % gl.get_value('plgdir')
          
           tfo = '%s/ocserv_template.conf' % gl.get_value('tempdir')
           newfo = '%s/ocserv/ocserv_%s.conf' % (gl.get_value('plgdir'),idata.get('servmode'))
           aaa = open(tfo,'r+').read()
           aaa = re.sub(r'auth =.*',"auth = %s" % authtype, aaa)
           if idata.get('ipaddr') != '*':
              aaa = re.sub(r'#listen-host =.*',"listen-host = %s" % idata.get('ipaddr'), aaa)
           aaa = re.sub(r'max-clients =.*',"max-clients = %s" % idata.get('maxclient'), aaa)
           aaa = re.sub(r'tcp-port =.*',"tcp-port = %s" % idata.get('servport'), aaa)
           aaa = re.sub(r'udp-port =.*',"udp-port = %s" % idata.get('servport'), aaa)
           aaa = re.sub(r'max-same-clients =.*',"max-same-clients = %s" % idata.get('maxuser'), aaa)
           aaa = re.sub(r'compression =.*',"compression = %s" % comp, aaa)
           aaa = re.sub(r'auth-timeout =.*',"auth-timeout = %s" % idata.get('authtimeout'), aaa)
           aaa = re.sub(r'min-reauth-time =.*',"min-reauth-time = %s" % idata.get('authnum'), aaa)
           aaa = re.sub(r'ban-reset-time =.*',"ban-reset-time = %s" % idata.get('locktime'), aaa)
           aaa = re.sub(r'ipv4-network =.*',"ipv4-network = %s" % idata.get('virip'), aaa)
           aaa = re.sub(r'ipv4-netmask =.*',"ipv4-netmask = %s" % idata.get('virmask'), aaa)
           aaa = re.sub(r'cisco-client-compat =.*',"cisco-client-compat = %s" % cisco, aaa)
           aaa = re.sub(r'{signpath}',gl.get_value('wkdir'), aaa)
           open(newfo,'w+').write(aaa)
    elif kwargs.get('action') == 'uptcltconf' :
         tfo = '%s/openconn_template.conf' % gl.get_value('tempdir')
         newfo = '%s/ocserv/ocserv_client.conf' % gl.get_value('plgdir')
         sql = " SELECT value FROM sysattr WHERE attr='vpnclient' and status='1'"
         result = readDb(sql,)
         aaa = open(tfo,'r+').read()
         for data in result:
             idata = eval(data.get('value'))
             # write conf
             if idata.get('authtype') == '1':
                ndata=(idata.get('ipaddr'),idata.get('servport'),idata.get('tunid'),idata.get('vmtu'),idata.get('vpnuser'),idata.get('vpnpass'))
                newlist = 'openconn_conf=(authtype=1 ipaddr=%s servport=%s tunid=%s vmtu=%s vpnuser=%s vpnpass=%s)' % ndata
             else:
                ndata=(idata.get('ipaddr'),idata.get('servport'),idata.get('tunid'),idata.get('vmtu'),idata.get('certinfo'),idata.get('vpnpass'))
                newlist = 'openconn_conf=(authtype=0 ipaddr=%s servport=%s tunid=%s vmtu=%s certinfo=%s vpnpass=%s)' % ndata
             aaa = re.sub(r'clientconfzone.*', newlist, aaa)
             open(newfo,'w+').write(aaa)
    elif kwargs.get('action') == 'uptuser' :
         keys = AppServer().getConfValue('keys','passkey')
         sql = " select username,passwd,policy from user union select commonname,safekey,organization from certmgr where certtype='Client' "
         result = readDb(sql,)
         if result :
            cmds.gettuplerst('true > %s/ocserv/ocserv.auth' % gl.get_value('plgdir'))
            for data in result :
                try:
                   npass = LoginCls().decode(keys,data.get('passwd'))
                except:
                   npass = data.get('passwd')
                if npass is False :
                   npass = data.get('passwd')
                open('/tmp/secret.txt','w+').write(npass)
                cmds.gettuplerst('ocpasswd -c %s/ocserv/ocserv.auth %s -g %s < %s' % (gl.get_value('plgdir'),data.get('username'),data.get('policy'),'/tmp/secret.txt'))
    elif kwargs.get('action') == 'uptgroup' :
         sql = " select id,pushdns,pushroute,pushnoroute from vpnpolicy "
         result = readDb(sql,)
         if result :
            for data in result :
                pushline = ''
                grpfile = '%s/ocserv/group/%s' % (gl.get_value('plgdir'),data.get('id'))
                cmds.gettuplerst('true > %s' % grpfile)
                if data.get('pushdns') != "":
                   for adb in data.get('pushdns').split('\n'):
                       pushline += "dns = %s\n" % adb
                if data.get('pushroute') != "":
                   for bdb in data.get('pushroute').split('\n'):
                       pushline += "route = %s\n" % bdb
                if data.get('pushnoroute') != "":
                   for cdb in data.get('pushnoroute').split('\n'):
                       pushline += "no-route = %s\n" % cdb
                open(grpfile,'a+').write(pushline)
    elif kwargs.get('action') == 'uptprofile' :
         sql = " select value from sysattr where attr='vpnprofile' " 
         result = readDb(sql,)
         if result :
            profile='%s/ocserv/profile.xml' % gl.get_value('plgdir')
            cmds.gettuplerst('true > %s' % profile)
            open(profile,'wb+').write('%s\n' % result[0].get('value'))
            cmds.gettuplerst('%s/sbin/dos2unix %s' % (gl.get_value('wkdir'),profile))
    return True

def writeUTMconf(**kwargs):
    from MySQL import readDb
    tfo = '%s/ipset_template.conf' % gl.get_value('tempdir')
    tfo2 = '%s/iptables_template.conf' % gl.get_value('tempdir')
    # 判断是否临时写入
    if kwargs.get('tempiptconf') == True :
       newfo = '/tmp/ipset.conf'
       newfo2 = '/tmp/iptables.conf'
    else :
       newfo = '%s/firewall/ipset.conf' % gl.get_value('plgdir')
       newfo2 = '%s/firewall/iptables.conf' % gl.get_value('plgdir')
    aaa = open(tfo,'r+').read()
    bbb = open(tfo2,'r+').read()
    ipsetline,iptline = '',''
    if kwargs.get('action') == 'addconf' or kwargs.get('action') == 'uptconf':
       # 写入允许VPN服务端口
       sql = " select value from sysattr where attr='vpnserver' "
       iresult = readDb(sql,)
       portline = '';
       for sdata in iresult:
           idata = eval(sdata.get('value'))
           sportline='add vpnport %s' % idata.get('servport')
           portline += sportline+'\n'
       aaa = re.sub(r'{{vpnportzone}}.*',portline, aaa)
       # 写UTM规则
       sql = " select id,pronum,actzone,srcaddr,sproto,sport,dstaddr,dproto,dport,runaction from ruleconfutm where status='1' order by pronum"
       result = readDb(sql,)
       utmiptlineA,utmsetline2 = '',''
       for cdata in result:
           if cdata.get('sport') == "":
              sportdesc = ''
           else :
              sportdesc = '-m multiport -p %s --sport %s' % (cdata.get('sproto').lower(),cdata.get('sport'))
           if cdata.get('dport') == "":
              dportdesc = ''
           else :
              dportdesc = '-m multiport -p %s --dport %s' % (cdata.get('dproto').lower(),cdata.get('dport'))
           if cdata.get('srcaddr') != "" and cdata.get('dstaddr') != "":
              utmiptlineA += '-A %s -m set --match-set utmrule_src_%s src %s -m set --match-set utmrule_dst_%s dst %s -j %s\n' % (cdata.get('actzone'),cdata.get('id'),sportdesc,cdata.get('id'),dportdesc,cdata.get('runaction'))
           elif cdata.get('srcaddr') == "" and cdata.get('dstaddr') != "":
              utmiptlineA += '-A %s %s -m set --match-set utmrule_dst_%s dst %s -j %s\n' % (cdata.get('actzone'),sportdesc,cdata.get('id'),dportdesc,cdata.get('runaction'))
           elif cdata.get('srcaddr') != "" and cdata.get('dstaddr') == "":
                utmiptlineA += '-A %s -m set --match-set utmrule_src_%s src %s %s -j %s\n' % (cdata.get('actzone'),cdata.get('id'),sportdesc,dportdesc,cdata.get('runaction'))
           else:
                utmiptlineA += '-A %s %s %s -j %s\n' % (cdata.get('actzone'),sportdesc,dportdesc,cdata.get('runaction'))
           utmset = "create utmrule_src_%s hash:net family inet hashsize 1024 maxelem 65536\ncreate utmrule_dst_%s hash:net family inet hashsize 1024 maxelem 65536\n" % (cdata.get('id'),cdata.get('id'))
           utmsetline = ''
           for utmline in cdata.get('srcaddr').split('\n'):
               if utmline != "":
                  utmline = IPNetwork(utmline)
                  utmsetline += 'add utmrule_src_%s %s\n' % (cdata.get('id'),utmline)
           for utmline in cdata.get('dstaddr').split('\n'):
               if utmline != "":
                  utmline = IPNetwork(utmline)
                  utmsetline += 'add natrule_dst_%s %s\n' % (cdata.get('id'),utmline)
           utmsetline2 += utmset+utmsetline+'\n'
       aaa = re.sub(r'{{utmrulezone}}.*',utmsetline2, aaa)
       bbb = re.sub(r'{{utmrulezoneA}}.*',utmiptlineA, bbb)

       # 写NAT规则
       sql = " select id,srcaddr,dstmatch,dstaddr,runaction,runobject from ruleconfnat where status='1' "
       result = readDb(sql,)
       natiptlineA,natsetline2 = '',''
       for adata in result:
           if adata.get('dstmatch') == 0:
              dstmatch='!'
           else:
              dstmatch=''
           if adata.get('runobject') == "vpnrelay":
              runobject='tun1000'
           else:
              runobject=adata.get('runobject')
           if adata.get('srcaddr') != "" and adata.get('dstaddr') != "":
              if adata.get('runaction') == "SNAT":
                 natiptlineA += '-A POSTROUTING -m set --match-set natrule_src_%s src -m set %s --match-set natrule_dst_%s dst -j SNAT --to %s\n' % (adata.get('id'),dstmatch,adata.get('id'),runobject)
              else:
                 natiptlineA += '-A POSTROUTING -m set --match-set natrule_src_%s src -m set %s --match-set natrule_dst_%s dst -o %s -j MASQUERADE\n' % (adata.get('id'),dstmatch,adata.get('id'),runobject)
           elif adata.get('srcaddr') == "" and adata.get('dstaddr') != "":
              if adata.get('runaction') == "SNAT":
                 natiptlineA += '-A POSTROUTING -m set %s --match-set natrule_dst_%s dst -j SNAT --to %s' % (dstmatch,adata.get('id'),runobject)
              else:
                 natiptlineA += '-A POSTROUTING -m set %s --match-set natrule_dst_%s dst -o %s -j MASQUERADE\n' % (dstmatch,adata.get('id'),runobject)
           elif adata.get('srcaddr') != "" and adata.get('dstaddr') == "":
              if adata.get('runaction') == "SNAT":
                 natiptlineA += '-A POSTROUTING -m set --match-set natrule_src_%s src -j SNAT --to %s\n' % (adata.get('id'),runobject)
              else:
                 natiptlineA += '-A POSTROUTING -m set --match-set natrule_src_%s src -o %s -j MASQUERADE\n' % (adata.get('id'),runobject)
           else:
              if adata.get('runaction') == "SNAT":
                 natiptlineA += '-A POSTROUTING -j SNAT --to %s\n' % (runobject)
              else:
                 natiptlineA += '-A POSTROUTING -o %s -j MASQUERADE\n' % (runobject)
           natset = "create natrule_src_%s hash:net family inet hashsize 1024 maxelem 65536\ncreate natrule_dst_%s hash:net family inet hashsize 1024 maxelem 65536\n" % (adata.get('id'),adata.get('id'))
           natsetline = ''
           for natline in adata.get('srcaddr').split('\n'):
               if natline != "":
                  natline = IPNetwork(natline)
                  natsetline += 'add natrule_src_%s %s\n' % (adata.get('id'),natline)
           for natline in adata.get('dstaddr').split('\n'):
               if natline != "":
                  natline = IPNetwork(natline)
                  natsetline += 'add natrule_dst_%s %s\n' % (adata.get('id'),natline)
           natsetline2 += natset+natsetline+'\n'
       aaa = re.sub(r'{{natrulezone}}.*',natsetline2, aaa)
       bbb = re.sub(r'{{natrulezoneA}}.*',natiptlineA, bbb)
       # 写VPN策略规则
       sql = " select id,pushdns,pushroute,pushnoroute from vpnpolicy "
       result = readDb(sql,)
       ipsetline4,vpniptlineA,vpniptlineB,vpniptlineC = '','','',''
       for sdata in result:
           #vpniptlineA += '-A POSTROUTING -m set --match-set vpnpolicy_src_%s src -o tun1000 -j MASQUERADE\n' % sdata.get('id')
           vpniptlineB += '-A FORWARD -m set --match-set vpnpolicy_src_%s src -j vpnpolicy_%s\n' % (sdata.get('id'),sdata.get('id'))
           vpniptlineC += ':vpnpolicy_%s - [0:0]\n' % sdata.get('id')
           vpnsetline = ''
           vpnset = """create vpnpolicy_src_%s hash:net family inet hashsize 1024 maxelem 65536\ncreate vpnpolicy_net_%s hash:net family inet hashsize 1024 maxelem 65536\ncreate vpnpolicy_local_%s hash:net family inet hashsize 1024 maxelem 65536 """ % (sdata.get('id'),sdata.get('id'),sdata.get('id'))
           if sdata.get('pushroute') != "" and sdata.get('pushnoroute') != "":
              vpniptlineB += '-A vpnpolicy_%s -m set --match-set vpnpolicy_net_%s dst -j ACCEPT\n-A vpnpolicy_%s -j DROP\n' % (sdata.get('id'),sdata.get('id'),sdata.get('id'))
              vpnstr = sdata.get('pushdns')+'\n'+sdata.get('pushroute')
              for vpnline in vpnstr.split('\n'):
                  vpnline = IPNetwork(vpnline)
                  vpnsetline += 'add vpnpolicy_net_%s %s\n' % (sdata.get('id'),vpnline)
              for vpnline in sdata.get('pushnoroute').split('\n'):
                  vpnline = IPNetwork(vpnline)
                  vpnsetline += 'add vpnpolicy_local_%s %s\n' % (sdata.get('id'),vpnline)
           elif sdata.get('pushroute') != "" and sdata.get('pushnoroute') == "":
              vpniptlineB += '-A vpnpolicy_%s -m set --match-set vpnpolicy_net_%s dst -j ACCEPT\n-A vpnpolicy_%s -j DROP\n' % (sdata.get('id'),sdata.get('id'),sdata.get('id'))
              vpnstr = sdata.get('pushdns')+'\n'+sdata.get('pushroute')
              for vpnline in vpnstr.split('\n'):
                  vpnline = IPNetwork(vpnline)
                  vpnsetline += 'add vpnpolicy_net_%s %s\n' % (sdata.get('id'),vpnline)
           elif sdata.get('pushroute') == "" and sdata.get('pushnoroute') != "":
              vpniptlineB += '-A vpnpolicy_%s -m state --state RELATED,ESTABLISHED -j ACCEPT\n-A vpnpolicy_%s -m set --match-set vpnpolicy_local_%s dst -j DROP\n-A vpnpolicy_%s -j ACCEPT\n' % (sdata.get('id'),sdata.get('id'),sdata.get('id'),sdata.get('id'))
              for vpnline in sdata.get('pushnoroute').split('\n'):
                  vpnline = IPNetwork(vpnline)
                  vpnsetline += 'add vpnpolicy_local_%s %s\n' % (sdata.get('id'),vpnline)
           else:
              vpniptlineB += '-A vpnpolicy_%s -j ACCEPT\n' % sdata.get('id')
           ipsetline4 += vpnset+'\n'+vpnsetline+'\n'
       aaa = re.sub(r'{{vpnpolicyzone}}.*',ipsetline4, aaa)
       #bbb = re.sub(r'{{vpnpolicyzoneA}}.*',vpniptlineA, bbb)
       bbb = re.sub(r'{{vpnpolicyzoneB}}.*',vpniptlineB, bbb)
       bbb = re.sub(r'{{vpnpolicyzoneC}}.*',vpniptlineC, bbb)
       # 写入本地网络
       subnet=''
       info = cmds.getdictrst('ip route|awk \'/^[0-9].*\//{if($1!="169.254.0.0/16") print $1}\'')
       for sysnet in info.get('result').split('\n'):
           if sysnet != "":
              subnet += 'add localnet %s\n' % sysnet
       aaa = re.sub(r'{{localnetzone}}.*',subnet, aaa)
       # 处理DNS强制代理
       sql = " select value from sysattr where servattr='dnsmasq' and attr='dnsconf' "
       result = readDb(sql,)
       for data in result:
           idata = eval(data.get('value'))
           # DNS IPTABLES
           if idata.get('dnsproxy') == "1" :
              dnsproxy='-A PREROUTING -p udp -m udp --dport 53 -m comment --comment "DNSPROXY" -j REDIRECT --to-ports 53'
           else:
              dnsproxy=""
           bbb = re.sub(r'{{dnsproxyzone}}.*',dnsproxy, bbb)
       # 处理高级路由IPSET+IPTABLES
       sql = " select id,srcaddr,destaddr,pronum,iface from sysrouteadv order by pronum"
       result2 = readDb(sql,)
       for data in result2:
           src_set_sub,dst_set_sub,src_set,dst_set,srcipt,dstipt = '','','','','',''
           #当源地址或目地地址都为空时，忽略写入ipset+iptables
           if data.get('srcaddr') == "" and data.get('destaddr') == "" :
              continue
           #当源地址或目地地址两者均不为空的情况
           if data.get('srcaddr') != "":
              for subdata in data.get('srcaddr').split('\n'):
                  subdata = IPNetwork(subdata)
                  src_set_sub = src_set_sub+'\n'+'add advroute_src_%s %s' % (data.get('id'),subdata)
              srcipt = '-m set --match-set advroute_src_%s src' % data.get('id')
              src_set = 'create advroute_src_%s hash:net family inet hashsize 1024 maxelem 65536' % data.get('id')
           if data.get('destaddr') != "":
              for subdata in data.get('destaddr').split('\n'):
                  subdata = IPNetwork(subdata)
                  dst_set_sub = dst_set_sub+'\n'+'add advroute_dst_%s %s' % (data.get('id'),subdata)
              dstipt = '-m set --match-set advroute_dst_%s dst' % data.get('id')
              dst_set = 'create advroute_dst_%s hash:net family inet hashsize 1024 maxelem 65536' % data.get('id')
           ipsetline = ipsetline+'\n'+src_set+src_set_sub+'\n'+dst_set+dst_set_sub+'\n'
           iptline= iptline+'\n'+'-A Policy_Route %s %s -j MARK --set-mark 1000%s\n-A Policy_Route %s %s -j RETURN' % (srcipt,dstipt,data.get('id'),srcipt,dstipt)
       aaa = re.sub(r'{{advroutezone}}.*',ipsetline, aaa)
       bbb = re.sub(r'{{advroutezone}}.*',iptline, bbb)
       open(newfo,'w+').write(aaa)
       open(newfo2,'w+').write(bbb)
    if kwargs.get('tempiptconf') != True :
       cmds.servboot('firewall')

# 操作日志
def wrtlog(objname,objact,objtext,objhost):
    from MySQL import writeDb
    wrttime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    sql = " INSERT INTO logrecord(objtime,objname,objact,objtext,objhost) VALUES(%s,%s,%s,%s,%s) "
    data = (wrttime,objname,objact,objtext,objhost)
    result = writeDb(sql,data)
    if result != True:
       logging.debug(data)

# sendmail
def sendmail(subject,content):
    from smtplib import SMTP,SMTP_SSL
    from email.header import Header
    from email.mime.text import MIMEText
    emHost = AppServer().getConfValue('Email','emHost')
    emPort = AppServer().getConfValue('Email','emPort')
    emUser = AppServer().getConfValue('Email','emUser')
    emPass = AppServer().getConfValue('Email','emPass')
    emFrom = AppServer().getConfValue('Email','emFrom')
    emSSL = AppServer().getConfValue('Email','emSSL')
    emTo = 'master@lnmos.com'
    if emSSL == 'True' :
       try:
          smtp = SMTP_SSL(emHost,int(emPort),timeout=3)
       except:
          return 1
    else: 
       try:
          smtp = SMTP(emHost,int(emPort),timeout=3)
       except:
          return 1
    #smtp.set_debuglevel(1)
    smtp.ehlo(emHost)
    try:
       smtp.login(emUser, emPass)
    except:
       return 2
    #MIMEText：[mailcode: plain/html; mailencode: gb2312/utf-8]
    msg = MIMEText(content, "html", 'utf-8')
    msg["Subject"] = Header(subject, 'utf-8')
    msg["from"] = emFrom
    msg["to"] = emTo
    
    smtp.sendmail(emFrom, emTo, msg.as_string())
    smtp.quit()
    return 0

# APP get API
class getAPIData(object):
      def getUserLineID(self,uuid):
          from MySQL import writeDb,readDb
          sql = " select policy from user where username=%s "
          result = readDb(sql,(uuid,))
          if result:
             return result[0].get('policy')
          else:
             return 0

# 程序守护进程执行处理
from threading import Timer,Thread
class runDaemonTask(object):
    #def __new__(cls):
    #    if not hasattr(cls,'instance'):
    #        cls.instance = super(ResMonitor,cls).__new__(cls)
    #    return cls.instance

    def __init__(self):
        # 数据库连接
        from MySQL import testDB
        if testDB() == False :
           print "DB Connect Failure"
           os._exit(0)
        #初始化服务
        self.createTask('InitService')
        #动态处理UTM规则
        self.createTask('rundyUTM')
        #资源监控
        self.createTask('ResMonitor')
        #VPN持续连接
        self.createTask('chkVPNConn')

    def createTask(self,taskfun):
        t=Thread(target=eval('self.%s' % taskfun))
        t.setDaemon(True)
        t.start()

    def ResMonitor(self):
        from MySQL import writeDb,readDb
        # 获取资源监控配置参数值
        sql = " select value from sysattr where attr='resData' "
        info = readDb(sql,)
        try:
           ninfo=json.loads(info[0].get('value'))
        except:
           return False
        self.state = ninfo.get('ResState')
        self.saveDay = int(ninfo.get('ResSaveDay'))
        self.inv = int(ninfo.get('ResInv'))
        # 执行脚本循环判断
        sqlinsert = " insert into sysinfo (INFO,TIM) VALUES (%s,%s) "
        sqldelete = " delete from sysinfo where TIM < %s "
        memoryTotal = round(psutil.virtual_memory().total/(1024.0*1024.0*1024.0), 2)
        while True :
            time.sleep(self.inv)
            if not self.state:
               continue
            #CPU信息
            cpuUsed = psutil.cpu_percent(1)
            #内存信息 
            memoryInfo = psutil.virtual_memory()
            memoryUsedSize = round(memoryInfo.used / (1024.0*1024.0*1024.0),2)
            memoryUsed = round(memoryUsedSize/memoryTotal,2)*100
            #网络io
            net = psutil.net_io_counters()
            bytesRcvd = (net.bytes_recv / 1024)
            bytesSent = (net.bytes_sent / 1024)
            time.sleep(1)
            net = psutil.net_io_counters()
            realTimeRcvd = round(((net.bytes_recv / 1024) - bytesRcvd),2)
            realTimeSent = round(((net.bytes_sent / 1024) - bytesSent),2)
            #VPN在线
            cmd=''' occtl show sessions all|grep 'authenticated'|wc -l '''
            try:
               cmd_status,cmd_result=cmds.gettuplerst(cmd)
            except: 
                cmd_result == 0
            #分割线
            tim = time.strftime('%H:%M:%S',time.localtime())
            realTimeInfo = {
            'cpu':{'cpuUsed':cpuUsed},
            'memory':{'memoryUsed':memoryUsed},
            'net':{'rcvd':realTimeRcvd,'send':realTimeSent},
            'vpn':{'vpnUsed':int(cmd_result)}
            }
            insertdata = (json.dumps(realTimeInfo),time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()))
            writeDb(sqlinsert,insertdata)
            deletedata = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()-(int(self.saveDay) * 86400)))
            writeDb(sqldelete,(deletedata,))
            #print(realTimeInfo)

    def InitService(self):
        # 判断系统32 or 64
        if platform.machine() == 'AMD64':
           cmds.gettuplerst('ln -fs %s/sbin/busybox-x86_64 %s/sbin/busybox' % (gl.get_value('wkdir'),gl.get_value('wkdir')))
        elif platform.machine() == 'x86_64':
           cmds.gettuplerst('ln -fs %s/sbin/busybox-x86_64 %s/sbin/busybox' % (gl.get_value('wkdir'),gl.get_value('wkdir')))
        else:
           cmds.gettuplerst('ln -fs %s/sbin/busybox_i686 %s/sbin/busybox' % (gl.get_value('wkdir'),gl.get_value('wkdir')))
        # 初始化网络配置
        logging.debug('System Boot Service : NETWORKS ')
        writeNIconf(action='uptconf')
        writeROUTEconf(action='uptconf')
        cmds.servboot('networks')
        # DNS服务检测
        logging.debug('System Boot Service : DNSMASQ ')
        writeDNSconf(action='uptconf')
        cmds.servboot('dnsmasq',action='start')
        # 启动防火墙策略
        logging.debug('System Boot Service : FireWALL ')
        writeUTMconf(action='uptconf')
        cmds.servboot('firewall')
        # 启动VPN客户端连接
        logging.debug('System Boot Service : VPNServ ')
        writeVPNconf(action='uptcltconf')
        cmds.servboot('vpnconn')
        # 启动VPN服务端连接
        logging.debug('System Boot Service : VPNConn ')
        writeVPNconf(action='uptconf')
        cmds.servboot('ocserv')

    def rundyUTM(self):
        while True:
           time.sleep(10)
           ipt=GetFileMd5('%s/firewall/iptables.conf' % gl.get_value('plgdir'))
           ipt2=GetFileMd5('%s/firewall/ipset.conf' % gl.get_value('plgdir'))
           writeUTMconf(action='uptconf',tempiptconf=True)
           tipt=GetFileMd5('/tmp/iptables.conf')
           tipt2=GetFileMd5('/tmp/ipset.conf')
           #开机第一次强制启动防火墙
           if ( ipt != tipt and tipt != False ) or ( ipt2 != tipt2 and tipt2 != False ):
              #logging.debug('%s %s %s %s' % (ipt,tipt,ipt2,tipt2))
              logging.debug('found firewall rule is change, please wait on!')
              writeUTMconf(action='uptconf')
              cmds.servboot('firewall')

    def chkVPNConn(self):
        while True:
           time.sleep(30)
           from MySQL import readDb
           sqldesc = "select value from sysattr where attr='vpnclient'"
           resultconn = readDb(sqldesc,)
           try:
              ninfo=json.loads(resultconn[0].get('value'))
           except:
              continue
           if ninfo.get('authtype') == "0" or ninfo.get('authtype') == "1" :
              if ninfo.get('chkconn') == "1" and netmod.getNiaddr('tun1000') ==  False:
                 logging.debug('check vpnconn server error, server reboot, please wait on')
                 cmds.servboot('networks',action='uptconf')
                 time.sleep(5)
                 cmds.servboot('vpnconn')

if __name__ == '__main__' :
   sys.exit()
