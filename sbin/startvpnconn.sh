#!/bin/sh
# +-----------------------------------------------------------------------+
# |       Author: Cheng Wenfeng   <277546922@qq.com>                      |
# +-----------------------------------------------------------------------+
#
wkdir=$(cd $(dirname $0); pwd)
if [ ! -f $wkdir/main.py ] ;then
   wkdir=$(cd $(dirname $0)/../; pwd)
fi
PATH=$PATH:$wkdir/sbin
myapp=$(which openconnect)
confdir="$wkdir/plugins/ocserv"
pidfile="$wkdir/plugins/ocserv/run/openconn.pid"

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

if [ -x $wkdir/sbin/vpnc-script ];then
   script="-s $wkdir/sbin/vpnc-script"
fi

if echo ${2} |grep -q '[^0-9]' || [ x"${2}" = x'' ]; then
   echo "Tun ID error."
   exit 1
fi

#获取客户端配置信息
for fileID in $(find $confdir -name "ocserv_client_${2}.conf"|xargs);do
    toDict $fileID openconn_conf
    if [ ${uDict["authtype"]} = "1" ];then
       server=${uDict["ipaddr"]}
       servport=${uDict["servport"]}
       tunid=${uDict["tunid"]}
       vmtu=${uDict["vmtu"]} 
       vpnuser=${uDict["vpnuser"]}
       connpass=${uDict["vpnpass"]}
       chkdtls=${uDict["dtls"]}
       if [ ${uDict["dtls"]} = "1"  ];then
          OPTIONS="-u $vpnuser --pfs $server:$servport --interface=tun${tunid} $script -m $vmtu --reconnect-timeout 10 --no-cert-check --syslog"
       else
          OPTIONS="-u $vpnuser --no-dtls $server:$servport --interface=tun${tunid} $script -m $vmtu --reconnect-timeout 10 --no-cert-check --syslog"
       fi
    elif [ ${uDict["authtype"]} = "0" ];then
       server=${uDict["ipaddr"]}
       servport=${uDict["servport"]}
       tunid=${uDict["tunid"]}
       vmtu=${uDict["vmtu"]}
       certinfo=${uDict["certinfo"]}
       connpass=${uDict["certpass"]}
       if [ ${uDict["dtls"]} = "1"  ];then
          OPTIONS="-c $wkdir/certs/conncerts/$certinfo --pfs $server:$servport --interface=tun${tunid} $script -m $vmtu --reconnect-timeout 10 --no-cert-check --syslog"
       else
          OPTIONS="-c $wkdir/certs/conncerts/$certinfo --no-dtls $server:$servport --interface=tun${tunid} $script -m $vmtu --reconnect-timeout 10 --no-cert-check --syslog"
       fi
    fi
done

case "$1" in
  start)
      echo -en "Starting VPNConnServer TunINFO : [${2} $server]:\t\t"
      /sbin/modprobe tun >/dev/null 2>&1
      $wkdir/sbin/start-stop-daemon --start -m -p $pidfile --exec $myapp -- $OPTIONS <<< $connpass -b >/dev/null 2>&1
      RETVAL=$?
      #echo
      if [ $RETVAL -eq 0 ] ;then
         echo "Done..."
      else
         echo "Failed"
      fi
      ;;
  stop)
      echo -en "Stoping VPNConnServer TunINFO: [${2} $server ]:\t\t"
      #$wkdir/sbin/start-stop-daemon --stop  --name openconnect >/dev/null 2>&1
      pids=$(ps ax|grep "openconnect.*tun${2}" |grep -v 'grep'|awk '{print $1}')
      if [ x"$pids" = x"" ];then
          echo "Failed" 
          exit 1
      else
          kill -9 $pids
      fi
      RETVAL=$?
      #echo
      #$wkdir/sbin/startnetworks.sh restart >/dev/null 2>&1 #接口调入vpnc-script
      if [ $RETVAL -eq 0 ] ;then
  	     echo "Done..."
      else
         echo "Failed"
      fi
      ;;
  status)
      for pid in  $( ps ax|grep "openconnect.*tun${2}" |grep -v 'grep'|awk '{print $1}');do
          echo $pid
      done
      ;;
  restart)
      $0 stop ${2}
      $0 start ${2}
      RETVAL=$?
      ;;
  *)
      echo "Usage: $0 {start|stop|restart|status}"
      exit 2
esac
