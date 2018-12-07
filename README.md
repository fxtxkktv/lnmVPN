# 该项目应用于企业远程维护、应用访问、安全连接、路由跳转
# 还有惊喜功能哦 ！！！
### 客户端下载：https://pan.baidu.com/s/1xDAfspJdBEm9ilipT61PbQ 分享密码:vzfn

## 安装步骤(仅针对centos/redhat发行版,其他版本自行测试)

1. 安装初始化环境 python >=2.7 (推荐lnmos定制版本,可以在"客户端下载"中获取) <br>
rpm -i python27-2.7.15-lnmos.rpm <br>
export PATH=$PATH:/usr/local/python27/bin <br>
安装pip工具 <br>
wget https://bootstrap.pypa.io/get-pip.py <br>
python27 get-pip.py <br>
安装virtualenv组件[使程序运行环境和系统环境分离] <br>
pip install virtualenv <br> 
virtualenv -p /usr/local/python27/bin/python --no-site-packages venv <br>
进入virtualenv环境 <br>
source venv/bin/activate <br>

2. 安装程序运行模块 <br>
MySQL服务 <br>
yum install -y gcc mysql-server mysql-devel MySQL-python <br>
证书组件 <br>
yum install -y gnutls-utils <br>
VPN服务: [yum需要调用第三方源] <br>
yum install -y epel-release <br>
yum install -y ocserv openconnect <br>
安装Python程序扩展包 <br>
pip install -r readme/requirements.txt <br>

3. 创建数据库并恢复数据模版 <br>
[创建数据库]: # mysql -u root -p -e "create database vpndb" <br>
[恢复数据模版]: # mysql -u root -p vpndb < readme/xxxxxx_Init.sql <br>
[配置数据库连接及其他]: # vim config/config.ini <br>

4. 正式运行程序 <br>
[程序调试]：python27 main.py <br>
[后台运行]: startweb.sh restart <br>
[前段访问]：https://IP地址:端口号 认用户名：admin 密码: admin<br>

备注：程序启动将自动接管网络接口配置、DNS服务、DHCP服务等相关，建议关闭系统中涉及到的相关程序，以免相互冲突。<br>

如有问题可直接反馈或邮件master@lnmos.com <br>

## 项目截图
### 系统管理
![其余界面](https://github.com/fxtxkktv/lnmVPN/blob/master/readme/systeminfo.jpg)
### 网络配置
![其余界面](https://github.com/fxtxkktv/lnmVPN/blob/master/readme/networks.jpg)
### UTM防护
![其余界面](https://github.com/fxtxkktv/lnmVPN/blob/master/readme/utm.jpg)
### VPN配置
![其余界面](https://github.com/fxtxkktv/lnmVPN/blob/master/readme/vpnserv.jpg)
### 日志审计
![其余界面](https://github.com/fxtxkktv/lnmVPN/blob/master/readme/logaudit.jpg)
### 帮助文档
![其余界面](https://github.com/fxtxkktv/lnmVPN/blob/master/readme/help.jpg)
### 支持捐赠
![其余界面](https://github.com/fxtxkktv/lnmVPN/blob/master/readme/pay.jpg)
