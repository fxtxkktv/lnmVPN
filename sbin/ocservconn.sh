#!/bin/bash
# +-----------------------------------------------------------------------+
# |       Author: Cheng Wenfeng   <277546922@qq.com>                      |
# +-----------------------------------------------------------------------+
#
wkdir=$(cd $(dirname $0); pwd)
if [ ! -f $wkdir/main.py ] ;then
   wkdir=$(cd $(dirname $0)/../; pwd)
fi
ipset=$(which ipset)

source $wkdir/venv/bin/activate
pytools="$wkdir/venv/bin/python"

getid=$($pytools $wkdir/tools/API.py API getUserLineID $USERNAME)

if [ "$getid" == "0" ];then
   getid=$GROUPNAME
fi

if [ "$REASON" = "connect" ];then
   # Disable the firewall for the user's device
   $ipset add VPN_Client_$getid $IP_REMOTE >/dev/null 2>&1
   # writelog
   $pytools $wkdir/tools/API.py API wrtvpnlogin "Ocserv" "登录成功,分配地址:$IP_REMOTE" $USERNAME $IP_REAL >/dev/null 2>&1
   # Reload User StaticRoute
   $wkdir/sbin/AdvRouteAPI.sh onlySR >/dev/null 2>&1
   # Reload Server Route
   if [ -f $wkdir/plugins/ocserv/servroute.conf ];then
      routestr=$(cat $wkdir/plugins/ocserv/servroute.conf|grep "^$USERNAME"|awk -F, '{print $NF}')
      ip route add $routestr via $IP_REMOTE dev $DEVICE >/dev/null 2>&1
   fi
else
   $ipset del VPN_Client_$getid $IP_REMOTE >/dev/null 2>&1
   # writelog
   $pytools $wkdir/tools/API.py API wrtvpnlogin "Ocserv" "退出登录,释放地址:$IP_REMOTE" $USERNAME $IP_REAL >/dev/null 2>&1
fi

exit 0
