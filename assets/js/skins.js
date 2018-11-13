/*Note: if you want to draw charts and sparkline with Theme Colors you must place skins.js in your page before beyond.js*/
/*Do not use JQuery if you intend to use this file in Head element*/


//Handle Skins
if (readCookie("current-skin")) {
    var a = document.createElement('link');
    a.href = readCookie("current-skin");
    a.rel = "stylesheet";
    document.getElementsByTagName("head")[0].appendChild(a);
}

//Handle RTL SUpport
//Checks Not to Do rtl-support for Arabic and Persian Demo Pages
if (location.pathname != "/index-rtl-fa.html" && location.pathname != "/index-rtl-ar.html") {
    if (readCookie("rtl-support")) {
        if (document.getElementById("beyond-link") != null)
            document.getElementById("beyond-link").setAttribute("href", "assets/css/beyond-rtl.min.css");
        if (document.getElementById("bootstrap-rtl-link") != null)
            document.getElementById("bootstrap-rtl-link").setAttribute("href", "assets/css/bootstrap-rtl.min.css");
        //Resolve 4095 Issue With IE<=9
        if (getInternetExplorerVersion() <= 9 && getInternetExplorerVersion() > 0) {
            var a = document.createElement('link');
            a.href = "assets/css/4095-rtl.min.css";
            a.rel = "stylesheet";
            document.getElementsByTagName("head")[0].appendChild(a);
        }
    }
    else {
        if (document.getElementById("beyond-link") != null)
            document.getElementById("beyond-link").setAttribute("href", "assets/css/beyond.min.css");
        if (document.getElementById("bootstrap-rtl-link") != null)
            document.getElementById("bootstrap-rtl-link").setAttribute("href", "");
        //Resolve 4095 Issue With IE<=9
        if (getInternetExplorerVersion() <= 9 && getInternetExplorerVersion() > 0) {
            var a = document.createElement('link');
            a.href = "assets/css/4095.min.css";
            a.rel = "stylesheet";
            document.getElementsByTagName("head")[0].appendChild(a);
        }
    }
}

//Create Cookie Function
function createCookie(name, value, days) {
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        var expires = "; expires=" + date.toGMTString();
    }
    else var expires = "";
    document.cookie = name + "=" + value + expires + "; path=/";
}

//Read Cookie Function
function readCookie(name) {
    var nameEq = name + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEq) == 0) return c.substring(nameEq.length, c.length);
    }
    return null;
}

//Erase Cookie Function
function eraseCookie(name) {
    createCookie(name, "", -1);
}

//Get Internet Explorer Version
function getInternetExplorerVersion() {
    var rv = -1;
    if (navigator.appName == "Microsoft Internet Explorer") {
        var ua = navigator.userAgent;
        var re = new RegExp("MSIE ([0-9]{1,}[.0-9]{0,})");
        if (re.exec(ua) != null) {
            rv = parseFloat(RegExp.$1);
        }
    }
    return rv;
}
