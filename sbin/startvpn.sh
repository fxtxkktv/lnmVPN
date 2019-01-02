#!/bin/sh
# +-----------------------------------------------------------------------+
# |       Author: Cheng Wenfeng   <277546922@qq.com>                      |
# +-----------------------------------------------------------------------+
#
wkdir=$(cd $(dirname $0); pwd)
if [ ! -f $wkdir/main.py ] ;then
   wkdir=$(cd $(dirname $0)/../; pwd)
fi
myapp=$(which ocserv)
confdir="$wkdir/plugins/ocserv"
piddir="$wkdir/plugins/ocserv/run"

case "$1" in
  start)
        # Run startup script, if defined
        if [ -x /usr/sbin/ocserv-genkey ]; then
            /usr/sbin/ocserv-genkey
        fi

        echo -en "Starting VPNServer:\t\t"
        /sbin/modprobe tun >/dev/null 2>&1
        for iconf in $(find $confdir -name 'ocserv_server.conf'); do
            pid=ocserv_server.pid
            $wkdir/sbin/start-stop-daemon --start --background -m -p $piddir/$pid --exec $myapp -- -c $iconf
        done
        RETVAL=$?
        #echo
        if [ $RETVAL -eq 0 ] ;then
           echo "Done..."
        else
           echo "Failed"
        fi
        ;;
  stop)
        echo -en "Stoping VPNServer:\t\t"
        $wkdir/sbin/start-stop-daemon --stop  --name ocserv-main >/dev/null 2>&1
        RETVAL=$?
        #echo
        if [ $RETVAL -eq 0 ] ;then
           for pid in  $( ps ax|grep ocserv-main |grep -v 'grep'|awk '{print $1}');do
             kill -9 $pid
           done
           echo "Done..."
        else
           echo "Failed"
        fi
        ;;
  status)
        for pid in  $( ps ax|grep ocserv-main |grep -v 'grep'|awk '{print $1}');do
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
