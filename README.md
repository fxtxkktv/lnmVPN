## 该项目应用于企业远程维护、应用访问、安全连接、GFW路由跳转
### 1.支持Android、IOS、MAC、Windows、Linux各类客户端拨入
### 2.支持不用用户不同的访问策略[速度、路由、网络地址、DNS解析]
### 3.支持用户在线下载客户端资源及用户配置说明
### 4.支持通过VPN帐号路由共享过墙，供企业内部学术研究
### 5.支持策略多线路由及域名跟踪解析路由（IPROUTE+DNSMASQ+IPSET+IPTABLES）
### 6.支持PPP、DNS、DHCP、NAT、UTM防护等功能

## 安装步骤(仅针对centos/redhat发行版,其他版本自行测试)

1. 安装lnmOS环境,从[fxtxkktv.github.io](https://raw.githubusercontent.com/fxtxkktv/fxtxkktv.github.io/master/files/Install_LnmOS_env.sh)获取简化安装Shell脚本<br>
wget https://raw.githubusercontent.com/fxtxkktv/fxtxkktv.github.io/master/files/Install_LnmOS_env.sh <br>
运行脚本<br> 
chmod +x ./Install_LnmOS_env.sh && ./Install_LnmOS_env.sh <br>

2. 获取程序代码 <br>
git clone https://github.com/fxtxkktv/lnmVPN.git <br>
进入程序目录 <br>
cd lnmVPN <br>
创建程序独立运行Python环境 <br>
virtualenv -p /opt/Py27lnmos/bin/python --no-site-packages venv <br>
进入virtualenv环境 <br>
source venv/bin/activate <br>

2. 安装程序运行模块 <br>
安装lnmVPN相关服务组件 <br>
yum install -y gnutls-utils ocserv openconnect iptables ipset dnsmasq iftop<br>
安装Python程序扩展包 <br>
pip install -r readme/requirements.txt <br>

3. 创建数据库并恢复数据模版 <br>
[创建数据库]: # mysql -u root -p -e "create database vpndb" <br>
[恢复数据模版]: # mysql -u root -p vpndb < readme/db_schema.sql <br>
[配置数据库连接及其他]: # vim config/config.ini <br>

4. 正式运行程序 <br>
[程序调试]：python27 main.py <br>
[后台运行]: startweb.sh restart <br>
[前段访问]：https://IP地址:888[端口号] 用户名：admin 密码: admin<br>
[修改safekey]: 首次使用建议修改passkey，可通过API接口重置管理员密码[python tools/API.py API resetAdminPass newpass]<br>

备注：程序启动将自动接管网络接口配置、DNS服务、DHCP服务等相关，建议关闭系统中涉及到的相关程序，以免相互冲突。<br>

如有问题可直接反馈或邮件master@lnmos.com <br>

## 项目截图
### 系统管理
![其余界面](https://github.com/fxtxkktv/lnmVPN/blob/master/readme/systeminfo.png)
### 网络配置
![其余界面](https://github.com/fxtxkktv/lnmVPN/blob/master/readme/network.png)
### DNS配置
![其余界面](https://github.com/fxtxkktv/lnmVPN/blob/master/readme/dnsconf.png)
### UTM防护
![其余界面](https://github.com/fxtxkktv/lnmVPN/blob/master/readme/utmconf.png)
### VPN配置
![其余界面](https://github.com/fxtxkktv/lnmVPN/blob/master/readme/vpnserver.png)
### 策略配置
![其余界面](https://github.com/fxtxkktv/lnmVPN/blob/master/readme/vpnpolicy.png)
### 日志审计
![其余界面](https://github.com/fxtxkktv/lnmVPN/blob/master/readme/logaudit.png)
### 帮助文档
![其余界面](https://github.com/fxtxkktv/lnmVPN/blob/master/readme/helpinfo.png)
### 支持捐赠
![其余界面](https://github.com/fxtxkktv/lnmVPN/blob/master/readme/pay.jpg)
