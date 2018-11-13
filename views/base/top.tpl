<style type="text/css">
.lnmosicon{
    background:url(/assets/img/login/logo.24x24.png) center no-repeat;
    display:block;
    vertical-align:middle;
    text-align:center;
    //margin-top:10px;
    width:100%;
    height:100%;
    }
</style>
<div class="navbar-inner">
    <div class="navbar-container">
        <!-- Navbar Barnd -->
        <div class="navbar-header pull-left">
            <a href="#" class="navbar-brand">
                <h4>{{session.get('sitename','')}}</h4>
            </a>
        </div>
        <!-- /Navbar Barnd -->
        <!-- Sidebar Collapse -->
        <div class="sidebar-collapse" id="sidebar-collapse">
            <i class="collapse-icon fa fa-bars"></i>
        </div>
        <!-- /Sidebar Collapse -->
        <!-- Account Area and Settings -->
        <div class="navbar-header pull-right">
            <div class="navbar-account">
		 <ul class="account-area">
            <li>
               <a class="login-area dropdown-toggle" title="Lnm工作室" href="https://blog.lnmos.com" target="_bank">
                 <i class='lnmosicon'></i>
               </a>
            </li>
		    %if session.get('access','') == 1 and session.get('errnum') > 0:
                    <li>
                        <a class="login-area dropdown-toggle" title="环境检测" href="/syscheck">
                            <i class="icon fa fa-warning"></i>
			                <span class="badge">{{session.get('errnum')}}</span>
                        </a>
                    </li>
		    %end
                    <!--li>
                        <a class="login-area wave in dropdown-toggle" data-toggle="dropdown" title="信息" href="#">
                            <i class="icon fa fa-envelope"></i>
                            <span class="badge">0</span>
                        </a>

                    </li-->

                    <!-- /Account Area -->
		            <li>
                        <a class="login-area dropdown-toggle" title="修改密码" href="/changepasswd">
                            <i class="icon fa fa-unlock-alt"></i>
                        </a>
                    </li>

                    <li>
                        <a class="dropdown-toggle login-area" data-toggle="dropdown" title="个人设置">
	            		<i class="icon glyphicon glyphicon-cog"></i>
                            <!--div class="avatar" title="个人设置"-->
				            <!--i class="icon glyphicon glyphicon-cog"></i-->
                            <!--img src="/assets/img/avatars/adam-jansen.jpg">
                            </div-->
                            <!--section>
                                <h2><span class="profile"><span>个人设置</span></span></h2>
                            </section-->
                        </a>
                        <!--Login Area Dropdown-->
                        <ul class="pull-right dropdown-menu dropdown-arrow dropdown-login-area">

                            <li class="email"><a>帐号: {{session.get('username',None)}}</a></li>
                            <!--Avatar Area-->
                            <!--li>
                                <div class="avatar-area">
                                    <img src="/assets/img/avatars/adam-jansen.jpg" class="avatar">
                                    <span class="caption">修改头像</span>
                                </div>
                            </li-->
			                <!--li>
                                <div>
                                    <span style= "text-align:center;" >修改密码</span>
                                </div>
                            </li-->

                            <!--Theme Selector Area-->
                            <li class="theme-area">
                                <ul class="colorpicker" id="skin-changer">
                                    <li><a class="colorpick-btn" href="#" style="background-color:#53a93f;" rel="/assets/css/skins/green.min.css"></a></li>
                                    <li><a class="colorpick-btn" href="#" style="background-color:#5DB2FF;" rel="/assets/css/skins/blue.min.css"></a></li>
                                    <li><a class="colorpick-btn" href="#" style="background-color:#2dc3e8;" rel="/assets/css/skins/azure.min.css"></a></li>
                                    <li><a class="colorpick-btn" href="#" style="background-color:#03B3B2;" rel="/assets/css/skins/teal.min.css"></a></li>
                                    <li><a class="colorpick-btn" href="#" style="background-color:#FF8F32;" rel="/assets/css/skins/orange.min.css"></a></li>
                                    <li><a class="colorpick-btn" href="#" style="background-color:#cc324b;" rel="/assets/css/skins/pink.min.css"></a></li>
                                    <li><a class="colorpick-btn" href="#" style="background-color:#AC193D;" rel="/assets/css/skins/darkred.min.css"></a></li>
                                    <li><a class="colorpick-btn" href="#" style="background-color:#8C0095;" rel="/assets/css/skins/purple.min.css"></a></li>
                                    <li><a class="colorpick-btn" href="#" style="background-color:#0072C6;" rel="/assets/css/skins/darkblue.min.css"></a></li>
                                    <li><a class="colorpick-btn" href="#" style="background-color:#585858;" rel="/assets/css/skins/gray.min.css"></a></li>
                                    <li><a class="colorpick-btn" href="#" style="background-color:#474544;" rel="/assets/css/skins/black.min.css"></a></li>
                                    <li><a class="colorpick-btn" href="#" style="background-color:#001940;" rel="/assets/css/skins/deepblue.min.css"></a></li>
                                </ul>
                            </li>
                            <!--/Theme Selector Area-->
                            <li class="dropdown-footer">
                                <a href="/logout">
                                    退出登陆
                                </a>
                            </li>
                        </ul>
                        <!--/Login Area Dropdown-->
                    </li>
		    
		            <!--li>
                        <a class="login-area dropdown-toggle" href="/backupset">
                            <div class="avatar" title="数据恢复">
                                <i class="icon fa fa-th-list" aria-hidden="true"></i>
                            </div>
                        </a>
                    </li-->
		    
                    <li>
                        <a class="login-area dropdown-toggle" data-toggle="dropdown">
                            <div class="avatar" title="项目支持">
				            <i class="icon glyphicon glyphicon-qrcode"></i>
                            </div>
                        </a>
                        <!--Login Area Dropdown-->
                        <ul class="pull-right dropdown-menu dropdown-arrow dropdown-login-area">

                            <li>
                                <div class="avatar-area">
                                    <img src="{{session.get('PayInfo','')}}" class="avatar">
                                </div>
				                <span class="caption">&emsp;扫码捐赠&emsp;</span>
                            </li>
                        </ul>
                        <!--/Login Area Dropdown-->
                    </li>

		            <!--li>
                        <a class="login-area dropdown-toggle" href="https://github.com/fxtxkktv/ocserv_centos6" target="_bank">
                            <div class="avatar" title="项目信息">
				            <i class="icon fa fa-id-card-o" aria-hidden="true"></i>
                            </div>
                        </a>
                    </li-->
                    <!--Note: notice that setting div must start right after account area list.
                    no space must be between these elements-->
                    <!-- Settings -->
	    </ul>	
            </div>
        </div>
        <!-- /Account Area and Settings -->
    </div>
</div>
