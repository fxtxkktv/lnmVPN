#!/bin/bash
# +-----------------------------------------------------------------------+
# |       Author: Cheng Wenfeng   <277546922@qq.com>                      |
# +-----------------------------------------------------------------------+
#
wkdir=$(cd $(dirname $0); pwd)
if [ ! -f $wkdir/main.py ] ;then
   wkdir=$(cd $(dirname $0)/../; pwd)
fi
PATH=$PATH:$wkdir/sbin
iconf="$wkdir/plugins/networks"

declare -A uDict
declare -A nDict

function toDict() {
   uDict=()
   ValueArry=$(grep "^$2" $1|sed "s/^${2}=//g"|grep -Po '(?<=\()[^)]+(?=\))')
   for x in $ValueArry ;do
	   key=$(echo $x|awk -F= '{print $1}')
	   value=$(echo $x|awk -F= '{print $2}'|sed 's/"//g')
	   uDict+=(["$key"]=$value)
   done	
}

function getifaceID() {
   nDict=()
   ValueArry=$(grep "$2" $1|sed "s/^${2}=//g"|grep -Po '(?<=\()[^)]+(?=\))')
   for x in $ValueArry ;do
       key=$(echo $x|awk -F= '{print $1}')
       value=$(echo $x|awk -F= '{print $2}'|sed 's/"//g')
       nDict+=(["$key"]=$value)
   done
}

function Networks(){
inum=70
#加载网络接口
for servID in $(awk -F= '/^netiface_[0-9]/{print $1}' $iconf/netiface.conf);do
    toDict $iconf/netiface.conf $servID
    # 处理IP信息
    ip link set ${uDict["ifacename"]} up >/dev/null 2>&1
    ip addr flush dev ${uDict["ifacename"]} >/dev/null 2>&1
    ip addr add local ${uDict["ipaddr"]}/${uDict["netmask"]} dev ${uDict["ifacename"]} >/dev/null 2>&1
    if [ "${uDict["defaultgw"]}" = "1" ] && [ "${uDict["gateway"]}" != "" ];then
       route add default gw ${uDict["gateway"]} >/dev/null 2>&1
       ip route flush table ${uDict["id"]} >/dev/null 2>&1
       ip route replace default via ${uDict["gateway"]} dev ${uDict["ifacename"]} src ${uDict["ipaddr"]} proto static table ${uDict["id"]} >/dev/null 2>&1
       ip route append prohibit default table ${uDict["id"]} metric 1 proto static >/dev/null 2>&1
    elif [ "${uDict["defaultgw"]}" = "0" ] && [ "${uDict["gateway"]}" != "" ];then
       ip route flush table ${uDict["id"]} >/dev/null 2>&1
       ip route replace default via ${uDict["gateway"]} dev ${uDict["ifacename"]} src ${uDict["ipaddr"]} proto static table ${uDict["id"]} >/dev/null 2>&1
       ip route append prohibit default table ${uDict["id"]} metric 1 proto static >/dev/null 2>&1
    else
        true
    fi
    # 处理扩展IP
    for line in $(echo ${uDict["extip"]}|sed 's/;/ /g');do
      if [ "$line" != "" ];then
         extipinfos=$(echo $line|awk -F/ '{print $1"/"$2}')
         ip addr add local $extipinfos dev ${uDict["ifacename"]} >/dev/null 2>&1
         extgwinfos=$(echo $line|awk -F/ '{print $3}')
         if [ ${extgwinfos} != "" ];then
            ip route flush table ${uDict["id"]} >/dev/null 2>&1
            ip route replace default via ${uDict["gateway"]} dev ${uDict["ifacename"]} src ${uDict["ipaddr"]} proto static table ${uDict["id"]} >/dev/null 2>&1
            ip route append prohibit default table ${uDict["id"]} metric 1 proto static >/dev/null 2>&1
         fi
      fi
   done
   # 增加接口路由
   if [ "${uDict["gateway"]}" != "" ];then
      ip rule del prio $inum
      ip rule add prio $inum from ${uDict["ipaddr"]}/${uDict["netmask"]} table ${uDict["id"]} >/dev/null 2>&1 
      let inum+=1
   fi
done

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


#加载用户定义高级路由[配合IPTABLES+IPSET]
#清理旧的
for i in $(ip rule |awk -F: '$1<32766 && $1>95 {print $1}');do
        ip rule del prio $i
done

# 加载高级路由规则
advdesc=$(awk -F= '/^advroute_[0-9]/{print $1}' $iconf/route.conf)
if [ "$advdesc" != "" ];then
   # 默认网关修改为高级路由模式
   for gw in $(python $wkdir/tools/Functions.pyc API getgw defaultgw);do
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
   ip rule del prio 50 table main >/dev/null 2>&1
   ip rule add prio 50 table main >/dev/null 2>&1
   for servID in $(awk -F= '/^advroute_[0-9]/{print $1}' $iconf/route.conf);do
      id=$(echo $servID|awk -F_ '{print $2}')
      toDict $iconf/route.conf $servID
      #判断下如果接口的IP地址无法获取，自动忽略该接口
      ifaceaddr=$(python $wkdir/tools/Functions.pyc API getniaddr "${uDict["iface"]}")
      if [ "$ifaceaddr" = "False" ];then
         continue
      fi
      if [ ${uDict["iface"]} = "tun1000" ];then
         if [ ${uDict["pronum"]} = "99" ];then
	    for dnsserv in $(echo ${uDict["dnsserver"]}|sed 's/-/ /g');do
	        ip rule add prio 99 to $dnsserv table 1000 >/dev/null 2>&1
	    done
         else
            ip rule add prio ${uDict["pronum"]} fwmark 1000${id} table 1000 >/dev/null 2>&1
         fi
      else
         getifaceID $iconf/netiface.conf "ifacename=${uDict["iface"]}"
         ip rule add prio ${uDict["pronum"]} fwmark 1000${id} table ${nDict["id"]} >/dev/null 2>&1
      fi
      ip route flush cache >/dev/null 2>&1
   done
fi
}

case "$1" in
  start)
        echo -en "Starting NetworksServer:\t\t"
	Networks
        RETVAL=$?
        #echo
        if [ $RETVAL -eq 0 ] ;then
           echo "Done..."
        else
           echo "Failed"
        fi
        ;;
  stop)
        echo -en "Stoping NetworksServer:\t\t"
        RETVAL=$?
        if [ $RETVAL -eq 0 ] ;then
           echo "Done..."
        else
           echo "Failed"
        fi
        ;;
  restart)
        $0 stop
        $0 start
        RETVAL=$?
        ;;
  *)
        echo "Usage: $0 {start|stop|restart}"
        exit 2
esac

exit 0
