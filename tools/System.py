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
    sql = """ SELECT id, rulename, left(srcaddr,100) as srcaddr, left(destaddr,100) as destaddr, pronum, iface FROM sysrouteadv order by pronum asc"""
    item_list = readDb(sql,)
    return json.dumps(item_list)

@route('/addroute')
@checkAccess
def addroute():
    s = request.environ.get('beaker.session')
    sql = " SELECT ifacename FROM netiface where status='UP' "
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
    else:
       msg = {'color':'red','message':u'添加失败'}
       return(template('staticroute',msg=msg,session=s))

@route('/addadvroute')
@checkAccess
def addroute():
    s = request.environ.get('beaker.session')
    netmod.InitNIinfo()
    sql = " SELECT ifacename FROM netiface where status='UP' UNION select value as ifacename FROM sysattr where status='1' and servattr='vpnrelay'"
    ifacelist_result = readDb(sql,)
    return template('addadvroute',session=s,info={},ifacelist_result=ifacelist_result)

@route('/addadvroute',method="POST")
@checkAccess
def do_addroute():
    s = request.environ.get('beaker.session')
    rulename = request.forms.get("rulename")
    srcaddr = request.forms.get("srcaddr").replace('\r\n','\n').strip()
    destaddr = request.forms.get("destaddr").replace('\r\n','\n').strip()
    pronum = request.forms.get("pronum")
    outdev = request.forms.get("ifacename")
    alladdr=srcaddr.split('\n')+destaddr.split('\n')
    #提交判断
    if outdev == '' or rulename == '':
       msg = {'color':'red','message':u'描述或出口未填写，添加失败'}
       return(template('advroute',msg=msg,session=s))
    if int(pronum) <100 or int(pronum) >32765 :
       msg = {'color':'red','message':u'优先级值填写错误，添加失败'}
       return(template('advroute',msg=msg,session=s))
    for ipmask in alladdr :
        if netmod.checkipmask(ipmask) == False and ipmask != '':
           msg = {'color':'red','message':u'地址格式错误，添加失败'}
           return(template('advroute',msg=msg,session=s))
    cmdDict=cmds.getdictrst('ip rule add prio %s fwmark 1000 dev %s' % (pronum,outdev))
    if cmdDict.get('status') == 0:
       sql = """ insert into sysrouteadv(rulename,srcaddr,destaddr,pronum,iface) VALUES(%s,%s,%s,%s,%s) """
       data = (rulename,srcaddr,destaddr,int(pronum),outdev)
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
    sql = " SELECT ifacename FROM netiface where status='UP' UNION select value as ifacename FROM sysattr where status='1' and servattr='vpnrelay'"
    ifacelist_result = readDb(sql,)
    sql2 = """ SELECT rulename,srcaddr,destaddr,pronum,iface FROM sysrouteadv WHERE id=%s """
    result = readDb(sql2,(id,))
    return template('addadvroute',session=s,info=result[0],ifacelist_result=ifacelist_result)

@route('/editadvroute/<id>',method="POST")
@checkAccess
def do_editadvroute(id):
    s = request.environ.get('beaker.session')
    rulename = request.forms.get("rulename")
    srcaddr = request.forms.get("srcaddr").replace('\r\n','\n').strip()
    destaddr = request.forms.get("destaddr").replace('\r\n','\n').strip()
    pronum = request.forms.get("pronum")
    outdev = request.forms.get("ifacename")
    alladdr=srcaddr.split('\n')+destaddr.split('\n')
    #提交判断
    if outdev == '' or rulename == '':
        msg = {'color':'red','message':u'描述或出口未填写，添加失败'}
        return(template('advroute',msg=msg,session=s))
    if int(pronum) <0 or int(pronum) >32765 :
        msg = {'color':'red','message':u'优先级值填写错误，添加失败'}
        return(template('advroute',msg=msg,session=s))
    for ipmask in alladdr :
        if netmod.checkipmask(ipmask) == False and ipmask != '':
           msg = {'color':'red','message':u'地址格式错误(%s)，添加失败' % ipmask}
           return(template('advroute',msg=msg,session=s))
    cmdDict=cmds.getdictrst('ip rule add prio %s fwmark 1000%s dev %s' % (pronum,id,outdev))
    if cmdDict.get('status') == 0:
       sql = """ UPDATE sysrouteadv SET rulename=%s,srcaddr=%s,destaddr=%s,pronum=%s,iface=%s WHERE id=%s """
       data = (rulename,srcaddr,destaddr,int(pronum),outdev,id)
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

@route('/delroute/<stype>/<id>')
@checkAccess
def deliface(stype,id):
    s = request.environ.get('beaker.session')
    if stype == 'sys' or stype == 'static' :
       sqlquery = " select dest,netmask,gateway FROM sysroute WHERE id=%s "
       sql = " DELETE FROM sysroute WHERE id=%s "
    else:
       sqlquery = " select srcaddr,destaddr,pronum,iface as outdev FROM sysrouteadv WHERE id=%s "
       sql = " DELETE FROM sysrouteadv WHERE id=%s "
    resultA = readDb(sqlquery,(id,))
    # 判断删除入口并返回到指定界面
    if stype == 'sys':
       tpl = 'routeconf'
    elif stype == 'static':
       tpl = 'staticroute'
    elif stype == 'adv':
       tpl = 'advroute'
    # 判断提交的指令
    result = writeDb(sql,(id,))
    if result == True:
       if stype == 'adv':
          try:
             if resultA[0].get('srcaddr') == '' and resultA[0].get('destaddr') != '':
                cmds.getdictrst('ip rule del prio %s to %s' % (resultA[0].get('pronum'),resultA[0].get('destaddr')))
             elif resultA[0].get('destaddr') == '' and resultA[0].get('srcaddr') != '':
                cmds.getdictrst('ip rule del prio %s from %s dev %s' % (resultA[0].get('pronum'),resultA[0].get('srcaddr')))
             elif resultA[0].get('destaddr') == '' and resultA[0].get('srcaddr') == '':
                cmds.getdictrst('ip rule del prio %s dev %s' % (resultA[0].get('pronum'),resultA[0].get('outdev')))
             else:
                cmds.getdictrst('ip rule del prio %s from %s to %s' % (resultA[0].get('pronum'),resultA[0].get('srcaddr'),resultA[0].get('destaddr')))
             msg = {'color':'green','message':u'删除成功'}
             return template(tpl,session=s,msg=msg)
          except:
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
    info['v4addr'] = 'Lan: '+netmod.NatIP()+'\tWan: '+netmod.NetIP()
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

# UTM添加规则
@route('/addutmrule')
@checkAccess
def addutmrule():
    """UTM配置 添加页"""
    s = request.environ.get('beaker.session')
    return template('addutmrule',session=s,msg={},info={})

@route('/addutmrule',method='POST')
@checkAccess
def do_addutmrule():
    """UTM配置 添加页"""
    s = request.environ.get('beaker.session')
    rulename = request.forms.get("rulename")
    pronum = request.forms.get("pronum")
    actzone = request.forms.get("actzone")
    srcaddr = request.forms.get("srcaddr").replace('\r\n','\n').strip()
    dstaddr = request.forms.get("dstaddr").replace('\r\n','\n').strip()
    sproto = request.forms.get("sproto")
    sport = request.forms.get("sport")
    dproto = request.forms.get("dproto")
    dport = request.forms.get("dport")
    runaction = request.forms.get("runaction")
    sql = "insert into ruleconfutm(rulename,pronum,actzone,srcaddr,dstaddr,sproto,sport,dproto,dport,runaction) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    data = (rulename,pronum,actzone,srcaddr,dstaddr,sproto,sport,dproto,dport,runaction)
    if not (rulename and pronum):
          msg = {'color':'red','message':u'规则名称或优先级未填写,添加失败'}
          return template('utmruleconf',session=s,msg=msg,info={})
    alladdr=srcaddr.split('\n')+dstaddr.split('\n')
    for ipmask in alladdr :
        if netmod.checkipmask(ipmask) == False and ipmask != '':
           msg = {'color':'red','message':u'源地址或目标地址格式错误，添加失败'}
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
    sql = " SELECT rulename,actzone,srcaddr,sproto,sport,dstaddr,dproto,dport,runaction,pronum from ruleconfutm where status='1' and id=%s"
    result = readDb(sql,(id,))
    return template('addutmrule',session=s,msg={},info=result[0])

@route('/editutmrule/<id>',method='POST')
@checkAccess
def do_editutmrule(id):
    """UTM配置 更新页"""
    s = request.environ.get('beaker.session')
    rulename = request.forms.get("rulename")
    pronum = request.forms.get("pronum")
    actzone = request.forms.get("actzone")
    srcaddr = request.forms.get("srcaddr").replace('\r\n','\n').strip()
    dstaddr = request.forms.get("dstaddr").replace('\r\n','\n').strip()
    sproto = request.forms.get("sproto")
    sport = request.forms.get("sport")
    dproto = request.forms.get("dproto")
    dport = request.forms.get("dport")
    runaction = request.forms.get("runaction")
    sql = "update ruleconfutm set rulename=%s,pronum=%s,actzone=%s,srcaddr=%s,dstaddr=%s,sproto=%s,sport=%s,dproto=%s,dport=%s,runaction=%s where id=%s"
    data = (rulename,pronum,actzone,srcaddr,dstaddr,sproto,sport,dproto,dport,runaction,id)
    if not (rulename and pronum):
          msg = {'color':'red','message':u'规则名称或优先级未填写,添加失败'}
          return template('utmruleconf',session=s,msg=msg,info={})
    alladdr=srcaddr.split('\n')+dstaddr.split('\n')
    for ipmask in alladdr :
        if netmod.checkipmask(ipmask) == False and ipmask != '':
           msg = {'color':'red','message':u'源地址或目标地址格式错误，添加失败'}
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
    """UTM配置 添加页"""
    s = request.environ.get('beaker.session')
    netmod.InitNIinfo()
    sql = " SELECT ifacename FROM netiface where status='UP' UNION select value as ifacename FROM sysattr where status='1' and servattr='vpnrelay'"
    ifacelist_result = readDb(sql,)
    return template('addnatrule',session=s,msg={},info={},ifacelist_result=ifacelist_result)

@route('/addnatrule',method='POST')
@checkAccess
def do_addutmrule():
    """UTM配置 添加页"""
    s = request.environ.get('beaker.session')
    rulename = request.forms.get("rulename")
    dstmatch = request.forms.get("dstmatch")
    srcaddr = request.forms.get("srcaddr").replace('\r\n','\n').strip()
    dstaddr = request.forms.get("dstaddr").replace('\r\n','\n').strip()
    runaction = request.forms.get("runaction")
    runobject = request.forms.get("runobject")
    if runaction == 'SNAT':
       runobject = request.forms.get("runobject")
       if netmod.checkip(runobject) == False:
          msg = {'color':'red','message':u'源地址转换不能填写非IP类型,添加失败'}
          return template('natruleconf',session=s,msg=msg,info={})
    else :
       runobject = request.forms.get("runobject2")
    sql = "insert into ruleconfnat(rulename,srcaddr,dstmatch,dstaddr,runaction,runobject) VALUES(%s,%s,%s,%s,%s,%s)"
    data = (rulename,srcaddr,dstmatch,dstaddr,runaction,runobject)
    alladdr=srcaddr.split('\n')+dstaddr.split('\n')
    for ipmask in alladdr :
        if netmod.checkipmask(ipmask) == False and ipmask != '':
           msg = {'color':'red','message':u'源地址或目标地址格式错误，添加失败'}
           return(template('natruleconf',msg=msg,session=s))
    result = writeDb(sql,data)
    if result == True:
       msg = {'color':'green','message':u'添加成功'}
       writeUTMconf(action='addconf')
       return template('natruleconf',session=s,msg=msg,info={})

@route('/editnatrule/<id>')
@checkAccess
def editutmrule(id):
    """UTM配置 添加页"""
    s = request.environ.get('beaker.session')
    netmod.InitNIinfo()
    sql = " SELECT ifacename FROM netiface where status='UP' UNION select value as ifacename FROM sysattr where status='1' and servattr='vpnrelay'"
    ifacelist_result = readDb(sql,)
    sql2 = " SELECT rulename,srcaddr,dstmatch,dstaddr,runaction,runobject,runobject as runobject2 from ruleconfnat where status='1' and id=%s"
    result = readDb(sql2,(id,))
    return template('addnatrule',session=s,msg={},info=result[0],ifacelist_result=ifacelist_result)

@route('/editnatrule/<id>',method='POST')
@checkAccess
def do_editutmrule(id):
    """UTM配置 更新页"""
    s = request.environ.get('beaker.session')
    rulename = request.forms.get("rulename")
    dstmatch = request.forms.get("dstmatch")
    srcaddr = request.forms.get("srcaddr").replace('\r\n','\n').strip()
    dstaddr = request.forms.get("dstaddr").replace('\r\n','\n').strip()
    runaction = request.forms.get("runaction")
    runobject = request.forms.get("runobject")
    if runaction == 'SNAT':
       runobject = request.forms.get("runobject")
       if netmod.checkip(runobject) == False:
          msg = {'color':'red','message':u'源地址转换不能填写非IP类型,添加失败'}
          return template('natruleconf',session=s,msg=msg,info={})
    else :
       runobject = request.forms.get("runobject2")
    sql = "update ruleconfnat set rulename=%s,srcaddr=%s,dstmatch=%s,dstaddr=%s,runaction=%s,runobject=%s where id=%s"
    data = (rulename,srcaddr,dstmatch,dstaddr,runaction,runobject,id)
    alladdr=srcaddr.split('\n')+dstaddr.split('\n')
    for ipmask in alladdr :
        if netmod.checkipmask(ipmask) == False and ipmask != '':
           msg = {'color':'red','message':u'源地址或目标地址格式错误，添加失败'}
           return(template('natruleconf',msg=msg,session=s))
    result = writeDb(sql,data)
    if result == True:
       writeUTMconf(action='uptconf')
       msg = {'color':'green','message':u'更新成功'}
       return template('natruleconf',session=s,msg=msg,info={})

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

@route('/api/getutmruleinfo',method=['GET', 'POST'])
@checkAccess
def getifaceinfo():
    sql = """ SELECT id,rulename,actzone,left(srcaddr,100) as srcaddr,left(dstaddr,100) as dstaddr,concat(sproto,':',sport) as sport,concat(dproto,':',dport) as dport,runaction,pronum 
              FROM ruleconfutm order by pronum """
    result = readDb(sql,)
    return json.dumps(result)

@route('/api/getnatruleinfo',method=['GET', 'POST'])
@checkAccess
def getifaceinfo():
    sql = " SELECT id,rulename,left(srcaddr,100) as srcaddr,left(concat((case dstmatch when 1 then '[==] ' when 0 then '[ !=] ' end),dstaddr),100) as dstaddr,runaction,runobject FROM ruleconfnat "
    iface_list = readDb(sql,)
    return json.dumps(iface_list)

# 策略配置
@route('/api/getpolicylist',method=['GET', 'POST'])
@checkAccess
def getifaceinfo():
    sql = " SELECT id,name,pushdns,left(pushroute,100) as pushroute,left(pushnoroute,100) as pushnoroute FROM vpnpolicy "
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
    return template('addpolicyconf',session=s,info={})


@route('/addpolicy',method="POST")
@checkAccess
def do_addpolicy():
    """POST"""
    s = request.environ.get('beaker.session')
    name = request.forms.get("name")
    pushdns = request.forms.get("pushdns").replace('\r\n','\n').strip()
    pushroute = request.forms.get("pushroute").replace('\r\n','\n').strip()
    pushnoroute = request.forms.get("pushnoroute").replace('\r\n','\n').strip()
    allipmask = pushroute.split('\n')+pushnoroute.split('\n')
    for ip in pushdns.split('\n') :
        if netmod.checkip(ip) == False and ip != '':
           msg = {'color':'red','message':u'DNS内容检测错误,更新失败'}
           return(template('policyconf',session=s,msg=msg,info={}))
    for ipmask in allipmask :
        if netmod.checkipmask(ipmask) == False and ipmask != '':
           msg = {'color':'red','message':u'路由内容检测错误,更新失败'}
           return(template('policyconf',session=s,msg=msg,info={}))

    sql = "INSERT INTO vpnpolicy(name,pushdns,pushroute,pushnoroute) VALUES(%s,%s,%s,%s)"
    data=(name,pushdns,pushroute,pushnoroute)
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
    sql = "select name,pushdns,pushroute,pushnoroute from vpnpolicy WHERE id=%s"
    result = readDb(sql,(id,))
    if result :
       return(template('addpolicyconf',session=s,info=result[0]))

@route('/editpolicy/<id>',method="POST")
@checkAccess
def editpolicy(id):
    """修改策略"""
    s = request.environ.get('beaker.session')
    name = request.forms.get("name")
    pushdns = request.forms.get("pushdns").replace('\r\n','\n').strip()
    pushroute = request.forms.get("pushroute").replace('\r\n','\n').strip()
    pushnoroute = request.forms.get("pushnoroute").replace('\r\n','\n').strip()
    allipmask = pushroute.split('\n')+pushnoroute.split('\n')
    # 内容检测
    for ip in pushdns.split('\n') :
        if netmod.checkip(ip) == False and ip != '':
           msg = {'color':'red','message':u'DNS内容检测错误,更新失败'}
           return(template('policyconf',session=s,msg=msg,info={}))
    for ipmask in allipmask :
        if netmod.checkipmask(ipmask) == False and ipmask != '' :
           msg = {'color':'red','message':u'路由内容检测错误,更新失败'}
           return(template('policyconf',session=s,msg=msg,info={}))

    sql = "UPDATE vpnpolicy set name=%s,pushdns=%s,pushroute=%s,pushnoroute=%s where id=%s"
    data=(name,pushdns,pushroute,pushnoroute,id)
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
    sql = " update sysattr set value=%s where attr='vpnserver' "
    iidata = json.dumps(idata)
    result = writeDb(sql,(iidata,))
    #sql = " INSERT INTO vpnservconf(servmode,authtype,ipaddr,servport,virip,virmask,maxclient,maxuser,authtimeout,authnum,locktime,comp,cisco) values ('server',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    #data = (authtype,ipaddr,servport,virip,virmask,maxclient,maxuser,authtimeout,authnum,locktime,comp,cisco)
    #result = writeDb(sql,data)
    if result == True :
       writeVPNconf(action='addconf')
       cmds.servboot('ocserv')
       writeUTMconf(action='uptconf')
       msg = {'color':'green','message':u'配置保存成功'}
       return template('vpnservconf',session=s,msg=msg,info={})

@route('/addclientconf')
@checkAccess
def addclientconf():
    """新增服务配置项"""
    s = request.environ.get('beaker.session')
    #获取证书选择列表
    conncerts_list=[]
    status,result=cmds.gettuplerst('find %s/conncerts -name \'*.p12\' -exec basename {} \;|sort' % gl.get_value('certdir'))
    for i in result.split('\n'):
        if str(i) != "":
           infos = {}
           infos['filename']=str(i)
           conncerts_list.append(infos)
    #加载现有配置
    sql = " select value from sysattr where attr='vpnclient' "
    idata = readDb(sql,)
    try:
       info = json.loads(idata[0].get('value'))
    except:
       return template('addvpncltconfig',session=s,msg={},info={},conncerts_list=conncerts_list)
    return template('addvpncltconfig',session=s,msg={},info=info,conncerts_list=conncerts_list)

@route('/addclientconf',method="POST")
@checkAccess
def addclientconf():
    """新增服务配置项"""
    s = request.environ.get('beaker.session')
    authtype = request.forms.get("authtype")
    idata=dict()
    if authtype == '0' :
       idata['certinfo'] = request.forms.get("certinfo")
       idata['vpnpass'] = request.forms.get("vpnpass")
    elif authtype == '1' :
       idata['vpnuser'] = request.forms.get("vpnuser")
       idata['vpnpass'] = request.forms.get("vpnpass")
    elif authtype == '2' :
       idata['service'] = 'off'
    else :
       msg = {'color':'green','message':u'验证类型错误，保存失败'}    
       return template('addvpncltconfig',session=s,msg=msg,info={})
    idata['authtype'] = request.forms.get("authtype")
    idata['ipaddr'] = request.forms.get("ipaddr")
    idata['servport'] = request.forms.get("servport")
    idata['tunid'] = request.forms.get("tunid")
    idata['vmtu'] = request.forms.get("vmtu")
    idata['chkconn'] = request.forms.get("chkconn")
    if not (idata['ipaddr'] and idata['servport'] and idata['tunid'] and idata['vmtu']):
       msg = {'color':'red','message':u'配置保存失败，关键参数未设置'}
       sql = " select value from sysattr where attr='vpnclient' "
       idata = readDb(sql,)
       try:
          info = json.loads(idata[0].get('value'))
       except:
          return template('addvpncltconfig',session=s,msg=msg,info={})
       return template('addvpncltconfig',session=s,msg=msg,info=info)
    sql = " update sysattr set value=%s where attr='vpnclient' "
    iidata=json.dumps(idata)
    result = writeDb(sql,(iidata,))
    if result == True :
       msg = {'color':'green','message':u'配置保存成功'}
       writeVPNconf(action='uptcltconf')
       cmds.servboot('vpnconn')
       writeUTMconf(action='uptconf')
       #获取证书选择列表
       conncerts_list=[]
       status,result=cmds.gettuplerst('find %s/conncerts -name \'*.p12\' -exec basename {} \;|sort' % gl.get_value('certdir'))
       for i in result.split('\n'):
           if str(i) != "":
              infos = {}
              infos['filename']=str(i)
              conncerts_list.append(infos)
       return template('addvpncltconfig',session=s,msg=msg,info=idata,conncerts_list=conncerts_list)


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
    commonname = request.forms.get("commonname")
    organization = request.forms.get("organization")
    expiration = request.forms.get("expiration")
    createdate = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    comment = 'CA*Server'
    #检测表单各项值，如果出现为空的表单，则返回提示
    if not (commonname and organization and expiration):
        message = "表单不允许为空！"
        return '-2'

    if expiration.isdigit() == False :
       message = "有效期不是一个整数"
       return '-2'

    result = mkcert(ct=certtype,cn=commonname,ou=organization,ex=expiration,comment=comment)
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
    name, ext = os.path.splitext(upload.filename)
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

# 策略配置
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
    name, ext = os.path.splitext(upload.filename)
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

if __name__ == '__main__' :
   sys.exit()
