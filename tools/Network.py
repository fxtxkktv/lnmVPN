#!/usr/bin/env python
#coding=utf-8
import os,sys,json,re,logging,time,datetime,hashlib
from bottle import request,route,error,run,default_app
from bottle import template,static_file,redirect,abort
import bottle

from MySQL import writeDb,readDb
from Login import checkLogin,checkAccess

from Functions import cmdhandle,netModule,writeNIconf,writeUTMconf,writeDNSconf,writeROUTEconf

cmds = cmdhandle()
netmod = netModule()

@route('/networkconf')
@checkAccess
def networkconf():
    s = request.environ.get('beaker.session')
    #清理所有网卡信息，重新获取最新的系统网卡信息
    sql = "delete from sysattr where servattr='netiface'"
    writeDb(sql,)
    netmod.InitNIinfo()
    netmod.getifaceData('getni')
    return template('networkconf',session=s,msg={})

@route('/api/getifaceinfo',method=['GET', 'POST'])
@checkAccess
def getifaceinfo():
    sql = " SELECT id,ifacename,ifacetype,ipaddr,netmask,gateway,rxdata,txdata,status FROM netiface "
    iface_list = readDb(sql,)
    return json.dumps(iface_list)

@route('/addinterface')
@checkAccess
def addinterface():
    s = request.environ.get('beaker.session')
    # 初始化网卡添加状态，已经被配置的网卡，无法再次配置
    sqla = " select attr from sysattr where status='1' and servattr='netiface' and attr not in (select ifacename from netiface) "
    erriface = readDb(sqla,)
    if len(erriface) > 0 :
       for x in erriface:
           sqlb = "update sysattr set status='1' where attr=%s and servattr='netiface'"
           writeDb(sqlb,(x.get('attr'),))
    sqlc = " select attr from sysattr where status='1' and servattr='netiface' and attr in (select ifacename from netiface) "
    erriface2 = readDb(sqlc,)
    if len(erriface2) > 0 :
       for y in erriface2:
           sqld = "update sysattr set status='0' where attr=%s and servattr='netiface'"
           writeDb(sqld,(y.get('attr'),))
    # 判断接口是否被锁定或已配置
    sqld = " SELECT attr as ifacename,concat(attr,'|',value) as value FROM sysattr where servattr='netiface' and status='1' order by attr desc"
    ifacelist_result = readDb(sqld,)
    if len(ifacelist_result) == 0 :
       msg = {'color':'red','message':u'无可用物理接口,添加失败'}
       return(template('networkconf',session=s,msg=msg))
    return template('addinterface',session=s,info={},ifacelist_result=ifacelist_result)

@route('/addinterface',method="POST")
@checkAccess
def do_additem():
    s = request.environ.get('beaker.session')
    ifacename = request.forms.get("ifacename")
    ifacetype = request.forms.get("ifacetype")
    ifacezone = request.forms.get("ifacezone")
    if ifacetype == 'ADSL' :
       username = request.forms.get("username")
       password = request.forms.get("password")
       mtu = request.forms.get("mtu")
       defaultgw = request.forms.get("defaultgwB")
    else :
       ipaddr = request.forms.get("ipaddr")
       netmask = request.forms.get("netmask")
       gateway = request.forms.get("gateway")
       extip = request.forms.get("extip").replace('\r\n','\n')
       defaultgw = request.forms.get("defaultgwA")
    osize = request.forms.get("osize")
    if ifacetype == 'STATIC' :
      # 固定IP类型：判断填写网关和没有填写网关的情况
      if ipaddr == '' or netmask == '' :
         msg = {'color':'red','message':u'地址不合法,添加失败'}
         return(template('networkconf',session=s,msg=msg))
      if gateway != '' :
         if netmod.checkip(ipaddr) == False or netmod.checkmask(netmask) == False or netmod.checkip(gateway) == False or netmod.checknet(gateway,ipaddr,netmask) == False :
            msg = {'color':'red','message':u'地址不合法,添加失败'}
            return(template('networkconf',session=s,msg=msg))
      else :
         if netmod.checkip(ipaddr) == False or netmod.checkmask(netmask) == False :
            msg = {'color':'red','message':u'地址不合法,添加失败'}
            return(template('networkconf',session=s,msg=msg))
      for extlist in extip.split('\n'):
        if len(extlist.split('/')) == 3:
           extsip=extlist.split('/')[0]
           extmask=extlist.split('/')[1]
           extgw=extlist.split('/')[2]
           if netmod.checkip(extsip) == False or netmod.checkmask(extmask) == False or netmod.checkip(extgw) == False or netmod.checknet(extgw,extsip,extmask) == False :
              msg = {'color':'red','message':u'扩展IP地址不合法,更新失败'}
              return(template('networkconf',session=s,msg=msg))
        elif len(extlist.split('/')) == 2:
           extsip=extlist.split('/')[0]
           extmask=extlist.split('/')[1]
           if netmod.checkip(extsip) == False or netmod.checkmask(extmask) == False :
              msg = {'color':'red','message':u'扩展IP地址不合法,更新失败'}
              return(template('networkconf',session=s,msg=msg))
           elif extlist == u'':
              True
           else :
              msg = {'color':'red','message':u'扩展IP地址不合法,更新失败'}
              return(template('networkconf',session=s,msg=msg))
    else :
        if int(mtu) % 4 != 0 :
           msg = {'color':'red','message':u'MTU值不合法,更新失败'}
           return(template('networkconf',session=s,msg=msg))
        

    if ifacename == u'' :
       msg = {'color':'red','message':u'物理接口未选择,添加失败'}
       return(template('networkconf',session=s,msg=msg))

    if ifacetype == 'STATIC' :
       sql = "INSERT INTO netiface (ifacename,ifacetype,ifacezone,ipaddr,netmask,gateway,defaultgw,extip,osize) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
       data = (ifacename,ifacetype,ifacezone,ipaddr,netmask,gateway,defaultgw,extip,osize)
       result = writeDb(sql,data)
    else :
       sql = "INSERT INTO netiface (ifacename,ifacetype,ifacezone,username,password,mtu,defaultgw,osize) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
       data = (ifacename,ifacetype,ifacezone,username,password,mtu,defaultgw,osize)
       result = writeDb(sql,data)

    if result == True:
       writeNIconf(action='uptconf')
       cmds.servboot('networks',action='uptconf')
       writeUTMconf(action='uptconf')
       msg = {'color':'green','message':u'添加成功'}
       #已绑定的网卡禁止再次绑定
       sql2 = """ update sysattr set status="0" where attr=%s """
       writeDb(sql2,(ifacename,))
    else:
       msg = {'color':'red','message':u'添加失败'}
    return template('networkconf',session=s,msg=msg)

@route('/rebootif/<id>')
@checkAccess
def do_chgstatus(id):
    s = request.environ.get('beaker.session')
    sql = """ select ifacename,ifacetype from netiface where id=%s """
    msg = {'color':'green','message':u'接口已成功重启'}
    itfinfo=readDb(sql,(id,))
    if itfinfo[0].get('ifacetype') == 'ADSL':
       cmds.gettuplerst('ps aux|grep -e \'xdsl.*%s\'|grep -v grep|awk \'{print $2}\' |xargs -i kill -9 {}' % id)
       cmds.gettuplerst('ip link set ppp%s down' % itfinfo[0].get('id'))
    cmds.gettuplerst('ip link set %s down' % itfinfo[0].get('ifacename'))
    cmds.servboot('networks',action='uptconf')
    return template('networkconf',session=s,msg=msg)


@route('/editiface/<id>')
@checkAccess
def editiface(id):
    s = request.environ.get('beaker.session')
    sql = " SELECT ifacename,ifacetype,ifacezone,ipaddr,netmask,gateway,defaultgw,extip,username,password,mtu,osize FROM netiface WHERE id = %s "
    sql2 = "select attr as ifacename,concat(attr,'|',value) as value from sysattr where attr=(select ifacename from netiface where id=%s);"
    info = readDb(sql,(id,))
    ifacelist_result = readDb(sql2,(id,))
    if not ifacelist_result:
        abort(404)
    if ifacelist_result[0].get('userid') != s.get('userid',None) and s.get('access',None) == 0:
        abort(404)
    return template('addinterface',session=s,info=info[0],ifacelist_result=ifacelist_result)

@route('/editiface/<id>',method="POST")
@checkAccess
def do_editiface(id):
    s = request.environ.get('beaker.session')
    ifacename = request.forms.get("ifacename")
    ifacetype = request.forms.get("ifacetype")
    ifacezone = request.forms.get("ifacezone")
    if ifacetype == 'ADSL' :
       username = request.forms.get("username")
       password = request.forms.get("password")
       mtu = request.forms.get("mtu")
       defaultgw = request.forms.get("defaultgwB")
    else :
       ipaddr = request.forms.get("ipaddr")
       netmask = request.forms.get("netmask")
       gateway = request.forms.get("gateway")
       extip = request.forms.get("extip").replace('\r\n','\n')
       defaultgw = request.forms.get("defaultgwA")
    osize = request.forms.get("osize")
    # 判断提交异常
    if ifacetype == 'STATIC' :
      if ipaddr == '' or netmask == '' :
         msg = {'color':'red','message':u'地址不合法,添加失败'}
         return(template('networkconf',session=s,msg=msg))
      if gateway != '' :
         if netmod.checkipmask('%s/%s' % (ipaddr,netmask)) == False or netmod.checknet(gateway,ipaddr,netmask) == False :
           msg = {'color':'red','message':u'地址不合法,添加失败%s,%s,%s' % (gateway,ipaddr,netmask)}
           return(template('networkconf',session=s,msg=msg))
      else :
         if netmod.checkip(ipaddr) == False or netmod.checkmask(netmask) == False :
            msg = {'color':'red','message':u'地址不合法,添加失败'}
            return(template('networkconf',session=s,msg=msg))

      for extlist in extip.split('\n'):
         if len(extlist.split('/')) == 3:
            extsip=extlist.split('/')[0]
            extmask=extlist.split('/')[1]
            extgw=extlist.split('/')[2]
            if netmod.checkip(extsip) == False or netmod.checkmask(extmask) == False or netmod.checkip(extgw) == False or netmod.checknet(extgw,extsip,extmask) == False :
               msg = {'color':'red','message':u'扩展IP地址不合法,更新失败'}
               return(template('networkconf',session=s,msg=msg))
         elif len(extlist.split('/')) == 2:
            extsip=extlist.split('/')[0]
            extmask=extlist.split('/')[1]
            if netmod.checkip(extsip) == False or netmod.checkmask(extmask) == False :
               msg = {'color':'red','message':u'扩展IP地址不合法,更新失败'}
               return(template('networkconf',session=s,msg=msg))
         elif extlist == u'':
              True
         else :
            msg = {'color':'red','message':u'扩展IP地址不合法,更新失败'}
            return(template('networkconf',session=s,msg=msg))
    else :
        if int(mtu) % 4 != 0 :
           msg = {'color':'red','message':u'MTU值不合法,更新失败'}
           return(template('networkconf',session=s,msg=msg))

    if ifacename == u'' :
       msg = {'color':'red','message':u'物理接口未选择,更新失败'}
       return(template('addinterface',session=s,msg=msg))

    if ifacetype == 'STATIC' :
       sql = "UPDATE netiface SET ifacename=%s,ifacetype=%s,ifacezone=%s,ipaddr=%s,netmask=%s,gateway=%s,defaultgw=%s,extip=%s,osize=%s WHERE id=%s"
       data = (ifacename,ifacetype,ifacezone,ipaddr,netmask,gateway,defaultgw,extip,osize,id)
       result = writeDb(sql,data)
    else :
       sql = "UPDATE netiface SET ifacename=%s,ifacetype=%s,ifacezone=%s,username=%s,password=%s,mtu=%s,defaultgw=%s,osize=%s WHERE id=%s"
       data = (ifacename,ifacetype,ifacezone,username,password,mtu,defaultgw,osize,id)
       result = writeDb(sql,data)

    if result == True:
       writeNIconf(action='uptconf')
       cmds.servboot('networks',action='uptconf')
       writeUTMconf(action='uptconf')
       msg = {'color':'green','message':u'更新成功'}
    return template('networkconf',session=s,msg=msg)

@route('/deliface/<id>')
@checkAccess
def deliface(id):
    s = request.environ.get('beaker.session')
    sql = " DELETE FROM netiface WHERE id=%s "
    sql2 = " select ifacename FROM netiface WHERE id=%s "
    ifacename = readDb(sql2,(id,))
    result = writeDb(sql,(id,))
    if result == True :
       writeNIconf(action='uptconf')
       cmds.servboot('networks',action='uptconf')
       writeUTMconf(action='uptconf')
       msg = {'color':'green','message':u'删除成功'}
       cmds.gettuplerst('ip addr flush dev %s' % ifacename[0].get('ifacename'))
       #如果是PPP类型接口，停用ADSL
       cmds.gettuplerst('ip link set %s down' % ifacename[0].get('ifacename'))
       cmds.gettuplerst('ps aux|grep -e \'xdsl.*%s\'|grep -v grep|awk \'{print $2}\' |xargs -i kill -9 {}' % id)
       #恢复绑定
       sql2 = "update sysattr set status='1' where attr=%s"
       writeDb(sql2,(ifacename[0].get('ifacename'),))
       return template('networkconf',session=s,msg=msg)
    else:
       msg = {'color':'red','message':u'删除失败'}
       return template('networkconf',session=s,msg=msg)

# DNS配置
@route('/dnsservconf')
@checkAccess
def dnsservconf():
    s = request.environ.get('beaker.session')
    return template('dnsservconf',session=s,msg={},info={})

@route('/adddnsconf')
@checkAccess
def adddnsconf():
    s = request.environ.get('beaker.session')
    msg = {'action':'accept'}
    return(template('adddnsconf',session=s,msg=msg,info={}))

@route('/adddnsconf',method="POST")
@checkAccess
def do_adddnsconf():
    s = request.environ.get('beaker.session')
    dnstype = request.forms.get("dnstype")
    domain = request.forms.get("domainA")
    record = request.forms.get("record")
    pronum = request.forms.get("pronum")
    if dnstype == 'NULL' :
       msg = {'color':'red','message':'请选择记录类型'}
       return(template('adddnsconf',session=s,msg=msg,info={}))
    if dnstype == 'MX' and netmod.is_domain(record) == False :
       msg = {'color':'red','message':'记录数据格式错误'}
       return(template('adddnsconf',session=s,msg=msg,info={}))
    if dnstype == 'CNAME' and netmod.is_domain(record) == False :
       msg = {'color':'red','message':'记录数据格式错误'}
       return(template('adddnsconf',session=s,msg=msg,info={}))
    if dnstype == 'A' and netmod.checkip(record) == False :
       msg = {'color':'red','message':'记录数据格式错误'}
       return(template('adddnsconf',session=s,msg=msg,info={}))
    if dnstype == 'PTR' and netmod.checkip(domain) == False :
       msg = {'color':'red','message':'数据格式错误'}
       return(template('adddnsconf',session=s,msg=msg,info={}))
    if dnstype == 'SET':
       domain = request.forms.get("domainB").replace('\r\n','\n').strip()
       if domain != "":
          for domains in domain.split('\n'):
             if netmod.is_domain(domains) == False:
                msg = {'color':'red','message':'记录数据格式错误'}
                return(template('adddnsconf',session=s,msg=msg,info={}))

    sql = "insert into dnsrecord (dnstype,domain,data,pronum) VALUE (%s,%s,%s,%s)"
    data = (dnstype,domain,record,pronum)
    result = writeDb(sql,data)
    if result == True:
       #如果含SET记录,写入网络对象
       if dnstype == 'SET':
          sql=" insert into netobjgroup (objname,objtype,objattr) value (%s,%s,'0')"
          data=(record,'ipset')
          writeDb(sql,data)
       writeDNSconf(action='uptconf')
       msg = {'color':'green','message':'提交成功'}
       return(template('dnsservconf',session=s,msg=msg,info={}))
    else :
       msg = {'color':'red','message':'保存失败'}
       return(template('dnsservconf',session=s,msg=msg,info={}))


@route('/editrecord/<id>')
@checkAccess
def editrecord(id):
    s = request.environ.get('beaker.session')
    sql = " select dnstype,domain,data as record,pronum from dnsrecord where id=%s "
    result = readDb(sql,(id,))
    msg = {'action':'accept'}
    if result[0].get('dnstype') == "SET":
       #当类型为ipset时，禁止编辑记录数据，仅支持删除或更新域名列表
       msg = {'action':'reject'}
    return(template('adddnsconf',session=s,msg=msg,info=result[0]))

@route('/editrecord/<id>',method="POST")
@checkAccess
def do_editrecord(id):
    s = request.environ.get('beaker.session')
    dnstype = request.forms.get("dnstype")
    domain = request.forms.get("domainA")
    record = request.forms.get("record")
    pronum = request.forms.get("pronum")
    if dnstype == 'NULL' :
       msg = {'color':'red','message':'请选择记录类型'}
       return(template('adddnsconf',session=s,msg=msg,info={}))
    if dnstype == 'MX' and netmod.is_domain(record) == False :
       msg = {'color':'red','message':'记录数据格式错误'}
       return(template('adddnsconf',session=s,msg=msg,info={}))
    if dnstype == 'CNAME' and netmod.is_domain(record) == False :
       msg = {'color':'red','message':'记录数据格式错误'}
       return(template('adddnsconf',session=s,msg=msg,info={}))
    if dnstype == 'A' and netmod.checkip(record) == False :
       msg = {'color':'red','message':'记录数据格式错误'}
       return(template('adddnsconf',session=s,msg=msg,info={}))
    if dnstype == 'PTR' and netmod.checkip(domain) == False :
       msg = {'color':'red','message':'数据格式错误'}
       return(template('adddnsconf',session=s,msg=msg,info={}))
    if dnstype == 'SET':
       domain = request.forms.get("domainB").replace('\r\n','\n').strip()
       if domain != "":
          if len(domain.split('\n')) > 40:
             msg = {'color':'red','message':'域名行数太多，无法支持'}
             return(template('adddnsconf',session=s,msg=msg,info={}))
          for domains in domain.split('\n'):
             if netmod.is_domain(domains) == False:
                msg = {'color':'red','message':'记录数据格式错误'}
                return(template('adddnsconf',session=s,msg=msg,info={}))
    sql = "update dnsrecord set dnstype=%s,domain=%s,data=%s,pronum=%s where id=%s"
    data = (dnstype,domain,record,pronum,id)
    result = writeDb(sql,data)
    if result == True:
       writeDNSconf(action='uptconf')
       msg = {'color':'green','message':'更新成功'}
       return(template('dnsservconf',session=s,msg=msg,info={}))
    else :
       msg = {'color':'red','message':'更新失败'}
       return(template('dnsservconf',session=s,msg=msg,info={}))

@route('/editdnsserv')
@checkAccess
def editdnsserv():
    s = request.environ.get('beaker.session')
    sql = " select value from sysattr where attr='dnsconf' "
    idata = readDb(sql,)
    try:
       info = json.loads(idata[0].get('value'))
    except:
       return(template('editdnsserv',session=s,msg={},info={}))
    info['dnsport']=53
    info['dnsstatus']=cmds.servchk(info.get('dnsport'))
    return(template('editdnsserv',session=s,msg={},info=info))

@route('/editdnsserv',method="POST")
@checkAccess
def do_editdnsserv():
    s = request.environ.get('beaker.session')
    dnsrelay = request.forms.get("dnsrelay")
    dnsproxy = request.forms.get("dnsproxy")
    dnsrule = request.forms.get("dnsrule")
    dnslist = request.forms.get("dnslist").replace('\r\n','\n').strip()
    idata = dict()
    idata['dnsrelay']=dnsrelay
    idata['dnsproxy']=dnsproxy
    idata['dnsrule']=dnsrule
    idata['dnslist']=dnslist
    idata['dnsport']=53
    dnsstatus=cmds.servchk(idata.get('dnsport'))
    idata['dnsstatus']=dnsstatus
    sql = " update sysattr set value=%s where attr='dnsconf' "
    iidata=json.dumps(idata)
    result = writeDb(sql,(iidata,))
    if result == True :
       writeDNSconf(action='uptconf')
       writeROUTEconf(action='uptconf')
       writeUTMconf(action='uptconf')
       msg = {'color':'green','message':'配置保存成功'}
       return(template('editdnsserv',session=s,msg=msg,info=idata))
    else :
       msg = {'color':'red','message':'配置保存失败'}
       sql = " select value from sysattr where attr='dnsconf' "
       idata = readDb(sql,)	
       return(template('editdnsserv',session=s,msg=msg,info=idata))

@route('/delrecord/<id>')
@checkAccess
def delrecord(id):
    s = request.environ.get('beaker.session')
    sql = "delete from dnsrecord where id in (%s) "
    result = writeDb(sql,(id,))
    if result:
       writeDNSconf(action='uptconf')
       msg = {'color':'green','message':'删除成功'}
       return(template('dnsservconf',session=s,msg=msg,info={}))
    else:
       msg = {'color':'red','message':'删除失败'}
       return(template('dnsservconf',session=s,msg=msg,info={}))

@route('/api/getdnsrecord',method=['GET', 'POST'])
@checkAccess
def getifaceinfo():
    sql = " SELECT id,domain,dnstype,data,pronum FROM dnsrecord order by dnstype"
    info = readDb(sql,)
    return json.dumps(info)

# DHCP配置
@route('/dhcpservconf')
@checkAccess
def editdhcpserv():
    s = request.environ.get('beaker.session')
    sql = " select value from sysattr where attr='dhcpconf' "
    idata = readDb(sql,)
    try:
       info = idata[0].get('value')
    except:
       return(template('editdhcpserv',session=s,msg={},info={}))
    idata=json.loads(idata[0].get('value'))
    idata['dhcpport']=67
    idata['dhcpstatus']=cmds.servchk(idata.get('dhcpport'))
    return(template('editdhcpserv',session=s,msg={},info=idata))

@route('/dhcpservconf',method="POST")
@checkAccess
def do_editdhcpserv():
    s = request.environ.get('beaker.session')
    dhcpenable = request.forms.get("dhcpenable")
    getgw = request.forms.get("getgw")
    getdns1 = request.forms.get("getdns1")
    getdns2 = request.forms.get("getdns2")
    startip = request.forms.get("startip")
    stopip = request.forms.get("stopip")
    otime = request.forms.get("otime")
    dhcplist = request.forms.get("dhcplist").replace('\r\n','\n').strip()
    idata = dict()
    idata['dhcpenable']=dhcpenable
    idata['getgw']=getgw
    idata['getdns1']=getdns1
    idata['getdns2']=getdns2
    idata['startip']=startip
    idata['stopip']=stopip
    idata['otime']=otime
    if netmod.checkip(startip) == False or netmod.checkip(stopip) == False or netmod.checkip(getgw) == False or netmod.checkip(getdns1) == False:
       msg = {'color':'red','message':'参数配置异常，保存失败'}
       return(template('editdhcpserv',session=s,msg=msg,info=idata))
    #判断dhcp固定分配是否为空
    if dhcplist != "":
       for i in dhcplist.split('\n'):
           try:
              xmac = i.split(',')[0]
              xip = i.split(',')[1]
              if (netmod.is_ValidMac(xmac) == False or netmod.checkip(xip) == False) and xmac != "":
                 msg = {'color':'red','message':'配置保存失败,固定分配记录异常'}
                 return(template('editdhcpserv',session=s,msg=msg,info=idata))
              else:
                 idata['dhcplist']=dhcplist
           except:
              msg = {'color':'red','message':'配置保存失败,固定分配记录异常'}
              return(template('editdhcpserv',session=s,msg=msg,info=idata))
    sql = " update sysattr set value=%s where attr='dhcpconf' "
    iidata=json.dumps(idata)
    result = writeDb(sql,(iidata,))
    if result == True :
       writeDNSconf(action='uptconf')
       msg = {'color':'green','message':'配置保存成功'}
       return(template('editdhcpserv',session=s,msg=msg,info=idata))
    else :
       msg = {'color':'red','message':'配置保存失败'}
       sql = " select value from sysattr where attr='dhcpconf' "
       idata = readDb(sql,)
       return(template('editdhcpserv',session=s,msg=msg,info=idata))

@route('/ifdatashow')
@checkAccess
def ifdatashow():
    s = request.environ.get('beaker.session')
    sql = " SELECT ifacename FROM netiface where status='UP' UNION select value as ifacename FROM sysattr where status='1' and servattr='vpnrelay'"
    ifacelist_result = readDb(sql,)
    return(template('ifdatashow',session=s,msg={},iflist=ifacelist_result,sel=dict(),runresult=''))

@route('/ifdatashow',method="POST")
@checkAccess
def do_ifdatashow():
    s = request.environ.get('beaker.session')
    sel = {}
    sel['ifname'] = request.forms.get("ifname")
    sel['shownum'] = request.forms.get("shownum")
    sel['rftime'] = request.forms.get("rftime")
    x,runresult = cmds.gettuplerst('iftop -i %s -n -N -P -t -L %s -s %s' % (sel['ifname'],sel['shownum'],sel['rftime']))
    sql = " SELECT ifacename FROM netiface where status='UP' UNION select value as ifacename FROM sysattr where status='1' and servattr='vpnrelay'"
    ifacelist_result = readDb(sql,)
    return(template('ifdatashow',session=s,msg={},iflist=ifacelist_result,sel=sel,runresult=runresult))

if __name__ == '__main__' :
   sys.exit()
