#!/bin/sh
# +-----------------------------------------------------------------------+
# |       Author: Cheng Wenfeng   <277546922@qq.com>                      |
# +-----------------------------------------------------------------------+
#
wkdir=$(cd $(dirname $0); pwd)
if [ ! -f $wkdir/main.py ] ;then
   wkdir=$(cd $(dirname $0)/../; pwd)
fi
myapp=$(which dnsmasq)
pidfile="$wkdir/plugins/dnsmasq/dnsmasq.pid"
iconf="$wkdir/plugins/dnsmasq/dnsmasq.conf"

case "$1" in
  start)
        echo -en "Starting DNSServer:\t\t"
        $wkdir/sbin/start-stop-daemon --start --background -m -p $pidfile --exec $myapp -- -C $iconf
        RETVAL=$?
        #echo
        if [ $RETVAL -eq 0 ] ;then
	   echo "Done..."
	else
	   echo "Failed"
	fi
        ;;
  stop)
	echo -en "Stoping DNSServer:\t\t"
	$wkdir/sbin/start-stop-daemon --stop --name dnsmasq >/dev/null 2>&1
	RETVAL=$?
        #echo
        if [ $RETVAL -eq 0 ] ;then
	   for pid in  $(ps ax|grep dnsmasq |grep -v 'grep'|awk '{print $1}');do
		kill -9 $pid
	   done
	   echo "Done..."
	else
	   echo "Failed"
	fi
        ;;
  status)
        for pid in  $( ps ax|grep dnsmasq |grep -v 'grep'|awk '{print $1}');do
	   echo $pid
	done
        ;;
  restart)
        $0 stop
        $0 start
        RETVAL=$?
        ;;
  *)
        echo "Usage: $0 {start|stop|restart|status}"
        exit 2
esac
