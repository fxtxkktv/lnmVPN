#!/bin/bash
# +-----------------------------------------------------------------------+
# |       Author: Cheng Wenfeng   <277546922@qq.com>                      |
# +-----------------------------------------------------------------------+
#
wkdir=$(cd $(dirname $0); pwd)
if [ ! -f $wkdir/main.py ] ;then
   wkdir=$(cd $(dirname $0)/../; pwd)
fi

source $wkdir/venv/bin/activate

PATH=$PATH:$wkdir/sbin
iconf="$wkdir/plugins/networks"
pytools="$wkdir/venv/bin/python"

# load process lock
lockfile="$wkdir/plugins/firewall/advroute_lock.pid"
if [ -f $lockfile ] ;then
   rm -f $lockfile
   exit 0
else
   echo $$ > $lockfile
fi

declare -A uDict

function toDict() {
   uDict=()
   ValueArry=$(grep "^$2" $1|sed "s/^${2}=//g"|grep -Po '(?<=\()[^)]+(?=\))')
   for x in $ValueArry ;do
	   key=$(echo $x|awk -F= '{print $1}')
	   value=$(echo $x|awk -F= '{print $2}'|sed 's/"//g')
	   uDict+=(["$key"]=$value)
   done	
}

function mkADVRoute(){
   for servID in $(awk -F= -v R=$1 '{if($1~R)print $1}' $iconf/route.conf);do
      id=$(echo $servID|awk -F_ '{print $2}')
      toDict $iconf/route.conf $servID
      if [ ${uDict["rttype"]} = "A" ];then
         ip route flush table $id >/dev/null 2>&1
         ifaceaddr=$($pytools $wkdir/tools/API.py API getniaddr "${uDict["iflist"]}")
         #忽略接口不存在地址的情况路由
         if [ $ifaceaddr = "" ];then
            continue
         fi
         if [[ ${uDict["iflist"]} =~ "tun10" ]];then
            echo  $id
            ip route flush table $id >/dev/null 2>&1
            ip route replace default dev ${uDict["iflist"]} src $ifaceaddr proto static table $id >/dev/null 2>&1
            ip route append prohibit default table $id metric 1 proto static >/dev/null 2>&1
         else
            ifaceniname=$($pytools $wkdir/tools/API.py API getniname "${uDict["iflist"]}")
            ifacegw=$($pytools $wkdir/tools/API.py API getgw "${uDict["iflist"]}")
            ip route replace default table $id via $ifacegw dev $ifaceniname src $ifaceaddr >/dev/null 2>&1
         fi
      elif [ ${uDict["rttype"]} = "B" ];then
         ip route flush table $id >/dev/null 2>&1
         for i in $(echo ${uDict["iflist"]}|sed 's/,/\n/g');do
             ifaceaddr=$($pytools $wkdir/tools/API.py API getniaddr $i)
             #忽略接口不存在地址的情况路由
             if [ $ifaceaddr = "" ] || [ $ifaceaddr = "False" ];then
                continue
             fi
             ifaceniname=$($pytools $wkdir/tools/API.py API getniname $i)
             ifacegw=$($pytools $wkdir/tools/API.py API getgw $i)
             ifaceweight=$($pytools $wkdir/tools/API.py API getniweight $i)
             gws2+="nexthop via $ifacegw dev $ifaceniname weight $ifaceweight "
         done
         ip route replace default table $id equalize $gws2 >/dev/null 2>&1
      fi
   done
}

#加载用户定义静态路由
for servID in $(awk -F= '/^stroute_[0-9]/{print $1}' $iconf/route.conf);do
    toDict $iconf/route.conf $servID
    if [ ${uDict["type"]}="net" ];then
       rttype='-net'
    else
       rttype='-host'
    fi
    if [ ${uDict["iface"]}="auto" ];then
       route add $rttype ${uDict["dest"]} netmask ${uDict["netmask"]} gw ${uDict["gateway"]} >/dev/null 2>&1
    else
       route add $rttype ${uDict["dest"]} netmask ${uDict["netmask"]} gw ${uDict["gateway"]} dev ${uDict["iface"]} >/dev/null 2>&1
    fi
done

# 禁止静态路由段
if [ "$1" = "onlySR" ];then
   rm -f $lockfile
   exit 0
fi

# Check高级路由规则段
if [ "$1" = "onlyChkAdvRoute" ];then
   RegStr="^advpolicy_$2"
   mkADVRoute $RegStr
   rm -f $lockfile
   exit 0
fi

# 刷新default路由
ip route flush table default >/dev/null 2>&1
for i in $(ip rule |awk -F: '$1<32766 && $1>79 {print $1}');do
        ip rule del prio $i
done

# 增加ADSL接口路由
inum=80
for servID in $(awk -F= '/^netiface_[0-9]/{print $1}' $iconf/netiface.conf);do
    toDict $iconf/netiface.conf $servID
    if [ "${uDict["ifacetype"]}" = "ADSL" ];then    
       ipaddr=$( $pytools $wkdir/tools/API.py API getniaddr ppp${uDict["id"]} )
       gateway=$( $pytools $wkdir/tools/API.py API getgw ppp${uDict["id"]} )
       ip rule del prio $inum >/dev/null 2>&1
       ip rule add prio $inum from $ipaddr table ${uDict["id"]} >/dev/null 2>&1
       ip route flush table ${uDict["id"]} >/dev/null 2>&1
       ip route replace default via $gateway dev ppp${uDict["id"]} src $ipaddr proto static table ${uDict["id"]} >/dev/null 2>&1
       ip route append prohibit default table ${uDict["id"]} metric 1 proto static >/dev/null 2>&1
       # 判断是不是默认网关接口
       if [ "${uDict["defaultgw"]}" = "1" ];then
          ip route replace default via $gateway dev ppp${uDict["id"]} src $ipaddr proto static table default >/dev/null 2>&1
       fi
    fi
    let inum+=1
done

# 加载高级路由[IP ROUTE]
advdesc_I=$(awk -F= '/^advpolicy_[0-9]/{print $1}' $iconf/route.conf)
if [ "$advdesc_I" != "" ];then
   # 默认网关修改为高级路由模式
   for gw in $($pytools $wkdir/tools/API.py API getgw defaultgw);do
       gws+="nexthop via $gw weight 1 "
   done
   ip route replace default table default equalize $gws >/dev/null 2>&1
   # 列举接口系统路由表
   while true ;do
     #移除系统默认路由，直到失败退出
     route del default >/dev/null 2>&1
     if [ $? != 0 ];then
       break
     fi
   done
   # 初始化系统制定策略路由
   RegStr="^advpolicy_"
   mkADVRoute $RegStr
fi

# 加载高级规则[IP RULE]
advdesc_II=$(awk -F= '/^advroute_[0-9]/{print $1}' $iconf/route.conf)
if [ "$advdesc_II" != "" ];then
   for servID in $(awk -F= '/^advroute_[0-9]/{print $1}' $iconf/route.conf);do
      id=$(echo $servID|awk -F_ '{print $2}')
      toDict $iconf/route.conf $servID
      # VPN路由例外
      if [ ${uDict["iface"]} = "tun1000" ];then
         if [ ${uDict["pronum"]} = "99" ];then
	        for dnsserv in $(echo ${uDict["dnsserver"]}|sed 's/-/ /g');do
	            ip rule add prio 99 to $dnsserv table 1000 >/dev/null 2>&1
	        done
         else
            if [ ${uDict["rtattr"]} = "sys" ];then
               ip rule add prio ${uDict["pronum"]} table 1000 >/dev/null 2>&1
            else
               ip rule add prio ${uDict["pronum"]} fwmark 1000${id} table 1000 >/dev/null 2>&1
            fi
         fi
      # 非VPN部分
      else
         #判断高级路由是不是包含本机网络的默认路由 rtattr=sys
         if [ ${uDict["rtattr"]} = "sys" ];then
            ip rule add prio ${uDict["pronum"]} table ${uDict["iface"]} >/dev/null 2>&1
         else
            ip rule add prio ${uDict["pronum"]} fwmark 1000${id} table ${uDict["iface"]} >/dev/null 2>&1
         fi
      fi
      ip route flush cache >/dev/null 2>&1
   done
fi

# 删除锁文件
rm -f $lockfile

exit 0
