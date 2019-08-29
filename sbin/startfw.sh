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
ipset=$(which ipset)
iptables=$(which iptables)
pidfile="$wkdir/plugins/firewall/firewall.pid"
ipsetconf="$wkdir/plugins/firewall/ipset.conf"
iptablesconf="$wkdir/plugins/firewall/iptables.conf"

# load kernel options
sysctl -p "$wkdir/template/kernel.conf" >/dev/null 2>&1


ipset_stop(){
ipset flush
for set in $(${ipset} list -name); do
    ipset destroy
done
}

ipset_start(){
ipset restore -! <$ipsetconf
}


IPTABLES_MODULES="nf_nat_ftp nf_conntrack_ftp nf_nat_pptp nf_conntrack_pptp nf_nat_h323 nf_conntrack_h323 nf_nat_sip nf_conntrack_sip"
for mod in $IPTABLES_MODULES; do
    modprobe $mod > /dev/null 2>&1
    let ret+=$?;
done

case "$1" in
  start)
        echo -en "Starting FireWallServer:\t\t"
        ipset_start
        $wkdir/sbin/start-stop-daemon --start --background -m -p $pidfile --exec /sbin/iptables-restore -- $iptablesconf
        #$wkdir/sbin/start-stop-daemon --start --background -m -p /tmp/firewall.pid --exec tcpsvd -- 127.0.0.1:50001 -l firewall
        RETVAL=$?
        #echo
        if [ $RETVAL -eq 0 ] ;then
           echo "Done..."
	    else
           echo "Failed"
	    fi
        ;;
  stop)
	    echo -en "Stoping FireWallServer:\t\t"
        #$wkdir/sbin/start-stop-daemon --stop -p /tmp/firewall.pid >/dev/null 2>&1
        for tab in $(echo "mangle filter nat raw") ;do
	    #echo $tab
	    if [ "$tab"="filter" ];then
               $iptables -t filter -P INPUT ACCEPT > /dev/null 2>&1
               $iptables -t filter -P OUTPUT ACCEPT > /dev/null 2>&1
               $iptables -t filter -P FORWARD ACCEPT > /dev/null 2>&1
            fi
            $iptables -t $tab -F > /dev/null 2>&1
            $iptables -X > /dev/null 2>&1
        done
	ipset_stop
	RETVAL=$?
        #echo
        if [ $RETVAL -eq 0 ] ;then
           echo "Done..."
	    else
           echo "Failed"
	    fi
        ;;
  status)
        for pid in  $( ps ax|grep iptables |grep -v 'grep'|awk '{print $1}');do
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
