
<!-- Page Sidebar -->
<div class="page-sidebar" id="sidebar">
    <!-- Page Sidebar Header-->
    <!--div class="sidebar-header-wrapper">
        <input type="text" class="searchinput" />
        <i class="searchicon fa fa-search"></i>
        <div class="searchhelper">搜索</div>
    </div-->
    <!-- /Page Sidebar Header -->

    <!-- Sidebar Menu -->
    <ul class="nav sidebar-menu">
        <!--Dashboard-->
        <li>
            <a href="/project">
                <i class="menu-icon glyphicon glyphicon-home"></i>
                <span class="menu-text"> 欢迎主页 </span>
            </a>
        </li>
    %if session.get('access','') == 1 :
        %if get('managetopli','')=='system':
          <li class="active open">
        %else:
          <li class="active">
    %end
            <a href="#" class="menu-dropdown">
                <i class="menu-icon fa fa-desktop"></i>
                <span class="menu-text"> 系统配置</span>
                <i class="menu-expand"></i>
            </a>
            <ul class="submenu">
                <li class="">
                    <a href="/systeminfo">
                        <span class="menu-text">系统信息</span>
                    </a>
                </li>
                <li class="">
                  <a href="/resconfig">
                  <span class="menu-text">监控配置</span>
                  </a>
                </li>
                <li class="">
                    <a href="/administrator">
                        <span class="menu-text">管&nbsp;理&nbsp;员</span>
                    </a>
                </li>
                <li class="">
                    <a href="/backupset">
                        <span class="menu-text">数据备份</span>
                    </a>
                </li>
	     </ul>
	 </li>
	%if get('managetopli','')=='networks':
          <li class="active open">
         %else:
          <li class="active">
         %end
            <a href="#" class="menu-dropdown">
                <i class="menu-icon fa fa-tasks"></i>
                <span class="menu-text"> 网络配置</span>
                <i class="menu-expand"></i>
            </a>
            <ul class="submenu">		
		<li class="">
                    <a href="/networkconf">
                        <span class="menu-text">网络配置</span>
                    </a>
                </li>
                <li class="">
                    <a href="/routeconf">
                        <span class="menu-text">路由管理</span>
                    </a>
                </li>
		<li class="">
                    <a href="/dnsservconf">
                        <span class="menu-text">DNS服务</span>
                    </a>
                </li>
		<li class="">
                    <a href="/dhcpservconf">
                        <span class="menu-text">DHCP服务</span>
                    </a>
                </li>
        <li class="">
                    <a href="/ifdatashow">
                        <span class="menu-text">流量统计</span>
                    </a>
                </li>
		<li class="">
                    <a href="/servtools">
                        <span class="menu-text">运维工具</span>
                    </a>
                </li>
            </ul>
        </li>

	%if get('managetopli','')=='firewall':
          <li class="active open">
        %else:
          <li class="active">
        %end
	    <a href="#" class="menu-dropdown">
                <i class="menu-icon fa fa-shield"></i>
                <span class="menu-text"> UTM防护 </span>
                <i class="menu-expand"></i>
            </a>
            <ul class="submenu">
                <li class="">
                    <a href="/netobjconf">
                        <span class="menu-text">网络对象</span>
                    </a>
                </li>
                <li class="">
                    <a href="/utmruleconf">
                        <span class="menu-text">UTM规则</span>
                    </a>
                </li>
                <li class="">
                    <a href="/natruleconf">
                        <span class="menu-text">NAT规则</span>
                    </a>
                </li>
                <li class="">
                    <a href="/mapruleconf">
                        <span class="menu-text">MAP规则</span>
                    </a>
                </li>
            </ul>
        </li>

        %if get('managetopli','')=='vpnserv':
          <li class="active open">
         %else:
          <li class="active">
         %end
            <a href="#" class="menu-dropdown">
                <i class="menu-icon fa fa-globe"></i>
                <span class="menu-text"> VPN配置 </span>
                <i class="menu-expand"></i>
            </a>
            <ul class="submenu">
		<li class="">
                    <a href="/vpnservconf">
                        <span class="menu-text">服务管理</span>
                    </a>
                </li>
                <li class="">
                    <a href="/vnodemgr">
                        <span class="menu-text">节点管理</span>
                    </a>
                </li>
                <li class="">
                    <a href="/certmgr">
                        <span class="menu-text">证书管理</span>
                    </a>
                </li>
		<li class="">
                    <a href="/user">
                        <span class="menu-text">用户管理</span>
                    </a>
                </li>
                <li class="">
                    <a href="/policyconf">
                        <span class="menu-text">策略管理</span>
                    </a>
                </li>
            </ul>
        </li>
      
        %if get('managetopli','')=='auditlog':
          <li class="active open">
         %else:
          <li class="active">
         %end
            <a href="#" class="menu-dropdown">
                <i class="menu-icon fa fa-print"></i>
                <span class="menu-text"> 日志审计 </span>
                <i class="menu-expand"></i>
            </a>
            <ul class="submenu">
                <li class="">
                    <a href="/showservlog">
                        <span class="menu-text">VPN日志</span>
                    </a>
                </li>
                <li class="">
                    <a href="/applog">
                        <span class="menu-text">操作日志</span>
                    </a>
                </li>
            </ul>
        </li>
	%end

	%if get('managetopli','')=='help':
          <li class="active open">
         %else:
          <li class="active">
         %end
            <a href="#" class="menu-dropdown">
                <i class="menu-icon fa fa-tty"></i>
                <span class="menu-text"> 帮助文档 </span>
                <i class="menu-expand"></i>
            </a>
            <ul class="submenu">
                <li class="">
                    <a href="/clientdownload">
                        <span class="menu-text">文件下载</span>
                    </a>
                </li>
                <!--li class="">
                    <a href="/resolvent">
                        <span class="menu-text">常见问题</span>
                    </a>
                </li-->
		<li class="">
                    <a href="/support">
                        <span class="menu-text">问题反馈</span>
                    </a>
                </li>
            </ul>
        </li>

	<li class="active">
         %end
            <a href="https://github.com/fxtxkktv" target="_bank" class="menu-dropdown">
                <i class="menu-icon fa fa-address-book-o"></i>
                <span class="menu-text"> AboutMe </span>
                <i class="menu-expand"></i>
            </a>
	</li>
    </ul>
    <!-- /Sidebar Menu -->
</div>
<!-- /Page Sidebar -->
<!-- Page Content -->
