# 该项目作用于企业远程维护、远程应用访问、安全连接
### 客户端下载：https://pan.baidu.com/s/1xDAfspJdBEm9ilipT61PbQ

## 安装步骤(仅针对centos/redhat发行版,其他版本自行测试)

1. 安装初始化环境 python >=2.7 (推荐lnmos定制版本) <br>
rpm -i python27-2.7.15-lnmos.rpm <br>
export PATH=$PATH:/usr/local/python27/bin
安装pip工具: wget https://bootstrap.pypa.io/get-pip.py <br>
python27 get-pip.py <br>

2. 安装pip环境并安装相关python组件模块 <br>
MySQL服务: mysql-server mysql-devel MySQL-Python <br>
VPN服务: ocserv openconnect epel-release[yum第三方源] <br>
证书组件: gnutls-utils <br>
yum install gcc mysql-server mysql-devel ocserv openconnect epel-release gnutls-utils <br>
程序扩展包: pip install -r requirements.txt <br>

3. 创建数据库并恢复数据模版 <br>
[创建数据库] <br>
[恢复数据模版] <br>
[配置数据库连接] vim config/config.ini <br>

4. 正式运行程序
[程序调试]：python main.py 
[后台运行]: startweb.sh restart
[前段访问]：https://IP地址:端口号

备注：程序启动将自动接管网络接口配置、DNS服务、DHCP服务等相关，建议关闭系统中涉及到的相关程序，以免相互冲突。


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
