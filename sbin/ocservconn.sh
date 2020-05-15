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
   ServRte=$($pytools $wkdir/tools/API.py API getVPNautoroute $USERNAME)
   if [ "$ServRte" != "None" ] && [ "$ServRte" != "" ];then
      for i in $(echo $ServRte|sed 's/,/\n/g') ;do
          ip route add $i via $IP_REMOTE dev $DEVICE >/dev/null 2>&1
      done
   fi
else
   $ipset del VPN_Client_$getid $IP_REMOTE >/dev/null 2>&1
   # writelog
   $pytools $wkdir/tools/API.py API wrtvpnlogin "Ocserv" "退出登录,释放地址:$IP_REMOTE" $USERNAME $IP_REAL >/dev/null 2>&1
fi

exit 0
