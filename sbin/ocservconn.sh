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
pytools=$(which python27)

getid=$($pytools $wkdir/tools/API.py API getUserLineID $USERNAME)

if [ "$getid" == "0" ];then
   getid=$GROUPNAME
fi

if [ "$REASON" = "connect" ];then
   # Disable the firewall for the user's device
   $ipset add vpnpolicy_src_$getid $IP_REMOTE >/dev/null 2>&1
   # writelog
   $pytools $wkdir/tools/API.py API wrtvpnlogin "Ocserv" "登录成功,分配地址:$IP_REMOTE" $USERNAME $IP_REAL >/dev/null 2>&1
else
   $ipset del vpnpolicy_src_$getid $IP_REMOTE >/dev/null 2>&1
   # writelog
   $pytools $wkdir/tools/API.py API wrtvpnlogin "Ocserv" "退出登录,释放地址:$IP_REMOTE" $USERNAME $IP_REAL >/dev/null 2>&1
fi

exit 0
