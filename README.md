# 该项目应用于企业远程维护、应用访问、安全连接、GFW路由跳转
### 1.支持Android、IOS、MAC、Windows、Linux各类客户端拨入
### 2.支持不用用户不同的访问策略控制
### 2.支持策略用户指定分配特定网络地址，防止端对端网络地址冲突
### 3.支持基于不同的用户策略组进行VPN连接限速
### 4.支持用户在线下载客户端资源及用户配置说明
### 5.支持通过VPN帐号自动翻墙并共享路由，供企业内部学术研究
### 6.支持DNS全局代理及防污染控制
### 客户端下载：https://pan.baidu.com/s/1xDAfspJdBEm9ilipT61PbQ 分享密码:vzfn

## 安装步骤(仅针对centos/redhat发行版,其他版本自行测试)

1. 安装初始化环境 python >=2.7 (推荐lnmos定制版本,可以在"客户端下载"中获取) <br>
rpm -i Py27lnmos-2.7.15-6.el6.rpm <br>
安装pip工具 <br>
wget https://bootstrap.pypa.io/get-pip.py <br>
/opt/Py27lnmos/bin/python27 get-pip.py <br>
安装virtualenv组件[使程序运行环境和系统环境分离] <br>
/opt/Py27lnmos/bin/pip install virtualenv <br> 
获取程序代码 <br>
git clone https://github.com/fxtxkktv/lnmVPN.git <br>
进入程序目录 <br>
cd lnmVPN <br>
创建程序虚拟环境 <br>
virtualenv -p /opt/Py27lnmos/bin/python --no-site-packages venv <br>
进入virtualenv环境 <br>
source venv/bin/activate <br>

2. 安装程序运行模块 <br>
MySQL服务 <br>
yum install -y gcc mysql-server mysql-devel MySQL-python <br>
证书组件 <br>
yum install -y gnutls-utils <br>
VPN服务: [yum需要调用第三方源] <br>
yum install -y epel-release <br>
yum install -y ocserv openconnect iptables ipset dnsmasq<br>
安装Python程序扩展包 <br>
pip install -r readme/requirements.txt <br>

3. 创建数据库并恢复数据模版 <br>
[创建数据库]: # mysql -u root -p -e "create database vpndb" <br>
[恢复数据模版]: # mysql -u root -p vpndb < readme/xxxxxx_Init.sql <br>
[配置数据库连接及其他]: # vim config/config.ini <br>

4. 正式运行程序 <br>
[程序调试]：python27 main.py <br>
[后台运行]: startweb.sh restart <br>
[前段访问]：https://IP地址:端口号 用户名：admin 密码: admin<br>
[修改safekey]: 首次使用建议修改passkey，可通过API接口重置管理员密码[python tools/API.py API resetAdminPass newpass]<br>

备注：程序启动将自动接管网络接口配置、DNS服务、DHCP服务等相关，建议关闭系统中涉及到的相关程序，以免相互冲突。<br>

如有问题可直接反馈或邮件master@lnmos.com <br>

## 项目截图
### 系统管理
![其余界面](https://github.com/fxtxkktv/lnmVPN/blob/master/readme/systeminfo.jpg)
### 网络配置
![其余界面](https://github.com/fxtxkktv/lnmVPN/blob/master/readme/networks.jpg)
### DNS配置
![其余界面](https://github.com/fxtxkktv/lnmVPN/blob/master/readme/dns.jpg)
### UTM防护
![其余界面](https://github.com/fxtxkktv/lnmVPN/blob/master/readme/utm.jpg)
### VPN配置
![其余界面](https://github.com/fxtxkktv/lnmVPN/blob/master/readme/vpnserv.jpg)
### 证书管理
![其余界面](https://github.com/fxtxkktv/lnmVPN/blob/master/readme/certs.jpg)
### 策略配置
![其余界面](https://github.com/fxtxkktv/lnmVPN/blob/master/readme/policys.jpg)
### 日志审计
![其余界面](https://github.com/fxtxkktv/lnmVPN/blob/master/readme/logaudit.jpg)
### 帮助文档
![其余界面](https://github.com/fxtxkktv/lnmVPN/blob/master/readme/help.jpg)
### 支持捐赠
![其余界面](https://github.com/fxtxkktv/lnmVPN/blob/master/readme/pay.jpg)
