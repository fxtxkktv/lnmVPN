#!/usr/bin/env python
#coding=utf-8
import os,sys,json,re,time,datetime,logging,zipfile,socket,platform
from bottle import request,route
from bottle import template,redirect,static_file

from MySQL import writeDb,readDb,readDb2
from Login import checkLogin,checkAccess

from Functions import AppServer,cmdhandle,netModule,writeVPNconf,writeROUTEconf,writeUTMconf
import Global as gl

cmds=cmdhandle()
netmod=netModule()

@route('/routeconf')
@checkAccess
def routeconf():
    s = request.environ.get('beaker.session')
    return template('routeconf',session=s,msg={})

@route('/staticroute')
@checkAccess
def routeconf():
    s = request.environ.get('beaker.session')
    return template('staticroute',msg={},session=s)

@route('/advroute')
@checkAccess
def routeconf():
    s = request.environ.get('beaker.session')
    return template('advroute',msg={},session=s)

@route('/showadvroute')
@checkAccess
def routeconf():
    s = request.environ.get('beaker.session')
    result = cmds.getdictrst('ip rule')
    return template('showlog',session=s,info=result)


@route('/api/getrouteinfo',method=['GET', 'POST'])
@checkAccess
def getrouteinfo():
    netmod.Initrouteinfo()
    sql = """ SELECT I.id, I.dest, I.netmask, I.gateway, I.iface FROM sysroute as I where fromtype=0 order by id """
    item_list = readDb(sql,)
    return json.dumps(item_list)

@route('/api/getrouteinfo2',method=['GET', 'POST'])
@checkAccess
def getrouteinfo():
    sql = """ SELECT I.id, I.dest, I.netmask, I.gateway, I.iface FROM sysroute as I where fromtype=1 """
    item_list = readDb(sql,)
    return json.dumps(item_list)

@route('/api/getrouteinfo3',method=['GET', 'POST'])
@checkAccess
def getrouteinfo():
    sql = """ SELECT U.id, U.rulename, U.pronum, concat(U.starttime,'-',U.stoptime) as stime, U.iface, D.value, 
              if(U.srcaddr="all","全部网络",concat(if(U.srcmatch=0,"! ",""),E.objname)) as srcaddr,
              if(U.dstaddr="all","全部网络",concat(if(U.dstmatch=0,"! ",""),F.objname)) as dstaddr
              FROM sysrouteadv as U LEFT OUTER JOIN sysattr as D on position(U.iface in D.attr) 
              LEFT OUTER JOIN netobjgroup as E on E.id=U.srcaddr LEFT OUTER JOIN netobjgroup as F on F.id=U.dstaddr
              order by pronum asc """
    info=[]
    item_list = readDb(sql,)
    for idict in item_list:
        idict['rtname']=json.loads(idict.get('value')).get('rtname')
        info.append(idict)
    return json.dumps(info)

@route('/addroute')
@checkAccess
def addroute():
    s = request.environ.get('beaker.session')
    sql = " SELECT ifacename FROM netiface "
    ifacelist_result = readDb(sql,)
    return template('addrouteconf',session=s,info={},ifacelist_result=ifacelist_result)

@route('/addroute',method="POST")
@checkAccess
def do_addroute():
    s = request.environ.get('beaker.session')
    rttype = request.forms.get("rttype")
    destaddr = request.forms.get("ipaddr")
    netmask = request.forms.get("netmask")
    gateway = request.forms.get("gateway")
    gwiface = request.forms.get("gwiface")
    # 格式判断
    if netmod.checkip(destaddr) == False or netmod.checkmask(netmask) == False or netmod.checkip(gateway) == False :
       msg = {'color':'red','message':u'地址不合法,添加失败'}
       return(template('staticroute',msg=msg,session=s))
    # 系统判断
    if gwiface == 'auto':
       resultA = cmds.getdictrst('route add -net %s netmask %s gw %s' % (destaddr,netmask,gateway))
    else :
       resultA = cmds.getdictrst('route add -net %s netmask %s gw %s dev %s' % (destaddr,netmask,gateway,gwiface))
    if resultA.get('status') != 0 :
       msg = {'color':'red','message':u'目标不可达或其他错误，添加失败'}
       return(template('staticroute',msg=msg,session=s))
    sql = "INSERT INTO sysroute(type,dest,netmask,gateway,iface,fromtype) VALUES(%s,%s,%s,%s,%s,%s)"
    data = ('net',destaddr,netmask,gateway,gwiface,1)
    result = writeDb(sql,data)
    if result == True:
       writeROUTEconf(action='uptconf')
       writeUTMconf(action='uptconf')
       msg = {'color':'green','message':u'添加成功'}
       return(template('staticroute',msg=msg,session=s))
    else:
       msg = {'color':'red','message':u'添加失败'}
       return(template('staticroute',msg=msg,session=s))

@route('/addadvroute')
@checkAccess
def addroute():
    s = request.environ.get('beaker.session')
    sql = """ select id,objname from netobjgroup where status='1' order by id """
    result = readDb(sql,)
    netmod.InitNIinfo()
    sql = " SELECT attr,value FROM sysattr where servattr='advroutepolicy' "
    iflist_result = readDb(sql,)
    infos=[]
    for idict in iflist_result:
        idict['attr']=idict.get('attr')
        idict['rtname']=json.loads(idict.get('value')).get('rtname')
        infos.append(idict)
    return template('addadvroute',session=s,info={},iflist=infos,setlist=result)

@route('/addadvroute',method="POST")
@checkAccess
def do_addroute():
    s = request.environ.get('beaker.session')
    rulename = request.forms.get("rulename")
    pronum = request.forms.get("pronum")
    starttime = request.forms.get("starttime")
    stoptime = request.forms.get("stoptime")
    outdev = request.forms.get("ifacename").replace('advpolicy_','')
    srcmatch = request.forms.get("srcmatch")
    if srcmatch == "2":
       srcaddr="all"
    else:
       srcaddr = (',').join(request.forms.getlist("srcaddr"))
    dstmatch = request.forms.get("dstmatch")
    if dstmatch == "2":
       dstaddr="all"
    else:
       dstaddr = (',').join(request.forms.getlist("dstaddr"))
    #提交判断
    if outdev == '' or rulename == '':
       msg = {'color':'red','message':u'描述或出口未填写，添加失败'}
       return(template('advroute',msg=msg,session=s))
    if int(pronum) <100 or int(pronum) >32765 :
       msg = {'color':'red','message':u'优先级值填写错误，添加失败'}
       return(template('advroute',msg=msg,session=s))
    cmdDict=cmds.getdictrst('ip rule add prio %s fwmark 1000 dev %s' % (pronum,outdev.replace('advpolicy_','')))
    if cmdDict.get('status') == 0:
       sql = """ insert into sysrouteadv(rulename,srcmatch,srcaddr,dstmatch,dstaddr,pronum,starttime,stoptime,iface) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s) """
       data = (rulename,srcmatch,srcaddr,dstmatch,dstaddr,int(pronum),starttime,stoptime,outdev)
       result = writeDb(sql,data)
       if result :
          writeROUTEconf(action='uptconf')
          writeUTMconf(action='uptconf')
          msg = {'color':'green','message':u'添加成功'}
       else :
          msg = {'color':'red','message':u'添加失败'}
    else:
       msg = {'color':'red','message':u'系统规则生成异常，添加失败'}
    return(template('advroute',msg=msg,session=s))

@route('/editadvroute/<id>')
@checkAccess
def editadvroute(id):
    s = request.environ.get('beaker.session')
    sql = """ select id,objname from netobjgroup where status='1' order by id"""
    result = readDb(sql,)
    sql2 = """ SELECT attr,value FROM sysattr where servattr='advroutepolicy' """
    iflist_result = readDb(sql2,)
    infos=[]
    for idict in iflist_result:
        idict['attr']=idict.get('attr')
        idict['rtname']=json.loads(idict.get('value')).get('rtname')
        infos.append(idict)
    sql2 = """ SELECT rulename,srcmatch,srcaddr,dstmatch,dstaddr,pronum,starttime,stoptime,concat('advpolicy_',iface) as iface FROM sysrouteadv WHERE id=%s """
    result2 = readDb(sql2,(id,))
    return template('addadvroute',session=s,info=result2[0],iflist=infos,setlist=result)

@route('/editadvroute/<id>',method="POST")
@checkAccess
def do_editadvroute(id):
    s = request.environ.get('beaker.session')
    rulename = request.forms.get("rulename")
    pronum = request.forms.get("pronum")
    starttime = request.forms.get("starttime")
    stoptime = request.forms.get("stoptime")
    outdev = request.forms.get("ifacename").replace('advpolicy_','')
    srcmatch = request.forms.get("srcmatch")
    if srcmatch == "2":
       srcaddr="all"
    else:
       srcaddr = (',').join(request.forms.getlist("srcaddr"))
    dstmatch = request.forms.get("dstmatch")
    if dstmatch == "2":
       dstaddr="all"
    else:
       dstaddr = (',').join(request.forms.getlist("dstaddr"))
    #提交判断
    if outdev == '' or rulename == '':
        msg = {'color':'red','message':u'描述或出口未填写，添加失败'}
        return(template('advroute',msg=msg,session=s))
    if int(pronum) <0 or int(pronum) >32765 :
        msg = {'color':'red','message':u'优先级值填写错误，添加失败'}
        return(template('advroute',msg=msg,session=s))
    cmdDict=cmds.getdictrst('ip rule add prio %s fwmark 1000%s dev %s' % (pronum,id,outdev))
    if cmdDict.get('status') == 0:
       sql = """ UPDATE sysrouteadv SET rulename=%s,srcmatch=%s,srcaddr=%s,dstmatch=%s,dstaddr=%s,pronum=%s,starttime=%s,stoptime=%s,iface=%s WHERE id=%s """
       data = (rulename,srcmatch,srcaddr,dstmatch,dstaddr,int(pronum),starttime,stoptime,outdev,id)
       result = writeDb(sql,data)
       if result :
          writeROUTEconf(action='uptconf')
          writeUTMconf(action='uptconf')
          msg = {'color':'green','message':u'更新成功'}
       else :
          msg = {'color':'red','message':u'更新失败'}
    else:
       msg = {'color':'red','message':u'系统规则生成异常，添加失败'}
    return(template('advroute',msg=msg,session=s))

@route('/advroutepolicy')
@checkAccess
def advroutepolicy():
    s = request.environ.get('beaker.session')
    return template('advroutepolicy',session=s,msg={})

@route('/addadvroutepolicy')
@checkAccess
def do_addadvroutepolicy():
    s = request.environ.get('beaker.session')
    netmod.InitNIinfo()
    sql = " SELECT ifacename FROM netiface UNION select concat('tun',tunid) as ifacename FROM vnodemgr where status='1' "
    ifacelist_result = readDb(sql,)
    return template('addadvroutepolicy',session=s,msg={},info={},ifacelist_result=ifacelist_result)

@route('/addadvroutepolicy',method="POST")
@checkAccess
def addadvroutepolicy():
    s = request.environ.get('beaker.session')
    rid = 'advpolicy_%d' % time.time()
    rtname = request.forms.get("rtname")
    rttype = request.forms.get("rttype")
    if rttype == 'A' :
       iflist = request.forms.getlist("ifname")
       if 'tun10' in iflist[0] :
          rid = 'advpolicy_%d' % int(iflist[0].replace('tun',''))
    elif rttype == 'B' :
       iflist = request.forms.getlist("ifnames")
       for ifname in iflist:
         if 'tun10' in ifname :
            msg = {'color':'red','message':u'添加失败,TUN接口仅适用于单线路由模式'}
            return(template('advroutepolicy',msg=msg,session=s))
       if len(iflist) < 2 :
          msg = {'color':'red','message':u'添加失败,权重模式至少2个接口'}
          return(template('advroutepolicy',msg=msg,session=s))
    vdict = {'rtname': rtname, 'rttype': rttype, 'iflist': iflist}
    sql = " INSERT INTO sysattr (attr,value,status,servattr) value (%s,%s,1,'advroutepolicy')"
    ndata = (rid,json.dumps(vdict))
    result = writeDb(sql,ndata)
    #提交判断
    if result == True:
       msg = {'color':'green','message':u'添加成功'}
       writeROUTEconf(action='uptconf')
       return(template('advroutepolicy',msg=msg,session=s))
    else:
       msg = {'color':'red','message':u'添加失败'}
       return(template('advroutepolicy',msg=msg,session=s))

@route('/editadvroutepolicy/<id>')
@checkAccess
def do_addadvroutepolicy(id):
    s = request.environ.get('beaker.session')
    netmod.InitNIinfo()
    sql = " select attr,value from sysattr where attr=%s "
    result = readDb(sql,(id,))
    for info in result :
        info['rtname']=json.loads(info.get('value')).get('rtname')
        info['rttype']=json.loads(info.get('value')).get('rttype')
        info['iflist']=','.join(json.loads(info.get('value')).get('iflist'))
    sql2 = " SELECT ifacename FROM netiface UNION select concat('tun',tunid) as ifacename FROM vnodemgr where status='1' "
    ifacelist_result = readDb(sql2,)
    return template('addadvroutepolicy',session=s,msg={},info=info,ifacelist_result=ifacelist_result)

@route('/editadvroutepolicy/<id>',method="POST")
@checkAccess
def do_editadvroutepolicy(id):
    s = request.environ.get('beaker.session')
    rtname = request.forms.get("rtname")
    rttype = request.forms.get("rttype")
    if rttype == 'A' :
       iflist = request.forms.getlist("ifname")
    elif rttype == 'B' :
       iflist = request.forms.getlist("ifnames")
       for ifname in iflist:
         if 'tun10' in ifname :
           msg = {'color':'red','message':u'添加失败,TUN接口仅适用于单线路由模式'}
           return(template('advroutepolicy',msg=msg,session=s))
       if len(iflist) < 2 :
          msg = {'color':'red','message':u'添加失败,权重模式至少2个接口'}
          return(template('advroutepolicy',msg=msg,session=s))
    vdict = {'rtname': rtname, 'rttype': rttype, 'iflist': iflist}
    sql = " update sysattr set value=%s where attr=%s"
    ndata = (json.dumps(vdict),id)
    result = writeDb(sql,ndata)
    #提交判断
    if result == True:
       msg = {'color':'green','message':u'更新成功'}
       writeROUTEconf(action='uptconf')
       return(template('advroutepolicy',msg=msg,session=s))
    else:
       msg = {'color':'red','message':u'更新失败'}
       return(template('advroutepolicy',msg=msg,session=s))


@route('/delroute/<stype>/<id>')
@checkAccess
def deliface(stype,id):
    s = request.environ.get('beaker.session')
    if stype == 'sys' or stype == 'static' :
       sqlquery = " select dest,netmask,gateway FROM sysroute WHERE id=%s "
       sql = " DELETE FROM sysroute WHERE id=%s "
    elif stype == 'advpolicy': 
       sql = " DELETE FROM sysattr WHERE attr=%s "
       sqlquery = " select count(*) as num from sysrouteadv WHERE position( iface in %s) "
    else:
       sqlquery = " select id,pronum,srcmatch,dstmatch,iface FROM sysrouteadv WHERE id=%s "
       sql = " DELETE FROM sysrouteadv WHERE id=%s "
    resultA = readDb(sqlquery,(id,))
    # 判断删除入口并返回到指定界面
    if stype == 'sys':
       tpl = 'routeconf'
    elif stype == 'static':
       tpl = 'staticroute'
    elif stype == 'adv':
       tpl = 'advroute'
    elif stype == 'advpolicy':
       tpl = 'advroutepolicy'
       # 判断当删除高级策略时，该策略是否被关联
       if resultA[0].get('num') > 0:
          msg = {'color':'red','message':u'策略已被关联,无法删除'}
          return template(tpl,session=s,msg=msg) 
    # 判断提交的指令
    result = writeDb(sql,(id,))
    if result == True:
       if stype == 'adv':
          try:
             if resultA[0].get('srcmatch') == 2 and resultA[0].get('dstmatch') == 2 :
                cmds.getdictrst('ip rule del prio %s table %s' % (resultA[0].get('pronum'),resultA[0].get('iface')))
             else :
                cmds.getdictrst('ip rule del prio %s fwmark 1000%s table %s' % (resultA[0].get('pronum'),resultA[0].get('id'),resultA[0].get('iface')))
             msg = {'color':'green','message':u'删除成功'}
             return template(tpl,session=s,msg=msg)
          except:
                msg = {'color':'red','message':u'删除失败'}
                return template(tpl,session=s,msg=msg)
       elif stype == 'advpolicy':
          writeROUTEconf(action='uptconf')
          msg = {'color':'green','message':u'删除成功'}
          return template(tpl,session=s,msg=msg)
       else:
          cmds.getdictrst('route del -net %s netmask %s gw %s' % (resultA[0].get('dest'),resultA[0].get('netmask'),resultA[0].get('gateway')))
          writeROUTEconf(action='uptconf')
          writeUTMconf(action='uptconf')
          msg = {'color':'green','message':u'删除成功'}
          return template(tpl,session=s,msg=msg)
    else:
       msg = {'color':'red','message':u'删除失败'}
       return template(tpl,session=s,msg=msg)

@route('/servtools')
@checkAccess
def servtools():
    """服务工具"""
    s = request.environ.get('beaker.session')
    return template('servtools',session=s,info={})

@route('/servtools',method="POST")
@checkAccess
def do_servtools():
    s = request.environ.get('beaker.session')
    toolsname = request.forms.get("toolsname")
    if toolsname == 'DEVACT':
       servname = request.forms.get("servname2")
    else:
       servname = request.forms.get("servname")
    result = cmds.syscmds(toolsname,servname)
    info = {}
    info['toolsname'] = toolsname
    info['servname'] = servname
    info['result'] = result
    if result :
       msg = {'color':'green','message':u'查询完成'}
    return(template('servtools',msg=msg,session=s,info=info))

@route('/resconfig')
@checkAccess
def servtools():
    """资源配置"""
    s = request.environ.get('beaker.session')
    sql = " select value from sysattr where attr='resData' and servattr='sys' "
    result = readDb(sql,)
    try:
        info = json.loads(result[0].get('value'))
    except:
        return(template('resconfig',session=s,msg={},info={}))
    return template('resconfig',session=s,msg={},info=info)

@route('/resconfig',method="POST")
@checkAccess
def do_servtools():
    s = request.environ.get('beaker.session')
    ResState = request.forms.get("ResState")
    ResSaveDay = request.forms.get("ResSaveDay")
    ResInv = request.forms.get("ResInv")
    visitDay = request.forms.get("visitDay")
    try:
       int(ResSaveDay)
       int(visitDay)
       int(ResInv)
    except:
       msg = {'color':'red','message':'配置保存失败,参数不符合要求'}
       return redirect('/resconfig')
    if int(ResSaveDay) < 1 or int(visitDay) < 1 or int(ResInv) < 60 :
       msg = {'color':'red','message':'配置保存失败,参数不符合要求'}
       return redirect('/resconfig')
    idata = dict()
    idata['ResState'] = ResState
    idata['ResSaveDay'] = ResSaveDay
    idata['ResInv'] = ResInv
    idata['visitDay'] = visitDay
    sql = " update sysattr set value=%s where attr='resData' "
    iidata=json.dumps(idata)
    result = writeDb(sql,(iidata,))
    if result == True :
       msg = {'color':'green','message':'配置保存成功'}
    else:
       msg = {'color':'red','message':'配置保存失败'}
    return(template('resconfig',msg=msg,session=s,info=idata))

@route('/systeminfo')
@route('/')
@checkAccess
def systeminfo():
    """系统信息项"""
    s = request.environ.get('beaker.session')
    info=dict()
    info['hostname'] = platform.node()
    info['kernel'] = platform.platform()
    info['systime'] = cmds.getdictrst('date +"%Y%m%d %H:%M:%S"').get('result')
    cmdRun='cat /proc/uptime|awk -F. \'{run_days=$1/86400;run_hour=($1%86400)/3600;run_minute=($1%3600)/60;run_second=$1%60;printf("%d天%d时%d分%d秒",run_days,run_hour,run_minute,run_second)}\''
    info['runtime'] = cmds.getdictrst(cmdRun).get('result')
    info['pyversion'] = platform.python_version()
    info['memsize'] = cmds.getdictrst('cat /proc/meminfo |grep \'MemTotal\' |awk -F: \'{printf ("%.0fM",$2/1024)}\'|sed \'s/^[ \t]*//g\'').get('result')
    info['cpumode'] = cmds.getdictrst('grep \'model name\' /proc/cpuinfo |uniq |awk -F : \'{print $2}\' |sed \'s/^[ \t]*//g\' |sed \'s/ \+/ /g\'').get('result')
    info['v4addr'] = 'Wan: '+netmod.NetIP()
    info['appversion'] = AppServer().getVersion()
    """管理日志"""
    sql = " SELECT id,objtext,objact,objhost,objtime FROM logrecord order by id DESC limit 7 "
    logdict = readDb(sql,)
    return template('systeminfo',session=s,info=info,logdict=logdict)

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
           return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
           return obj.strftime("%Y-%m-%d")
        else:
           return json.JSONEncoder.default(self, obj)

@route('/systeminfo',method="POST")
@checkAccess
def do_systeminfo():
    s = request.environ.get('beaker.session')
    sql = " select value from sysattr where attr='resData' "
    info = readDb(sql,)
    try:
       ninfo=json.loads(info[0].get('value'))
    except:
       return False
    visitDay = ninfo.get('visitDay')
    try:
        date = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()-(int(visitDay) * 86400)))
        sql = " select info,tim from sysinfo where tim > (%s) order by id"
        resultData = readDb2(sql,(date,))
        result = [True,resultData]
    except Exception as e:
        result = [False,str(e)]
    return json.dumps({'resultCode':0,'result':result},cls=DateEncoder)

@route('/applog')
@checkAccess
def applog():
    """服务工具"""
    s = request.environ.get('beaker.session')
    return template('applog',session=s,msg={},info={})

@route('/api/getapplog',method=['GET', 'POST'])
@checkAccess
def getapplog():
    sql = """ SELECT id,objtime,objname,objtext,objact,objhost FROM logrecord order by id desc """
    item_list = readDb(sql,)
    return json.dumps(item_list, cls=DateEncoder)

# 网络对象
@route('/netobjconf')
@checkAccess
def netobjconf():
    """UTM配置页"""
    s = request.environ.get('beaker.session')
    return template('netobjconf',session=s,msg={})

@route('/addnetobj')
@checkAccess
def addnetobj():
    """网络对象配置 添加页"""
    s = request.environ.get('beaker.session')
    return template('addnetobj',session=s,msg={},info={})

@route('/addnetobj',method='POST')
@checkAccess
def do_addnetobj():
    """网络对象配置 添加页"""
    s = request.environ.get('beaker.session')
    objname = request.forms.get("objname")
    objtype = request.forms.get("objtype")
    if objname == "":
       msg = {'color':'red','message':u'添加失败，对象名称不能为空'}
       return template('netobjconf',session=s,msg=msg,info={})
    if objtype == "ipset" :
       objtext = request.forms.get("objtextA").replace('\r\n','\n').strip()
       objtext = '\n'.join(sorted(set(objtext.split('\n'))))
       for ipaddr in objtext.split('\n'):
           if netmod.checkips(ipaddr) == False :
              msg = {'color':'red','message':u'添加失败，地址不合法'}
              return template('netobjconf',session=s,msg=msg,info={})
    elif objtype == "domainset" :
       objtext = request.forms.get("objtextB").replace('\r\n','\n').strip()
       for domain in objtext.split('\n'):
           if netmod.is_domain(domain) == False :
              msg = {'color':'red','message':u'添加失败，域名不合法'}
              return template('netobjconf',session=s,msg=msg,info={})
    sql = "insert into netobjgroup(objname,objtype,objtext,status,objattr) VALUES(%s,%s,%s,%s,%s)"
    data = (objname,objtype,objtext,"1","1")
    result = writeDb(sql,data)
    if result == True:
       writeUTMconf(action='uptconf')
       msg = {'color':'green','message':u'添加成功'}
       return template('netobjconf',session=s,msg=msg,info={})
    else:
       msg = {'color':'red','message':u'添加失败'}
       return template('netobjconf',session=s,msg=msg,info={})

@route('/editnetobj/<id>')
@checkAccess
def editnetobj(id):
    s = request.environ.get('beaker.session')
    sql = " SELECT objname,objtype,objtext FROM netobjgroup where status='1' and id=%s"
    result = readDb(sql,(id,))
    return template('addnetobj',session=s,msg={},info=result[0])

@route('/editnetobj/<id>',method="POST")
@checkAccess
def do_editnetobj(id):
    s = request.environ.get('beaker.session')
    objname = request.forms.get("objname")
    objtype = request.forms.get("objtype")
    if objname == "":
       msg = {'color':'red','message':u'添加失败，对象名称不能为空'}
       return template('netobjconf',session=s,msg=msg,info={})
    if objtype == "ipset" :
       objtext = request.forms.get("objtextA").replace('\r\n','\n').strip()
       objtext = '\n'.join(sorted(set(objtext.split('\n'))))
       for ipaddr in objtext.split('\n'):
           if netmod.checkips(ipaddr) == False :
              msg = {'color':'red','message':u'添加失败，地址不合法'}
              return template('netobjconf',session=s,msg=msg,info={})
    elif objtype == "domainset" :
       objtext = request.forms.get("objtextB").replace('\r\n','\n').strip()
       for domain in objtext.split('\n'):
           if netmod.is_domain(domain) == False :
              msg = {'color':'red','message':u'添加失败，域名不合法'}
              return template('netobjconf',session=s,msg=msg,info={})
    sql = "update netobjgroup set objname=%s,objtype=%s,objtext=%s where id=%s"
    data = (objname,objtype,objtext,id)
    result = writeDb(sql,data)
    if result == True:
       writeUTMconf(action='uptconf')
       msg = {'color':'green','message':u'添加成功'}
       return template('netobjconf',session=s,msg=msg,info={})
    else:
       msg = {'color':'red','message':u'添加失败'}
       return template('netobjconf',session=s,msg=msg,info={})

@route('/delnetobj/<id>')
@checkAccess
def delutmrule(id):
    s = request.environ.get('beaker.session')
    sql = """ select count(*) as count from (select srcaddr,dstaddr FROM ruleconfnat union select srcaddr,dstaddr FROM ruleconfutm union select srcaddr,dstaddr FROM sysrouteadv ) as U 
              where srcaddr=%s or dstaddr=%s
          """
    result = readDb(sql,(id,id))
    if result[0].get('count') == 0:
       sql2 = "delete from netobjgroup where id=%s"
       result2 = writeDb(sql2,(id,))
       if result2 == True:
          writeUTMconf(action='uptconf')
          msg = {'color':'green','message':u'删除成功'}
          return template('netobjconf',session=s,msg=msg)
       else:
          msg = {'color':'red','message':u'删除失败'}
          return template('netobjconf',session=s,msg=msg)
    else:
       msg = {'color':'red','message':u'删除失败,对象已被关联使用'}
       return template('netobjconf',session=s,msg=msg)

# UTM配置
@route('/utmruleconf')
@checkAccess
def utmruleconf():
    """UTM配置页"""
    s = request.environ.get('beaker.session')
    return template('utmruleconf',session=s,msg={})

@route('/natruleconf')
@checkAccess
def utmruleconf():
    """NAT配置页"""
    s = request.environ.get('beaker.session')
    return template('natruleconf',session=s,msg={})

@route('/mapruleconf')
@checkAccess
def utmruleconf():
    """MAP配置页"""
    s = request.environ.get('beaker.session')
    return template('mapruleconf',session=s,msg={})

@route('/addmaprule')
@checkAccess
def addmaprule():
    """MAP配置 添加页"""
    s = request.environ.get('beaker.session')
    netmod.InitNIinfo()
    sql = " SELECT ifacename FROM netiface "
    ifacelist_result = readDb(sql,)
    return template('addmaprule',session=s,msg={},info={},ifacelist_result=ifacelist_result)

@route('/addmaprule',method='POST')
@checkAccess
def do_addmaprule():
    """MAP配置 添加页"""
    s = request.environ.get('beaker.session')
    rulename = request.forms.get("rulename")
    pronum = request.forms.get("pronum")
    wantype = request.forms.get("wantype")
    if int(wantype) == 0 :
       wanaddr = request.forms.get("wanaddr")
    elif int(wantype) == 1 :
       wanaddr = request.forms.get("waniface")
    wanport = request.forms.get("wanport")
    intaddr = request.forms.get("intaddr")
    intport = request.forms.get("intport")
    proto = ','.join(request.forms.getlist("prototype"))
    sql = "insert into ruleconfmap(rulename,pronum,wantype,wanaddr,wanport,intaddr,intport,proto) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
    data = (rulename,pronum,wantype,wanaddr,wanport,intaddr,intport,proto)
    if not (rulename and pronum):
          msg = {'color':'red','message':u'规则名称或优先级未填写,添加失败'}
          return template('mapruleconf',session=s,msg=msg,info={})
    if int(wantype) == 0 :
       alladdr=wanaddr.split('\n')+intaddr.split('\n')
    elif int(wantype) == 1 :
       alladdr=intaddr.split('\n')
    for ip in alladdr :
        if netmod.checkip(ip) == False and ip != '':
           msg = {'color':'red','message':u'地址格式错误，添加失败'}
           return(template('mapruleconf',msg=msg,session=s))
    if len(wanport.split(',')) > 10 or len(intport.split(',')) > 10 :
       msg = {'color':'red','message':u'端口组总数量超过最大值10，添加失败'}
       return(template('mapruleconf',msg=msg,session=s))
    allport = wanport.split(',')+intport.split(',')
    for port in allport :
        if ':' in port:
           if len(port.split(':')) != 2 or port.split(':')[0] >= port.split(':')[1]:
              msg = {'color':'red','message':u'连续端口格式错误，添加失败'}
              return(template('mapruleconf',msg=msg,session=s))
        else :
           if netmod.is_port(port) == False and port != '' :
              msg = {'color':'red','message':u'外部端口或内部端口格式错误，添加失败'}
              return(template('mapruleconf',msg=msg,session=s))
    result = writeDb(sql,data)
    if result == True:
       msg = {'color':'green','message':u'添加成功'}
       writeUTMconf(action='addconf')
       return template('mapruleconf',session=s,msg=msg,info={})

# UTM添加规则
@route('/addutmrule')
@checkAccess
def addutmrule():
    """UTM配置 添加页"""
    s = request.environ.get('beaker.session')
    sql = """ select id,objname from netobjgroup where status='1' order by id"""
    result = readDb(sql,)
    return template('addutmrule',session=s,msg={},info={},setlist=result)

@route('/addutmrule',method='POST')
@checkAccess
def do_addutmrule():
    """UTM配置 添加页"""
    s = request.environ.get('beaker.session')
    rulename = request.forms.get("rulename")
    pronum = request.forms.get("pronum")
    actzone = request.forms.get("actzone")
    srcmatch = request.forms.get("srcmatch")
    if srcmatch == "2":
       srcaddr="all"
    else:
       srcaddr = (',').join(request.forms.getlist("srcaddr"))
    dstmatch = request.forms.get("dstmatch")
    if dstmatch == "2":
       dstaddr="all"
    else:
       dstaddr = (',').join(request.forms.getlist("dstaddr"))
    netproto = request.forms.get("netproto")
    sport = request.forms.get("sport")
    dport = request.forms.get("dport")
    runaction = request.forms.get("runaction")
    sql = """ insert into ruleconfutm(rulename,pronum,actzone,srcmatch,srcaddr,dstmatch,dstaddr,netproto,sport,dport,runaction) 
              VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    data = (rulename,pronum,actzone,srcmatch,srcaddr,dstmatch,dstaddr,netproto,sport,dport,runaction)
    if not (srcaddr and dstaddr and rulename and pronum):
          msg = {'color':'red','message':u'规则名称或优先级未填写,添加失败'}
          return template('utmruleconf',session=s,msg=msg,info={})
    if ( netproto == "TCP" or netproto == "UDP" ) and ( sport == "" and dport == ""):
       msg = {'color':'red','message':u'TCP/UDP协议端口不能全部为空'}
       return(template('utmruleconf',msg=msg,session=s))
    if len(sport.split(',')) > 10 or len(dport.split(',')) > 10 :
       msg = {'color':'red','message':u'端口组总数量超过最大值10，添加失败'}
       return(template('utmruleconf',msg=msg,session=s))
    allport = sport.split(',')+dport.split(',')
    for port in allport :
        if ':' in port:
           if len(port.split(':')) != 2 or port.split(':')[0] >= port.split(':')[1]:
              msg = {'color':'red','message':u'连续端口格式错误，添加失败'}
              return(template('utmruleconf',msg=msg,session=s))
        else :
           if netmod.is_port(port) == False and port != '' :
              msg = {'color':'red','message':u'源端口或目标端口格式错误，添加失败'}
              return(template('utmruleconf',msg=msg,session=s))
    result = writeDb(sql,data)
    if result == True:
       msg = {'color':'green','message':u'添加成功'}
       writeUTMconf(action='addconf')
       return template('utmruleconf',session=s,msg=msg,info={})

@route('/editutmrule/<id>')
@checkAccess
def editutmrule(id):
    """UTM配置 添加页"""
    s = request.environ.get('beaker.session')
    sql = """ select id,objname from netobjgroup where status='1' order by id"""
    result = readDb(sql,)
    sql2 = """ SELECT rulename,actzone,srcmatch,srcaddr,netproto,sport,dstmatch,dstaddr,dport,runaction,pronum 
               from ruleconfutm where status='1' and id=%s """
    result2 = readDb(sql2,(id,))
    return template('addutmrule',session=s,msg={},info=result2[0],setlist=result)

@route('/editutmrule/<id>',method='POST')
@checkAccess
def do_editutmrule(id):
    """UTM配置 更新页"""
    s = request.environ.get('beaker.session')
    rulename = request.forms.get("rulename")
    pronum = request.forms.get("pronum")
    actzone = request.forms.get("actzone")
    srcmatch = request.forms.get("srcmatch")
    if srcmatch == "2":
       srcaddr="all"
    else:
       srcaddr = (',').join(request.forms.getlist("srcaddr"))
    dstmatch = request.forms.get("dstmatch")
    if dstmatch == "2":
       dstaddr="all"
    else:
       dstaddr = (',').join(request.forms.getlist("dstaddr"))
    netproto = request.forms.get("netproto")
    sport = request.forms.get("sport")
    dport = request.forms.get("dport")
    runaction = request.forms.get("runaction")
    sql = """ update ruleconfutm set rulename=%s,pronum=%s,actzone=%s,srcmatch=%s,srcaddr=%s,dstmatch=%s,dstaddr=%s,netproto=%s,sport=%s,dport=%s,runaction=%s where id=%s """
    data = (rulename,pronum,actzone,srcmatch,srcaddr,dstmatch,dstaddr,netproto,sport,dport,runaction,id)
    if not (srcaddr and dstaddr and rulename and pronum):
          msg = {'color':'red','message':u'规则名称或优先级、地址类型未填写,添加失败'}
          return template('utmruleconf',session=s,msg=msg,info={})
    if ( netproto == "TCP" or netproto == "UDP" ) and (sport == "" and dport == ""):
       msg = {'color':'red','message':u'TCP/UDP协议端口不能全部为空'}
       return(template('utmruleconf',msg=msg,session=s))
    if len(sport.split(',')) > 10 or len(dport.split(',')) > 10 :
       msg = {'color':'red','message':u'端口组总数量超过最大值10，添加失败'}
       return(template('utmruleconf',msg=msg,session=s))
    allport = sport.split(',')+dport.split(',')
    for port in allport :
        if ':' in port:
           if len(port.split(':')) != 2 or port.split(':')[0] >= port.split(':')[1]:
              msg = {'color':'red','message':u'连续端口格式错误，添加失败'}
              return(template('utmruleconf',msg=msg,session=s))
        else :
           if netmod.is_port(port) == False and port != '' :
              msg = {'color':'red','message':u'源端口或目标端口格式错误，添加失败'}
              return(template('utmruleconf',msg=msg,session=s))
    result = writeDb(sql,data)
    if result == True:
       msg = {'color':'green','message':u'更新成功'}
       writeUTMconf(action='addconf')
       return template('utmruleconf',session=s,msg=msg,info={})

@route('/addnatrule')
@checkAccess
def addutmrule():
    """NAT配置 添加页"""
    s = request.environ.get('beaker.session')
    sql = """ select id,objname from netobjgroup where status='1' order by id"""
    result = readDb(sql,)
    netmod.InitNIinfo()
    sql = """ SELECT ifacename FROM netiface UNION select concat('tun',tunid) as ifacename FROM vnodemgr where status='1' """
    ifacelist_result = readDb(sql,)
    return template('addnatrule',session=s,msg={},info={},ifacelist_result=ifacelist_result,setlist=result)

@route('/addnatrule',method='POST')
@checkAccess
def do_addnatrule():
    """UTM配置 添加页"""
    s = request.environ.get('beaker.session')
    rulename = request.forms.get("rulename")
    runaction = request.forms.get("runaction")
    runobject = request.forms.get("runobject")
    pronum = request.forms.get("pronum")

    srcmatch = request.forms.get("srcmatch")
    if srcmatch == "2":
       srcaddr="all"
    else:
       srcaddr = (',').join(request.forms.getlist("srcaddr"))
    dstmatch = request.forms.get("dstmatch")
    if dstmatch == "2":
       dstaddr="all"
    else:
       dstaddr = (',').join(request.forms.getlist("dstaddr"))

    if runaction == 'SNAT':
       runobject = request.forms.get("runobject")
       if netmod.checkip(runobject) == False:
          msg = {'color':'red','message':u'源地址转换不能填写非IP类型,添加失败'}
          return template('natruleconf',session=s,msg=msg,info={})
    else :
       runobject = request.forms.get("runobject2")

    sql = "insert into ruleconfnat(rulename,srcmatch,srcaddr,dstmatch,dstaddr,runaction,runobject,pronum) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
    data = (rulename,srcmatch,srcaddr,dstmatch,dstaddr,runaction,runobject,pronum)
    result = writeDb(sql,data)
    if result == True:
       msg = {'color':'green','message':u'添加成功'}
       writeUTMconf(action='addconf')
       return template('natruleconf',session=s,msg=msg,info={})
    else:
       msg = {'color':'green','message':u'添加失败'}
       return template('natruleconf',session=s,msg=msg,info={})

@route('/editnatrule/<id>')
@checkAccess
def editnatrule(id):
    """UTM配置 添加页"""
    s = request.environ.get('beaker.session')
    netmod.InitNIinfo()
    sql = """ select id,objname from netobjgroup where status='1' order by id"""
    result = readDb(sql,)
    sql2 = """ SELECT ifacename FROM netiface UNION select concat('tun',tunid) as ifacename FROM vnodemgr where status='1' """
    ifacelist_result = readDb(sql2,)
    sql3 = " SELECT rulename,srcmatch,srcaddr,dstmatch,dstaddr,runaction,runobject,runobject as runobject2,pronum from ruleconfnat where status='1' and id=%s"
    result3 = readDb(sql3,(id,))
    return template('addnatrule',session=s,msg={},info=result3[0],ifacelist_result=ifacelist_result,setlist=result)

@route('/editnatrule/<id>',method='POST')
@checkAccess
def do_editnatrule(id):
    """UTM配置 更新页"""
    s = request.environ.get('beaker.session')
    rulename = request.forms.get("rulename")
    runaction = request.forms.get("runaction")
    runobject = request.forms.get("runobject")
    pronum = request.forms.get("pronum")

    srcmatch = request.forms.get("srcmatch")
    if srcmatch == "2":
       srcaddr="all"
    else:
       srcaddr = (',').join(request.forms.getlist("srcaddr"))
    dstmatch = request.forms.get("dstmatch")
    if dstmatch == "2":
       dstaddr="all"
    else:
       dstaddr = (',').join(request.forms.getlist("dstaddr"))
    if runaction == 'SNAT':
       runobject = request.forms.get("runobject")
       if netmod.checkip(runobject) == False:
          msg = {'color':'red','message':u'源地址转换不能填写非IP类型,添加失败'}
          return template('natruleconf',session=s,msg=msg,info={})
    else :
       runobject = request.forms.get("runobject2")
    sql = "update ruleconfnat set rulename=%s,srcmatch=%s,srcaddr=%s,dstmatch=%s,dstaddr=%s,runaction=%s,runobject=%s,pronum=%s where id=%s"
    data = (rulename,srcmatch,srcaddr,dstmatch,dstaddr,runaction,runobject,pronum,id)
    result = writeDb(sql,data)
    if result == True:
       writeUTMconf(action='uptconf')
       msg = {'color':'green','message':u'更新成功'}
       return template('natruleconf',session=s,msg=msg,info={})

@route('/editmaprule/<id>')
@checkAccess
def editutmrule(id):
    """UTM配置 添加页"""
    s = request.environ.get('beaker.session')
    netmod.InitNIinfo()
    sql = " SELECT ifacename FROM netiface UNION select concat('tun',tunid) as ifacename FROM vnodemgr where status='1' "
    ifacelist_result = readDb(sql,)
    sql2 = " SELECT rulename,wantype,wanaddr,wanport,intaddr,intport,proto,pronum from ruleconfmap where status='1' and id=%s"
    result = readDb(sql2,(id,))
    return template('addmaprule',session=s,msg={},info=result[0],ifacelist_result=ifacelist_result)

@route('/editmaprule/<id>',method='POST')
@checkAccess
def do_editutmrule(id):
    """MAP配置 添加页"""
    s = request.environ.get('beaker.session')
    rulename = request.forms.get("rulename")
    pronum = request.forms.get("pronum")
    wantype = request.forms.get("wantype")
    if int(wantype) == 0 :
       wanaddr = request.forms.get("wanaddr")
    elif int(wantype) == 1 :
       wanaddr = request.forms.get("waniface")
    wanport = request.forms.get("wanport")
    intaddr = request.forms.get("intaddr")
    intport = request.forms.get("intport")
    proto = ','.join(request.forms.getlist("prototype"))
    sql = "update ruleconfmap set rulename=%s,pronum=%s,wantype=%s,wanaddr=%s,wanport=%s,intaddr=%s,intport=%s,proto=%s where id=%s"
    data = (rulename,pronum,wantype,wanaddr,wanport,intaddr,intport,proto,id)
    if not (rulename and pronum):
          msg = {'color':'red','message':u'规则名称或优先级未填写,添加失败'}
          return template('mapruleconf',session=s,msg=msg,info={})
    if int(wantype) == 0 :
       alladdr=wanaddr.split('\n')+intaddr.split('\n')
    elif int(wantype) == 1 :
       alladdr=intaddr.split('\n')
    for ip in alladdr :
        if netmod.checkip(ip) == False and ip != '':
           msg = {'color':'red','message':u'地址格式错误，添加失败'}
           return(template('mapruleconf',msg=msg,session=s))
    if len(wanport.split(',')) > 10 or len(intport.split(',')) > 10 :
       msg = {'color':'red','message':u'端口组总数量超过最大值10，添加失败'}
       return(template('mapruleconf',msg=msg,session=s))
    allport = wanport.split(',')+intport.split(',')
    for port in allport :
        if ':' in port:
           if len(port.split(':')) != 2 or port.split(':')[0] >= port.split(':')[1]:
              msg = {'color':'red','message':u'连续端口格式错误，添加失败'}
              return(template('mapruleconf',msg=msg,session=s))
        else :
           if netmod.is_port(port) == False and port != '' :
              msg = {'color':'red','message':u'外部端口或内部端口格式错误，添加失败'}
              return(template('mapruleconf',msg=msg,session=s))
    result = writeDb(sql,data)
    if result == True:
       msg = {'color':'green','message':u'添加成功'}
       writeUTMconf(action='addconf')
       return template('mapruleconf',session=s,msg=msg,info={})

@route('/delutmrule/<id>')
@checkAccess
def delutmrule(id):
    s = request.environ.get('beaker.session')
    sql = " DELETE FROM ruleconfutm WHERE id=%s "
    result = writeDb(sql,(id,))
    if result == True :
       writeUTMconf(action='uptconf')
       msg = {'color':'green','message':u'删除成功'}
       return template('utmruleconf',session=s,msg=msg)
    else:
       msg = {'color':'red','message':u'删除失败'}
       return template('utmruleconf',session=s,msg=msg)

@route('/delnatrule/<id>')
@checkAccess
def delnatrule(id):
    s = request.environ.get('beaker.session')
    sql = " DELETE FROM ruleconfnat WHERE id=%s "
    result = writeDb(sql,(id,))
    if result == True :
       writeUTMconf(action='uptconf')
       msg = {'color':'green','message':u'删除成功'}
       return template('natruleconf',session=s,msg=msg)
    else:
       msg = {'color':'red','message':u'删除失败'}
       return template('natruleconf',session=s,msg=msg)

@route('/delmaprule/<id>')
@checkAccess
def delmaprule(id):
    s = request.environ.get('beaker.session')
    sql = " DELETE FROM ruleconfmap WHERE id=%s "
    result = writeDb(sql,(id,))
    if result == True :
       writeUTMconf(action='uptconf')
       msg = {'color':'green','message':u'删除成功'}
       return template('mapruleconf',session=s,msg=msg)
    else:
       msg = {'color':'red','message':u'删除失败'}
       return template('mapruleconf',session=s,msg=msg)

@route('/api/getutmruleinfo',method=['GET', 'POST'])
@checkAccess
def getifaceinfo():
    sql = """ SELECT U.id,U.rulename,U.actzone,U.runaction,U.pronum,
              if(U.srcaddr="all","全部网络",concat(if(U.srcmatch=0,"! ",""),D.objname)) as srcaddr,
              if(U.dstaddr="all","全部网络",concat(if(U.dstmatch=0,"! ",""),E.objname)) as dstaddr,
              if(U.netproto="ALL","不限",concat(U.netproto,':',U.sport)) as sport,
              if(U.netproto="ALL","不限",concat(U.netproto,':',U.dport)) as dport
              FROM ruleconfutm as U LEFT OUTER JOIN netobjgroup as D on D.id=U.srcaddr LEFT OUTER JOIN netobjgroup as E on E.id=U.dstaddr order by pronum """
    result = readDb(sql,)
    return json.dumps(result)

@route('/api/getnetobjinfo',method=['GET', 'POST'])
@checkAccess
def getnetobjinfo():
    sql = """ SELECT id,objname,objtype,left(objtext,100) as objtext,objattr,status
              FROM  netobjgroup where objattr='1' order by id """
    result = readDb(sql,)
    return json.dumps(result)

@route('/api/getnatruleinfo',method=['GET', 'POST'])
@checkAccess
def getifaceinfo():
    sql = """ SELECT U.id,U.rulename,U.runaction,U.runobject,U.pronum,
              if(U.srcaddr="all","全部网络",concat(if(U.srcmatch=0,"! ",""),D.objname)) as srcaddr,
              if(U.dstaddr="all","全部网络",concat(if(U.dstmatch=0,"! ",""),E.objname)) as dstaddr
              FROM ruleconfnat as U LEFT OUTER JOIN netobjgroup as D on D.id=U.srcaddr LEFT OUTER JOIN netobjgroup as E on E.id=U.dstaddr order by pronum """
    iface_list = readDb(sql,)
    return json.dumps(iface_list)

@route('/api/getmapruleinfo',method=['GET', 'POST'])
@checkAccess
def getifaceinfo():
    sql = """ SELECT id,rulename,wanaddr,wanport,intaddr,intport,proto,pronum 
            FROM ruleconfmap order by pronum """
    iface_list = readDb(sql,)
    return json.dumps(iface_list)

# 策略配置
@route('/api/getpolicylist',method=['GET', 'POST'])
@checkAccess
def getifaceinfo():
    sql = " SELECT id,name,pushaddr,txlimit,rxlimit,pushdns,left(pushroute,100) as pushroute,left(pushnoroute,100) as pushnoroute FROM vpnpolicy "
    iface_list = readDb(sql,)
    return json.dumps(iface_list)

@route('/policyconf')
@checkAccess
def policyconf():
    """策略列表页"""
    s = request.environ.get('beaker.session')
    return template('policyconf',session=s,msg={})

@route('/addpolicy')
@checkAccess
def policyconf():
    """添加策略页"""
    s = request.environ.get('beaker.session')
    return template('addpolicyconf',session=s,info={'pushaddr':'DynamicIP'})


@route('/addpolicy',method="POST")
@checkAccess
def do_addpolicy():
    """POST"""
    s = request.environ.get('beaker.session')
    name = request.forms.get("name")
    pushaddr = request.forms.get("pushaddr")
    txlimit = request.forms.get("txlimit")
    rxlimit = request.forms.get("rxlimit")
    pushdns = request.forms.get("pushdns").replace('\r\n','\n').strip()
    pushroute = request.forms.get("pushroute").replace('\r\n','\n').strip()
    pushnoroute = request.forms.get("pushnoroute").replace('\r\n','\n').strip()
    allipmask = pushroute.split('\n')+pushnoroute.split('\n')
    if netmod.checkip(pushaddr) == False and pushaddr != 'DynamicIP':
           msg = {'color':'red','message':u'分配地址内容检测错误,添加失败'}
           return(template('policyconf',session=s,msg=msg,info={}))
    for ip in pushdns.split('\n') :
        if netmod.checkip(ip) == False and ip != '':
           msg = {'color':'red','message':u'DNS内容检测错误,更新失败'}
           return(template('policyconf',session=s,msg=msg,info={}))
    for ips in allipmask :
        if netmod.checkips(ips) == False and ips != '':
           msg = {'color':'red','message':u'路由内容检测错误,更新失败'}
           return(template('policyconf',session=s,msg=msg,info={}))
    try:
       int(txlimit)
    except:
       txlimit = 100
    try:
       int(rxlimit)
    except:
       rxlimit = 100
    sql = "INSERT INTO vpnpolicy(name,pushaddr,txlimit,rxlimit,pushdns,pushroute,pushnoroute) VALUES(%s,%s,%s,%s,%s,%s,%s)"
    data=(name,pushaddr,txlimit,rxlimit,pushdns,pushroute,pushnoroute)
    result = writeDb(sql,data)
    if result == True:
       writeVPNconf(action='uptgroup')
       writeUTMconf(action='addconf')    
       msg = {'color':'green','message':u'添加成功'}
       return(template('policyconf',session=s,msg=msg,info={}))
    else:
       msg = {'color':'red','message':u'添加失败'}
       return(template('policyconf',session=s,msg=msg,info={}))

@route('/editpolicy/<id>')
@checkAccess
def editpolicy(id):
    """修改策略"""
    s = request.environ.get('beaker.session')
    sql = "select name,pushaddr,txlimit,rxlimit,pushdns,pushroute,pushnoroute from vpnpolicy WHERE id=%s"
    result = readDb(sql,(id,))
    if result :
       return(template('addpolicyconf',session=s,info=result[0]))

@route('/editpolicy/<id>',method="POST")
@checkAccess
def editpolicy(id):
    """修改策略"""
    s = request.environ.get('beaker.session')
    name = request.forms.get("name")
    pushaddr = request.forms.get("pushaddr")
    txlimit = request.forms.get("txlimit")
    rxlimit = request.forms.get("rxlimit")
    pushdns = request.forms.get("pushdns").replace('\r\n','\n').strip()
    pushroute = request.forms.get("pushroute").replace('\r\n','\n').strip()
    pushnoroute = request.forms.get("pushnoroute").replace('\r\n','\n').strip()
    allipmask = pushroute.split('\n')+pushnoroute.split('\n')
    # 内容检测
    if netmod.checkip(pushaddr) == False and pushaddr != 'DynamicIP':
           msg = {'color':'red','message':u'分配地址内容检测错误,添加失败'}
           return(template('policyconf',session=s,msg=msg,info={}))
    for ip in pushdns.split('\n') :
        if netmod.checkip(ip) == False and ip != '':
           msg = {'color':'red','message':u'DNS内容检测错误,更新失败'}
           return(template('policyconf',session=s,msg=msg,info={}))
    for ips in allipmask :
        if netmod.checkips(ips) == False and ips != '' :
           msg = {'color':'red','message':u'路由内容检测错误,更新失败'}
           return(template('policyconf',session=s,msg=msg,info={}))
    try:
       int(txlimit)
    except:
       txlimit = 100
    try: 
       int(rxlimit)
    except:
       rxlimit = 100
    sql = "UPDATE vpnpolicy set name=%s,pushaddr=%s,txlimit=%s,rxlimit=%s,pushdns=%s,pushroute=%s,pushnoroute=%s where id=%s"
    data=(name,pushaddr,txlimit,rxlimit,pushdns,pushroute,pushnoroute,id)
    result = writeDb(sql,data)
    if result == True:
       writeVPNconf(action='uptgroup')
       writeUTMconf(action='addconf')    
       msg = {'color':'green','message':u'更新成功'}
       return(template('policyconf',session=s,msg=msg,info={}))
    else:
       msg = {'color':'red','message':u'更新失败'}
       return(template('policyconf',session=s,msg=msg,info={}))

@route('/delpolicy/<id>')
@checkAccess
def delpolicy(id):
    """删除策略"""
    s = request.environ.get('beaker.session')
    sql = "select username from user where policy=%s "
    chkdata = readDb(sql,(id,))
    if len(chkdata) > 0 :
       msg = {'color':'red','message':u'删除失败,该策略已被关联无法删除'}
       return(template('policyconf',session=s,msg=msg,info={}))
    sql = "delete from vpnpolicy where id in (%s) "
    result = writeDb(sql,(id,))
    if result:
       writeVPNconf(action='uptgroup')
       writeUTMconf(action='uptconf')
       msg = {'color':'green','message':u'删除成功'}
       return(template('policyconf',session=s,msg=msg,info={}))
    else:
       msg = {'color':'red','message':u'删除失败'}
       return(template('policyconf',session=s,msg=msg,info={}))

@route('/addprofile')
@checkAccess
def addprofile():
    s = request.environ.get('beaker.session')
    sql = " select value from sysattr where attr='vpnprofile' "
    result = readDb(sql,)
    return(template('addprofile',session=s,msg={},info=result[0]))

@route('/addprofile', method="POST")
@checkAccess
def addprofile():
    s = request.environ.get('beaker.session')
    xmltext = request.forms.get("xmltext")
    if xmltext == '' :
       msg = {'color':'red','message':u'信息为空，保存失败'}
       return(template('addprofile',session=s,msg=msg,info={}))
    sql = " update sysattr set value=%s where attr='vpnprofile' "
    result = writeDb(sql,(xmltext,))
    if result == True:
       writeVPNconf(action='uptprofile')
       msg = {'color':'green','message':u'Profile.xml保存成功'}
       sql = " select value from sysattr where attr='vpnprofile' "
       result = readDb(sql,)
       return(template('addprofile',session=s,msg=msg,info=result[0]))

@route('/vpnservconf')
@checkAccess
def servconf():
    """VPN服务配置项"""
    s = request.environ.get('beaker.session')
    return template('vpnservconf',session=s,msg={})

@route('/addservconf')
@checkAccess
def addservconf():
    """新增服务配置项"""
    s = request.environ.get('beaker.session')
    sql = " select value from sysattr where attr='vpnserver' "
    idata = readDb(sql,)
    try:
       info = json.loads(idata[0].get('value'))
       if cmds.servchk(info.get('servport')) == 0:
          info['servstatus'] = '0'
       else :
          info['servstatus'] = '1'
    except:
       return template('addvpnconfig',session=s,msg={},info={})
    return template('addvpnconfig',session=s,info=info)

@route('/disconnect/<id>')
@checkAccess
def do_disconnect(id):
    """强制断开用户"""
    s = request.environ.get('beaker.session')
    xstatus,result=cmds.gettuplerst('occtl disconnect user %s' % id)
    if xstatus == 0 :
       msg = {'color':'green','message':u'断开成功'}
       return template('vpnservconf',session=s,msg=msg)
    else:
       msg = {'color':'red','message':u'断开失败'}
       return template('vpnservconf',session=s,msg=msg)

@route('/addservconf',method="POST")
@checkAccess
def do_addservconf():
    """新增服务配置项"""
    s = request.environ.get('beaker.session')
    idata = dict()
    idata['authtype'] = request.forms.get("authtype")
    idata['ipaddr'] = request.forms.get("ipaddr")
    idata['servport'] = request.forms.get("servport")
    idata['virip'] = request.forms.get("virip")
    idata['virmask'] = request.forms.get("virmask")
    idata['maxclient'] = request.forms.get("maxclient")
    idata['maxuser'] = request.forms.get("maxuser")
    idata['authtimeout'] = request.forms.get("authtimeout")
    idata['authnum'] = request.forms.get("authnum")
    idata['locktime'] = request.forms.get("locktime")
    idata['comp'] = request.forms.get("comp")
    idata['cisco'] = request.forms.get("cisco")
    if netmod.checkip(idata['virip']) == False or netmod.checkmask(idata['virmask']) == False :  
       msg = {'color':'red','message':u'虚拟地址填写不合法，保存失败'}
       return template('vpnservconf',session=s,msg=msg,info={})
    if idata['authtype'] == '3':
       idata = {"authtype": "3", "service": "off"}
    sql = " update sysattr set value=%s where attr='vpnserver' "
    iidata = json.dumps(idata)
    result = writeDb(sql,(iidata,))
    if result == True :
       writeVPNconf(action='addconf')
       if idata['authtype'] != '3':
          cmds.servboot('ocserv')
       writeUTMconf(action='uptconf')
       msg = {'color':'green','message':u'配置保存成功'}
       return template('vpnservconf',session=s,msg=msg,info={})

@route('/addclientconf')
@checkAccess
def addclientconf():
    """新增服务配置项"""
    s = request.environ.get('beaker.session')
    info={}
    #获取证书选择列表
    conncerts_list=[]
    status,result=cmds.gettuplerst('find %s/conncerts -name \'*.p12\' -exec basename {} \;|sort' % gl.get_value('certdir'))
    for i in result.split('\n'):
        if str(i) != "":
           infos = {}
           infos['filename']=str(i)
           conncerts_list.append(infos)
    #加载现有配置
    sql = " select tunid from vnodemgr where status=1 "
    data = readDb(sql,)
    max_item=1000
    try:
       for x in data:
           if x.get('tunid') > max_item:
              max_item = x.get('tunid')
       info['tunid'] = int(max_item)+1
    except:
       info['tunid'] = 1000
    return template('addvpncltconfig',session=s,msg={},info=info,conncerts_list=conncerts_list)

@route('/addclientconf',method="POST")
@checkAccess
def addclientconf():
    """新增服务配置项"""
    s = request.environ.get('beaker.session')
    authtype = request.forms.get("authtype")
    if authtype == '0' :
       vconninfo = '%s::%s ' % (request.forms.get("certinfo"),request.forms.get("certpass"))
    elif authtype == '1' :
       vconninfo = '%s::%s ' % (request.forms.get("vpnuser"),request.forms.get("vpnpass"))
    else :
       msg = {'color':'green','message':u'验证类型错误，保存失败'}    
       return template('addvpncltconfig',session=s,msg=msg,info={})
    vnodename = request.forms.get("vnodename")
    authtype = request.forms.get("authtype")
    ipaddr = request.forms.get("ipaddr")
    servport = request.forms.get("servport")
    tunid = request.forms.get("tunid")
    vmtu = request.forms.get("vmtu")
    chkconn = request.forms.get("chkconn")
    chkdtls = request.forms.get("chkdtls")
    #获取证书选择列表
    conncerts_list=[]
    status,result=cmds.gettuplerst('find %s/conncerts -name \'*.p12\' -exec basename {} \;|sort' % gl.get_value('certdir'))
    for i in result.split('\n'):
        if str(i) != "":
           infos = {}
           infos['filename']=str(i)
           conncerts_list.append(infos)
    #加载正常配置判断
    if not (ipaddr and servport and tunid and vmtu) :
       #处理特殊情况，关闭服务时
       msg = {'color':'red','message':u'配置保存失败，关键参数未设置'}
       return template('addvpncltconfig',session=s,msg=msg,info={},conncerts_list=conncerts_list)
    #服务器地址相同的情况下，只允许保存一次
    sqlx = " select ipaddr from vnodemgr where status=1"
    Xresult = readDb(sqlx,) 
    for i in Xresult:
          if ipaddr in i.get('ipaddr'):
             msg = {'color':'red','message':u'配置保存失败，服务器地址重复'}
             return template('addvpncltconfig',session=s,msg=msg,info={},conncerts_list=conncerts_list)
    #写入数据库
    sql = " insert into vnodemgr(vnodename,authtype,ipaddr,servport,tunid,vmtu,chkdtls,vconninfo,chkconn) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s) "
    idata=(vnodename,authtype,ipaddr,servport,tunid,vmtu,chkdtls,vconninfo,chkconn)
    result = writeDb(sql,idata)
    if result == True :
       msg = {'color':'green','message':u'配置保存成功'}
       writeVPNconf(action='uptcltconf')
       cmds.servboot('vpnconn')
       writeUTMconf(action='uptconf')
       return template('vnodemgr',session=s,msg=msg)

@route('/editcltconf/<id>')
@checkAccess
def editcltconf(id):
    """编辑客户端配置项"""
    s = request.environ.get('beaker.session')
    info={}
    #获取证书选择列表
    conncerts_list=[]
    status,result=cmds.gettuplerst('find %s/conncerts -name \'*.p12\' -exec basename {} \;|sort' % gl.get_value('certdir'))
    for i in result.split('\n'):
        if str(i) != "":
           infos = {}
           infos['filename']=str(i)
           conncerts_list.append(infos)
    #加载现有配置
    sql = " select vnodename,authtype,ipaddr,servport,tunid,vmtu,chkdtls,vconninfo,chkconn from vnodemgr where tunid=%s "
    xdata = readDb(sql,(id,))
    info['vnodename']=xdata[0].get('vnodename')
    info['authtype']=xdata[0].get('authtype')
    if xdata[0].get('authtype') == 0 :
       info['certinfo'] = xdata[0].get('vconninfo').split('::')[0]
       info['certpass'] = xdata[0].get('vconninfo').split('::')[1]
    elif xdata[0].get('authtype') == 1 :
       info['vpnuser'] = xdata[0].get('vconninfo').split('::')[0]
       info['vpnpass'] = xdata[0].get('vconninfo').split('::')[1]
    info['ipaddr']=xdata[0].get('ipaddr')
    info['servport']=xdata[0].get('servport')
    info['tunid']=xdata[0].get('tunid')
    info['vmtu']=xdata[0].get('vmtu')
    info['chkdtls']=xdata[0].get('chkdtls')
    info['chkconn']=xdata[0].get('chkconn')
    return template('addvpncltconfig',session=s,msg={},info=info,conncerts_list=conncerts_list)

@route('/editcltconf/<id>',method="POST")
@checkAccess
def post_editcltconf(id):
    """编辑VPN客户端配置项"""
    s = request.environ.get('beaker.session')
    authtype = request.forms.get("authtype")
    if authtype == '0' :
       vconninfo = '%s::%s ' % (request.forms.get("certinfo"),request.forms.get("certpass"))
    elif authtype == '1' :
       vconninfo = '%s::%s ' % (request.forms.get("vpnuser"),request.forms.get("vpnpass"))
    vnodename = request.forms.get("vnodename")
    authtype = request.forms.get("authtype")
    ipaddr = request.forms.get("ipaddr")
    servport = request.forms.get("servport")
    vmtu = request.forms.get("vmtu")
    chkconn = request.forms.get("chkconn")
    chkdtls = request.forms.get("chkdtls")
    #获取证书选择列表
    conncerts_list=[]
    status,result=cmds.gettuplerst('find %s/conncerts -name \'*.p12\' -exec basename {} \;|sort' % gl.get_value('certdir'))
    for i in result.split('\n'):
        if str(i) != "":
           infos = {}
           infos['filename']=str(i)
           conncerts_list.append(infos)
    #加载正常配置判断
    if not (ipaddr and servport and vmtu) :
       #处理特殊情况，关闭服务时
       msg = {'color':'red','message':u'配置保存失败，关键参数未设置'}
       return template('addvpncltconfig',session=s,msg=msg,info={},conncerts_list=conncerts_list)
    #服务器地址相同的情况下，只允许保存一次
    sqlx = " select ipaddr from vnodemgr where status=1 and tunid != %s"
    Xresult = readDb(sqlx,(id,))
    for i in Xresult:
          if ipaddr in i.get('ipaddr'):
             msg = {'color':'red','message':u'配置保存失败，服务器地址重复'}
             return template('addvpncltconfig',session=s,msg=msg,info={},conncerts_list=conncerts_list)
    #更新数据库
    sql = " UPDATE vnodemgr set vnodename=%s,authtype=%s,ipaddr=%s,servport=%s,vmtu=%s,chkdtls=%s,vconninfo=%s,chkconn=%s where tunid=%s "
    idata=(vnodename,authtype,ipaddr,servport,vmtu,chkdtls,vconninfo,chkconn,id)
    result = writeDb(sql,idata)
    if result == True :
       msg = {'color':'green','message':u'配置保存成功'}
       writeVPNconf(action='uptcltconf')
       cmds.servboot('vpnconn')
       writeUTMconf(action='uptconf')
       return template('vnodemgr',session=s,msg=msg)

@route('/delcltconf/<id>')
@checkAccess
def delcltconf(id):
    s = request.environ.get('beaker.session')
    sql1 = """ SELECT count(*) as num FROM ruleconfnat where runobject="tun%s" """ % id
    result1 = readDb(sql1,)
    args = '%%'+'iflist'+'%%'+'tun'+id+'%%'
    sql2 = """ SELECT count(*) as num FROM sysattr where servattr="advroutepolicy" and value like "%s" """ % args
    result2 = readDb(sql2,)
    if result1[0].get('num') > 0 or result2[0].get('num') > 0 :
       msg = {'color':'red','message':u'接口被绑定NAT或高级路由，无法关联删除'}
       return template('vnodemgr',session=s,msg=msg)
    sql = " DELETE FROM vnodemgr WHERE tunid=%s "
    result = writeDb(sql,(id,))
    if result == True :
       msg = {'color':'green','message':u'删除成功'}
       cmds.gettuplerst('%s/sbin/startvpnconn.sh stop %s' % (gl.get_value('wkdir'),id))
       cmds.servboot('ocserv')
       writeVPNconf(action='uptcltconf')
       cmds.servboot('vpnconn')
       writeUTMconf(action='uptconf')
       return template('vnodemgr',session=s,msg=msg)
    else:
       msg = {'color':'red','message':u'删除失败'}
       return template('vnodemgr',session=s,msg=msg)

# 策略配置
@route('/api/getvpnservinfo',method=['GET', 'POST'])
@checkAccess
def getvpnservinfo():
    sql = " SELECT id,servmode,authtype,concat(ipaddr,':',servport) as servinfo,concat(virip,'/',virmask)as virinfo,maxclient,maxuser,authtimeout,authnum,locktime,comp,cisco,workstatus FROM vpnservconf "
    certinfo_list = readDb(sql,)
    return json.dumps(certinfo_list)

@route('/api/getonlineinfo',method=['GET', 'POST'])
@checkAccess
def getonlineinfo():
    info=[]
    astatus,aresult=cmds.gettuplerst('occtl show users')
    bstatus,bresult=cmds.gettuplerst('occtl show users | awk \'/vpns/{print $2,$4,$5,$6,$7,$8,$9}\'')
    if astatus == 0:
       for i in bresult.split('\n'):
        if str(i) != "":
           infos={}
           infos['user']=str(i).split()[0]
           infos['ip']=str(i).split()[1]
           infos['vpn-ip']=str(i).split()[2]
           infos['device']=str(i).split()[3]
           infos['since']=str(i).split()[4]
           infos['dtls-cipher']=str(i).split()[5]
           infos['status']=str(i).split()[6]
           info.append(infos)
    return json.dumps(info)

@route('/delvpnservconf/<id>')
@checkAccess
def delvpnservconf(id):
    s = request.environ.get('beaker.session')
    sql = " DELETE FROM vpnservconf WHERE id=%s "
    result = writeDb(sql,(id,))
    if result == True :
       msg = {'color':'green','message':u'删除成功'}
       cmds.gettuplerst('/bin/rm -rf %s/ocserv/ocserv_*_%s.conf' % (gl.get_value('plgdir'),id))
       cmds.servboot('ocserv')
       writeUTMconf(action='uptconf')
       return template('vpnservconf',session=s,msg=msg)
    else:
       msg = {'color':'red','message':u'删除失败'}
       return template('vpnservconf',session=s,msg=msg)

@route('/editvpnservconf/<id>')
@checkAccess
def editvpnservconf(id):
    s = request.environ.get('beaker.session')
    sql = " SELECT authtype,ipaddr,servport,virip,virmask,maxclient,maxuser,authtimeout,authnum,locktime,comp,cisco,workstatus FROM vpnservconf WHERE id = %s "
    result = readDb(sql,(id,))
    return template('addvpnconfig',session=s,info=result[0])

@route('/editvpnservconf/<id>',method="POST")
@checkAccess
def do_editvpnservconf(id):
    """修改提交服务配置项"""
    s = request.environ.get('beaker.session')
    authtype = request.forms.get("authtype")
    ipaddr = request.forms.get("ipaddr")
    servport = request.forms.get("servport")
    virip = request.forms.get("virip")
    virmask = request.forms.get("virmask")
    maxclient = request.forms.get("maxclient")
    maxuser = request.forms.get("maxuser")
    authtimeout = request.forms.get("authtimeout")
    authnum = request.forms.get("authnum")
    locktime = request.forms.get("locktime")
    comp = request.forms.get("comp")
    cisco = request.forms.get("cisco")

    if netmod.checkip(virip) == False or netmod.checkmask(virmask) == False :
       msg = {'color':'red','message':u'虚拟地址填写不合法，保存失败'}
       return template('vpnservconf',session=s,msg=msg,info={})
    if servport.isdigit() == False or maxclient.isdigit() == False or maxuser.isdigit() == False or authtimeout.isdigit() == False or authnum.isdigit() == False or locktime.isdigit() == False:
       msg = {'color':'red','message':u'填写不合法，保存失败'}
       return template('vpnservconf',session=s,msg=msg,info={})
    if int(servport) < 0 or int(servport) > 65535 :
       msg = {'color':'red','message':u'端口配置错误，保存失败'}
       return template('vpnservconf',session=s,msg=msg,info={})

    if netmod.checkip(ipaddr) == True or ipaddr == '*' :
       True
    else:
       msg = {'color':'red','message':u'监听信息填写错误，保存失败'}
       return template('vpnservconf',session=s,msg=msg,info={})

    sql = " UPDATE vpnservconf set authtype=%s,ipaddr=%s,servport=%s,virip=%s,virmask=%s,maxclient=%s,maxuser=%s,authtimeout=%s,authnum=%s,locktime=%s,comp=%s,cisco=%s WHERE id=%s"
    data = (authtype,ipaddr,servport,virip,virmask,maxclient,maxuser,authtimeout,authnum,locktime,comp,cisco,id)
    result = writeDb(sql,data)
    if result == True :
       writeVPNconf(action='uptconf')
       cmds.servboot('ocserv')
       writeUTMconf(action='uptconf')
       return template('vpnservconf',session=s,info={},msg={})

@route('/showservlog')
@checkAccess
def showservlog():
    """显示日志项"""
    s = request.environ.get('beaker.session')
    result = cmds.getdictrst('grep "ocserv" /var/log/messages|tail -300|awk \'{$4="";print $0}\'')
    return template('showlog',session=s,msg={},info=result)

# 节点管理
@route('/vnodemgr')
@checkAccess
def servconf():
    """节点管理项"""
    s = request.environ.get('beaker.session')
    return template('vnodemgr',session=s,msg={})


# 证书配置
@route('/certmgr')
@checkAccess
def servconf():
    """证书管理项"""
    s = request.environ.get('beaker.session')
    return template('certmgr',session=s,msg={})

@route('/initca',method="POST")
@checkAccess
def initca():
    from Functions import mkcert
    s = request.environ.get('beaker.session')
    certtype = request.forms.get("certtype")
    servname = request.forms.get("servname")
    organization = request.forms.get("organization")
    expiration = request.forms.get("expiration")
    createdate = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    comment = request.forms.get("servname")
    #检测表单各项值，如果出现为空的表单，则返回提示
    if not (servname and organization and expiration):
        message = "表单不允许为空！"
        return '-2'

    if expiration.isdigit() == False :
       message = "有效期不是一个整数"
       return '-2'

    if netmod.is_domain(servname) == False :
       message = "服务名称不合法,格式: www.xxx.com"
       return '-2'

    result = mkcert(ct=certtype,cn=servname,ou=organization,ex=expiration,comment=comment)
    if result == 0:
       cmds.servboot('ocserv')
       return 0
    else:
       return '-1'

@route('/addusercerts')
@checkAccess
def addusercerts():
    s = request.environ.get('beaker.session')
    policylist_sql = "select id,name from vpnpolicy "
    plylist_result = readDb(policylist_sql,)
    return template('addusercerts',message='',info={},session=s,plylist_result=plylist_result)

@route('/addusercerts',method="POST")
@checkAccess
def addusercerts():
    from Functions import mkcert
    s = request.environ.get('beaker.session')
    certtype = request.forms.get("certtype")
    commonname = request.forms.get("commonname")
    expiration = request.forms.get("expiration")
    createdate = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    organization = request.forms.get("organization")
    safekey = request.forms.get("safekey")
    comment = request.forms.get("comment")
    #检测表单各项值，如果出现为空的表单，则返回提示
    if not (commonname and expiration and organization and safekey):
       msg = {'color':'red','message':u'表单不允许为空！'}
       return(template('certmgr',session=s,msg=msg))

    result = mkcert(ct=certtype,cn=commonname,ou=organization,ex=expiration,safekey=safekey,comment=comment)
    if result == 0:
       writeVPNconf(action='uptuser')
       msg = {'color':'green','message':u'添加成功'}
       return(template('certmgr',session=s,msg=msg))
    else:
       return '-1'

@route('/delcert',method="POST")
@checkAccess
def delcert():
    id = request.forms.get('str').rstrip(',')
    if not id:
        return '-1'
    for xid in id.split(',') :
        sql2 = " select commonname from certmgr where id=%s "
        result = readDb(sql2,(xid,))
        if result[0].get('commonname') == 'CA' or result[0].get('commonname') == 'Server':
           cmds.gettuplerst('rm -rf %s/*.crt %s/*.pem %s/*.txt %s/*.p12' % (gl.get_value('certdir'),gl.get_value('certdir'),gl.get_value('certdir'),gl.get_value('certdir')))
           writeDb('TRUNCATE TABLE certmgr')
           writeVPNconf(action='uptuser')
           return '0'
        else:
           commonname = result[0].get('commonname')
           # 吊销证书
           cmds.gettuplerst('cat %s/%s.crt >> %s/revoke.pem' % (gl.get_value('certdir'),commonname,gl.get_value('certdir')))
           cmds.gettuplerst('certtool --generate-crl --load-ca-privkey %s/ca-key.pem --load-ca-certificate %s/ca.crt --load-certificate %s/revoke.pem --template %s/crl.txt --outfile %s/crl.pem' % (gl.get_value('certdir'),gl.get_value('certdir'),gl.get_value('certdir'),gl.get_value('certdir'),gl.get_value('certdir')))
           # 删除用户证书文件
           cmds.gettuplerst('/bin/rm -rf %s/%s.crt %s/%s.pem %s/%s.p12' % (gl.get_value('certdir'),commonname,gl.get_value('certdir'),commonname,gl.get_value('certdir'),commonname))
           # 删除数据库条目
           sql = "delete from certmgr where id in (%s)"
           result = writeDb(sql % xid)
    if result:
        writeVPNconf(action='uptuser')
        cmds.servboot('ocserv')
        return '0'
    else:
        return '-1'


@route('/conncerts')
@checkAccess
def conncerts():
    s = request.environ.get('beaker.session')
    return template('conncerts',session=s,msg={})

@route('/uplconncerts')
@checkAccess
def conncerts():
    s = request.environ.get('beaker.session')
    return template('uplconncerts',session=s,msg={})

@route('/uplconncerts', method='POST')
def do_upload():
    s = request.environ.get('beaker.session')
    category = request.forms.get('category')
    upload = request.files.get('upload')
    try:
        name, ext = os.path.splitext(upload.filename)
    except:
        msg = {'color':'red','message':u'文件未检测到.上传失败'}
        return template('backupset',session=s,msg=msg)
    if ext not in ('.p12','.jpgsss'):
       msg = {'color':'red','message':u'文件格式不被允许.请重新上传'}
       return template('conncerts',session=s,msg=msg)
    try:
       upload.save('%s/conncerts' % gl.get_value('certdir'))
       msg = {'color':'green','message':u'文件上传成功'}
       return template('conncerts',session=s,msg=msg)
    except:
       msg = {'color':'red','message':u'文件上传失败'}
       return template('conncerts',session=s,msg=msg) 

@route('/download/<vdir>/<filename:re:.*\.zip|.*\.bkt|.*\.p12>')
def download(vdir,filename):
    if vdir == 'certs' :
       #定义download路径
       download_path = '/tmp'
       filenames = filename.split('.')[0]
       cmds.gettuplerst('/bin/rm -rf %s/%s' % (download_path,filename))
       zp = zipfile.ZipFile('%s/%s' % (download_path,filename),'w')
       if filenames == 'CA' or filenames == 'Server' :
          zp.write('%s/ca.crt' % gl.get_value('certdir'),'ca.crt')
          zp.write('%s/server.crt' % gl.get_value('certdir'),'server.crt')
       else : 
          sql = 'select safekey from certmgr where commonname=%s'
          result = readDb(sql,(filenames,))
          safekey = result[0].get('safekey')
          #20190104禁止下载CA、PEM 
          #zp.write('%s/ca.crt' % gl.get_value('certdir'),'ca.crt')
          #zp.write('%s/%s.crt' %  (gl.get_value('certdir'),filenames),'%s.crt' % filenames)
          #zp.write('%s/%s.pem' %  (gl.get_value('certdir'),filenames),'%s.pem' % filenames)
          status,result = cmds.gettuplerst('openssl pkcs12 -export -passout pass:%s -inkey %s/%s.pem -in %s/%s.crt -name "%s VPN Client Cert" -certfile %s/ca.crt -out %s/%s.p12' % (safekey,gl.get_value('certdir'),filenames,gl.get_value('certdir'),filenames,filenames,gl.get_value('certdir'),gl.get_value('certdir'),filenames))
          if status == 0 :
             zp.write('%s/%s.p12' %  (gl.get_value('certdir'),filenames),'%s.p12' % filenames)
       zp.close()
    elif vdir == 'backupset':
       download_path = '%s/backupset' % gl.get_value('plgdir')
    elif vdir == 'conncerts':
       download_path = '%s/conncerts' % gl.get_value('certdir')
    return static_file(filename, root=download_path, download=filename)

# LnmVPN系统对接
@route('/wsapi')
def wsapi():
    import urlparse,urllib
    s = request.environ.get('beaker.session')
    odict = urlparse.parse_qs(urlparse.urlparse('wsapi?%s' % request.environ.get('QUERY_STRING')).query)
    PassKey = AppServer().getConfValue('wsapi','token')

    try:
       if odict['token'][0] != PassKey :
          msg = {'return':255,'message':'token id error...'}
          return(template('wsapp.html',msg=msg,session=s))
    except:
       msg = {'return':256,'message':'token id error...'}
       return(template('wsapp.html',msg=msg,session=s))

    try:
       if odict['otype'][0] == '1':
          sql = """ select username as username,passwd as password,concat('Policy_',policy) as area from user where access=0 and stopdate >= %s """
          curdate = datetime.datetime.now().strftime('%Y%m%d')
          result = readDb(sql,(curdate,))
          if result is False or len(result) == 0:
             msg = {'return':255,'message':'wsapi get error...'}
          else:
             msg = {'return':0,'message':result}
       else:
          msg = {'return':255,'message':'system not found otype .'}
    except:
       msg = {'return':0,'message':'system not found otype .'}
    return(template('wsapp.html',msg=msg,session=s))

# 获取节点列表
@route('/api/getvnodelist',method=['GET', 'POST'])
@checkAccess
def getcertinfo():
    sql = """ select vnodename,authtype,concat(ipaddr,':',servport) as vconn,chkdtls,vconninfo,vmtu,chkconn,tunid from vnodemgr where status=1 """
    Xresult = readDb(sql,)
    return json.dumps(Xresult)

# 获取证书列表
@route('/api/getcertinfo',method=['GET', 'POST'])
@checkAccess
def getcertinfo():
    sql = """ SELECT U.id,U.commonname,U.certtype,U.expiration,D.name as organization,U.createdate,U.safekey,U.comment 
    FROM certmgr as U
    LEFT OUTER JOIN vpnpolicy as D on U.organization=D.id WHERE certtype = 'Client' UNION 
    SELECT id,commonname,certtype,expiration,organization,createdate,safekey,comment FROM certmgr WHERE certtype='caserver'
    order by id
    """
    certinfo_list = readDb(sql,)
    return json.dumps(certinfo_list)

@route('/syscheck')
@checkAccess
def syscheck():
    s = request.environ.get('beaker.session')
    return template('systemcheck',session=s)

@route('/api/getsyschkinfo',method=['GET', 'POST'])
@checkAccess
def getcertinfo():
    result = cmds.envCheck('result')
    return json.dumps(result)

# 备份集管理
@route('/backupset')
@checkAccess
def syscheck():
    s = request.environ.get('beaker.session')
    return template('backupset',session=s,msg={})

@route('/uploadfile')
@checkAccess
def syscheck():
    s = request.environ.get('beaker.session')
    return template('uploadfile',session=s,msg={})

@route('/uploadfile', method='POST')
def do_upload():
    s = request.environ.get('beaker.session')
    category = request.forms.get('category')
    upload = request.files.get('upload')
    try:
        name, ext = os.path.splitext(upload.filename)
    except:
        msg = {'color':'red','message':u'文件未检测到.上传失败'}
        return template('backupset',session=s,msg=msg)
    if ext not in ('.bkt','.jpgsss'):
       msg = {'color':'red','message':u'文件格式不被允许.请重新上传'}
       return template('backupset',session=s,msg=msg)
    try:
       upload.save('%s/backupset' % gl.get_value('plgdir'))
       msg = {'color':'green','message':u'文件上传成功'}
       return template('backupset',session=s,msg=msg)
    except:
       msg = {'color':'red','message':u'文件上传失败'}
       return template('backupset',session=s,msg=msg)

@route('/startbackupset')
@checkAccess
def delbackupset():
    s = request.environ.get('beaker.session')
    createtm = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
    from MySQL import db_name,db_user,db_pass,db_ip,db_port
    backupsetname='backupset_%s.bkt' % createtm
    cmd='mysqldump -u%s -p%s -h%s -P%s %s > %s/backupset/%s ' % (db_user,db_pass,db_ip,db_port,db_name,gl.get_value('plgdir'),backupsetname)
    x,y = cmds.gettuplerst(cmd)
    if x == 0:
       msg = {'color':'green','message':u'备份完成'}
    else :
       msg = {'color':'red','message':u'备份失败'}
    return template('backupset',session=s,msg=msg)

@route('/restore/<filename>')
@checkAccess
def restore(filename):
    s = request.environ.get('beaker.session')
    if filename != "":
       from MySQL import db_name,db_user,db_pass,db_ip,db_port
       x,y=cmds.gettuplerst('mysql -h%s -P%s -u%s -p%s %s < %s/backupset/%s' % (db_ip,db_port,db_user,db_pass,db_name,gl.get_value('plgdir'),filename))
       if x == 0:
          msg = {'color':'green','message':u'备份集恢复成功,请重启服务以重新加载数据.'}
       else:
          msg = {'color':'red','message':u'备份集恢复失败'}
    else:
       msg = {'color':'red','message':u'备份集恢复失败'}
    return template('backupset',session=s,msg=msg)

@route('/delbackupset/<filename>')
@checkAccess
def delbackupset(filename):
    s = request.environ.get('beaker.session')
    if filename != "":
       x,y=cmds.gettuplerst('rm -rf %s/backupset/%s' % (gl.get_value('plgdir'),filename))
       if x == 0:
          msg = {'color':'green','message':u'备份集删除成功'}
       else:
          msg = {'color':'red','message':u'备份集删除失败'}
    return template('backupset',session=s,msg=msg)

@route('/delconncerts/<filename>')
@checkAccess
def delbackupset(filename):
    s = request.environ.get('beaker.session')
    if filename != "":
       x,y=cmds.gettuplerst('rm -rf %s/conncerts/%s' % (gl.get_value('certdir'),filename))
       if x == 0:
          msg = {'color':'green','message':u'指定验证证书删除成功'}
       else:
          msg = {'color':'red','message':u'指定验证证书删除失败'}
    return template('conncerts',session=s,msg=msg)

@route('/api/getbackupsetinfo',method=['GET', 'POST'])
@checkAccess
def getbackupsetinfo():
    info=[]
    status,result=cmds.gettuplerst('find %s/backupset -name \'*.bkt\' -exec basename {} \;|sort' % gl.get_value('plgdir'))
    for i in result.split('\n'):
        if str(i) != "":
           infos={}
           infos['filename']=str(i)
           infos['filesize']=os.path.getsize('%s/backupset/%s' % (gl.get_value('plgdir'),i))
           cctime=os.path.getctime('%s/backupset/%s' % (gl.get_value('plgdir'),i))
           infos['filetime']=time.strftime('%Y%m%d%H%M%S',time.localtime(cctime))
           info.append(infos)
    return json.dumps(info)

@route('/api/getconncertsinfo',method=['GET', 'POST'])
@checkAccess
def getconncertsinfo():
    info=[]
    status,result=cmds.gettuplerst('find %s/conncerts -name \'*.p12\' -exec basename {} \;|sort' % gl.get_value('certdir'))
    for i in result.split('\n'):
        if str(i) != "":
           infos={}
           infos['filename']=str(i)
           infos['filesize']=os.path.getsize('%s/conncerts/%s' % (gl.get_value('certdir'),i))
           cctime=os.path.getctime('%s/conncerts/%s' % (gl.get_value('certdir'),i))
           infos['filetime']=time.strftime('%Y%m%d%H%M%S',time.localtime(cctime))
           info.append(infos)
    return json.dumps(info)

@route('/api/getadvroutepolicyinfo',method=['GET', 'POST'])
@checkAccess
def getadvroutepolicyinfo():
    info=[]
    sql = " SELECT attr,value FROM sysattr where servattr='advroutepolicy' order by attr "
    result = readDb(sql,)
    for sdict in result:
        sdict['attr']=sdict.get('attr')
        sdict['rtname']=json.loads(sdict.get('value')).get('rtname')
        sdict['rttype']=json.loads(sdict.get('value')).get('rttype')
        sdict['iflist']=json.loads(sdict.get('value')).get('iflist')
        info.append(sdict)
    return json.dumps(info)

if __name__ == '__main__' :
   sys.exit()
