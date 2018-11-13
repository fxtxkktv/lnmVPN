<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<!--Head-->
<head>
    <meta charset="utf-8" />
    <title>{{session.get('sitename','')}}</title>

    <meta name="description" content="login page" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <link rel="shortcut icon" href="/assets/img/favicon.png" type="image/x-icon">

    <!--Basic Styles-->
    <link href="/assets/css/bootstrap.min.css" rel="stylesheet" />
    <link id="bootstrap-rtl-link" href="" rel="stylesheet" />
    <link href="/assets/css/font-awesome.min.css" rel="stylesheet" />

    <!--Fonts-->
    <link href="/assets/css/google1.css" rel="stylesheet" type="text/css">

    <!--Beyond styles-->
    <link id="beyond-link" href="/assets/css/beyond.min.css" rel="stylesheet" />
    <link href="/assets/css/demo.min.css" rel="stylesheet" />
    <link href="/assets/css/animate.min.css" rel="stylesheet" />
    <link id="skin-link" href="" rel="stylesheet" type="text/css" />

    <!--Skin Script: Place this script in head to load scripts for skins and rtl support-->
    <script src="/assets/js/skins.min.js"></script>

</head>
<!--Head Ends-->
<!--Body-->
<body >
  <div class="login-bg1">
    <div class="login-bg2">
      <div class="login-container animated fadeInDown login-bg">
        <div class="loginbox bg-white">
            <div class="loginbox-title">SIGN IN</div>
            <div class="loginbox-social">
                <div class="social-title ">{{session.get('sitename','')}}</div>
		% if message:
                   <div class="loginbox-signup"><font color="red">{{message}}</font></div>
                % end
                <!--div class="social-buttons">
                    <a class="button-facebook">
                        <i class="social-icon fa fa-facebook"></i>
                    </a>
                    <a  class="button-twitter">
                        <i class="social-icon fa fa-twitter"></i>
                    </a>
                    <a  class="button-google">
                        <i class="social-icon fa fa-google-plus"></i>
                    </a>
                </div-->
            </div>
            <!--div class="loginbox-or">
                <div class="or-line"></div>
                <div class="or">OR</div>
            </div-->
            <form action="" method="post">
                <div class="loginbox-textbox">
                    <input type="text" class="form-control" name="username" onmousedown="s(event,this)" placeholder="帐号" />
                </div>
                <div class="loginbox-textbox">
                    <input type="password" class="form-control" name="passwd" placeholder="密码" />
                </div>

                <div class="loginbox-submit">
                    <input type="submit" class="btn btn-primary btn-block" value="登陆">
                </div>
            </form>
        </div>
     </div>	
    </div>
  </div>
    <!--Basic Scripts-->
    <script src="/assets/js/jquery-2.0.3.min.js"></script>
    <script src="/assets/js/bootstrap.min.js"></script>
    <script src="/assets/js/slimscroll/jquery.slimscroll.min.js"></script>

    <!--Beyond Scripts-->
    <script src="/assets/js/beyond.js"></script>

    <!--Google Analytics::Demo Only-->
    <script>
        (function (i, s, o, g, r, a, m) {
            i['GoogleAnalyticsObject'] = r; i[r] = i[r] || function () {
                (i[r].q = i[r].q || []).push(arguments)
            }, i[r].l = 1 * new Date(); a = s.createElement(o),
            m = s.getElementsByTagName(o)[0]; a.async = 1; a.src = g; m.parentNode.insertBefore(a, m)
        })(window, document, 'script', '/assets/js/google/analytics.js', 'ga');

        ga('create', 'UA-52103994-1', 'auto');
        ga('send', 'pageview');

    </script>
    <script>
	function s(e,a){
        	if ( e && e.preventDefault )
                	e.preventDefault();
        	else
                	window.event.returnValue=false;
                	a.focus();
        	}
   </script>
</body>
<!--Body Ends-->
</html>
