<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">

<head>
    <meta charset="utf-8" />
    <title>{{session.get('sitename','')}}</title>

    <meta name="description" content="{{session.get('sitename','')}}" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta http-equiv="Content-Security-Policy" content="upgrade-insecure-requests">
    <link rel="shortcut icon" href="/assets/img/favicon.png" type="image/x-icon">

    <!--Basic Styles-->
    <link href="/assets/css/bootstrap.min.css" rel="stylesheet" />
    <link href="/assets/css/bootstrap-table.css" rel="stylesheet" />

    <link id="bootstrap-rtl-link" href="" rel="stylesheet" />
    <link href="/assets/css/font-awesome.min.css" rel="stylesheet" />
    <link href="/assets/css/weather-icons.min.css" rel="stylesheet" />


    <!--Fonts
    <link href="http://fonts.useso.com/css?family=Open+Sans:300italic,400italic,600italic,700italic,400,600,700,300" rel="stylesheet" type="text/css">
    <link href='http://fonts.useso.com/css?family=Roboto:400,300' rel='stylesheet' type='text/css'>
    -->
    <!--Beyond styles-->
    <link href="/assets/css/beyond.min.css" rel="stylesheet" type="text/css"/>
    <link href="/assets/css/demo.min.css" rel="stylesheet" />
    <link href="/assets/css/typicons.min.css" rel="stylesheet" />
    <link href="/assets/css/animate.min.css" rel="stylesheet" />
    <link id="skin-link" href="" rel="stylesheet" type="text/css" />

	<!--20150610-->
	<link href="/assets/css/20150610.css" rel="stylesheet" />

    <!--Skin Script: Place this script in head to load scripts for skins and rtl support-->
    <script src="/assets/js/skins.min.js"></script>
    <script src="/assets/js/jquery-2.0.3.min.js"></script>
    <script src="/assets/js/bootstrap.min.js"></script>
    <script src="/assets/js/bootstrap-table.js"></script>
    <script src="/assets/js/slimscroll/jquery.slimscroll.min.js"></script>
    <script src="/assets/js/bootstrap-table-zh-CN.js"></script>


    <style type="text/css">
        input[type=checkbox]{
            opacity : 1;
            position: static;
        }
    </style>

</head>
<body>

    <!-- Navbar -->
    <div class="navbar">
        % include('top.tpl')
    </div>
    <!-- /Navbar -->

    <!-- Main Container -->
    <div class="main-container container-fluid">
        <div class="page-container">

          % include('menu.tpl')

            <div class="page-content">
                <!-- Page Breadcrumb -->
                <!--div class="page-breadcrumbs position-relative">
                    <ul class="breadcrumb">
                        <li>
                            <i class="fa fa-home"></i>
			    <a href="#">首页</a>	
                        </li>
                        <li class="active">欢迎页</li>
                    </ul>
                </div-->
                <!--div style="margin:30px 0px;"></div-->
                <!-- /Page Breadcrumb -->
                <!--Page Header
                <div class="page-header position-relative">
                    <div class="header-title">
                        <h1>
                            {{get('position',' ')}}
                        </h1>
                    </div>

                    <div class="header-buttons">
                        <a class="sidebar-toggler" href="#">
                            <i class="fa fa-arrows-h" title="宽屏"></i>
                        </a>
                        <a class="refresh" id="refresh-toggler" href="">
                            <i class="glyphicon glyphicon-refresh" title="刷新"></i>
                        </a>
                        <a class="fullscreen" id="fullscreen-toggler" href="#">
                            <i class="glyphicon glyphicon-fullscreen" title="全屏"></i>
                        </a>
                    </div>

                </div>
                <Page Header -->
                <!-- Page Body -->
                    %include
                <!-- /Page Body -->
            </div>
            <!-- /Page Content -->
        </div>
        <!-- /Page Container -->
        <!-- Main Container -->

    </div>
<script src="/assets/js/beyond.min.js"></script>
    <!--Beyond Scripts-->
</body>
</html>
