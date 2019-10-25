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
true > /etc/ppp/chap-secrets
true > /etc/ppp/pap-secrets
for servID in $(awk -F= '/^netiface_[0-9]/{print $1}' $iconf/netiface.conf);do
    toDict $iconf/netiface.conf $servID
    # 加载接口信息
    ip link set ${uDict["ifacename"]} up >/dev/null 2>&1
    ip addr flush dev ${uDict["ifacename"]} >/dev/null 2>&1
    # 处理Static IP信息
    if [ "${uDict["ifacetype"]}" = "STATIC" ];then
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
    # 处理ADSL线路信息
    elif [ "${uDict["ifacetype"]}" = "ADSL" ];then
      echo -en "\"${uDict["username"]}\"\t*\t\"${uDict["password"]}\"\t*\n" >> /etc/ppp/chap-secrets
      echo -en "\"${uDict["username"]}\"\t*\t\"${uDict["password"]}\"\t*\n" >> /etc/ppp/pap-secrets
      chmod 600 /etc/ppp/pap-secrets /etc/ppp/chap-secrets >/dev/null 2>&1 &
      if [ "${uDict["defaultgw"]}" = "0" ];then
         defgw=no
      else
         defgw=yes
      fi
      echo -en "BOOTPROTO=dialup\nCONNECT_POLL=6\nCONNECT_TIMEOUT=0\nDEMAND=no\nFIREWALL=NONE\nLCP_FAILURE=3\nLCP_INTERVAL=15\nPPPOE_TIMEOUT=80\nPIDFILE=/tmp/xdsl-ppp${uDict["id"]}.pid\nUNIT=${uDict["id"]}\nUSERCTL=yes\nETH=${uDict["ifacename"]}\nCLAMPMSS=${uDict["mtu"]}\nUSER=${uDict["username"]}\nDEFROUTE=$defgw\n" > /tmp/xdsl_${uDict["id"]}.cf      
      LineStatus=$(python $wkdir/tools/API.py API getnistatus ${uDict["ifacename"]})
      Pscount=$(ps -ef|grep "xdsl_${uDict["id"]}.cf"|grep -v 'grep'|wc -l)
      /sbin/pppoe-status /tmp/xdsl_${uDict["id"]}.cf >/dev/null 
      if [ $? != 0 ] && [ "$LineStatus" == "UP" ] && [ "$Pscount" == "0" ];then
         /sbin/pppoe-connect /tmp/xdsl_${uDict["id"]}.cf >/dev/null 2>&1 &
      fi
      # reload ppp script
      chkup=$(grep 'AdvRouteAPI.sh' /etc/ppp/ip-up)
      chkdown=$(grep 'AdvRouteAPI.sh' /etc/ppp/ip-down)
      if [ x"$chkup" = x"" ] || [ x"$chkdown" = x"" ];then
         sed -i "s:exit .*:$wkdir/sbin/AdvRouteAPI.sh\nexit 0:g" /etc/ppp/ip-up >/dev/null 2>&1
         sed -i "s:exit .*:$wkdir/sbin/AdvRouteAPI.sh\nexit 0:g" /etc/ppp/ip-down >/dev/null 2>&1
      fi
    fi

    # 处理扩展IP
    for line in $(echo ${uDict["extip"]}|sed 's/;/ /g');do
      if [ "$line" != "" ];then
         extipinfos=$(echo $line|awk -F/ '{print $1"/"$2}')
         ip addr add local $extipinfos dev ${uDict["ifacename"]} label ${uDict["ifacename"]}:${uDict["id"]} >/dev/null 2>&1
         extgwinfos=$(echo $line|awk -F/ '{print $3}')
         if [ ${extgwinfos} != "" ];then
            ip route flush table ${uDict["id"]} >/dev/null 2>&1
            ip route replace default via ${uDict["gateway"]} dev ${uDict["ifacename"]} src ${uDict["ipaddr"]} proto static table ${uDict["id"]} >/dev/null 2>&1
            ip route append prohibit default table ${uDict["id"]} metric 1 proto static >/dev/null 2>&1
         fi
      fi
    done

    #普通路由模式修改为高级路由模式
    ip rule del prio 50 table main >/dev/null 2>&1
    ip rule add prio 50 table main >/dev/null 2>&1
    # 增加静态接口路由(不包含动态IP,动态IP接口路由加载高级路由脚本)
    ifacezone=$(python $wkdir/tools/API.py API getnizone ${uDict["ifacename"]})
    if [ "${uDict["gateway"]}" != "" ] && [ "$ifacezone" != "LAN" ];then  #这个地方必须是WAN模式才增加进出路由
      #echo ${uDict["ipaddr"]}/${uDict["netmask"]}
      ip rule del prio $inum >/dev/null 2>&1
      ip rule add prio $inum from ${uDict["ipaddr"]}/${uDict["netmask"]} table ${uDict["id"]} >/dev/null 2>&1 
      let inum+=1
    fi
done
#加载VPN接口
if [ "$(python tools/API.py API getniaddr tun1000)" != "False" ];then
   ifaceaddr=$(python tools/API.py API getniaddr tun1000)
   ip rule del prio 79 >/dev/null 2>&1
   ip rule add prio 79 from $ifaceaddr table 1000 >/dev/null 2>&1
fi

#引入高级路由加载
$wkdir/sbin/AdvRouteAPI.sh >/dev/null 2>&1

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
