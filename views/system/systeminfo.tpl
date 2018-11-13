%rebase base position='欢迎主页', managetopli="system"
<link href="/assets/css/charisma-app.css" rel="stylesheet" type="text/css" />
<div class="page-body">
    <div class="row">
        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">
            <div class="widget" style="background: #fff;">
                <div class="widget-header bordered-bottom bordered-themesecondary">
                    <i class="widget-icon fa fa-tags themesecondary"></i>
                    <span class="widget-caption themesecondary">控制台</span>
                    <div class="widget-buttons">
                        <a href="#" data-toggle="maximize"><i class="fa fa-expand"></i></a>
                        <a href="#" data-toggle="collapse"><i class="fa fa-minus"></i></a>
                        <a href="#" data-toggle="dispose"><i class="fa fa-times"></i></a>
                    </div>
                </div><!--Widget Header-->
   <div class="row">
    <div class="box col-md-6">
        <div class="box-inner widget" style="background: #fff;">
            <div class="box-header well" data-original-title>
                <i class="glyphicon glyphicon-list-alt widget-icon"></i>
		<span class="widget-caption themesecondary">系统信息</span>
		<!--a href="/systeminfomore" style="float:right;" ><i class="fa fa-sliders"></i></a-->
            </div>
	
            <div class="box-content">
		<div style="display: block;">
                    <table class="table">
                        <tbody>
                        <tr>
                            <td>主机名称:</td>
                            <td class="center">{{info.get('hostname','')}}</td>
                        </tr>
                        <tr>
                            <td>平台信息:</td>
                            <td class="center">{{info.get('kernel','')}}</td>
                        </tr>
                        <tr>
                            <td>网络信息:</td>
                            <td class="center">{{info.get('v4addr','')}}</td>
                        </tr>
                        <tr>
                            <td>运行时长:</td>
                            <td class="center">{{info.get('runtime','')}}</td>
                        </tr>
                        <tr>
                            <td>Python版本:</td>
                            <td class="center">{{info.get('pyversion','')}}</td>
                        </tr>
			<tr>
                            <td>CPU型号:</td>
                            <td class="center">{{info.get('cpumode','')}}</td>
                        </tr>
			<tr>
                            <td>MEM容量:</td>
                            <td class="center">{{info.get('memsize','')}}</td>
                        </tr>
			<tr>
                            <td>APP版本:</td>
			    <td class="center">{{info.get('appversion','')}}</td>
                        </tr>
                        </tbody>
                    </table>
                </div>
        </div>
      </div>
   </div>

   <div class="box col-md-6">
        <div class="box-inner widget" style="background: #fff;">
            <div class="box-header well" data-original-title="">
                <i class="glyphicon glyphicon-list-alt widget-icon"></i>
                <span class="widget-caption themesecondary">管理日志</span>
		<a href="/applog" style="float:right;" ><i class="fa fa-sliders"></i></a>
            </div>
            <div class="box-content">
		<div style="display: block;">
                    <table class="table">
                        <tbody>
			<tr>
                        <td>用户</td>
                        <td class="center">操作信息</td>
                        <td class="center">远程主机</td>
                        <td class="center">操作时间</td>
			</tr>
			%for log in logdict:
			<tr>
			<td>{{log.get('objtext','')}}</td>
			<td class="center">{{log.get('objact','')}}</td>
			<td class="center">{{log.get('objhost','')}}</td>
			<td class="center">{{log.get('objtime','')}}</td>		
			</tr>
                        %end
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
   </div>
   <!--div class="box col-md-12">
        <div class="box-inner widget" style="background: #fff;height: 330px;">
            <div class="box-header well" style="margin-top: 0px;margin-left: 0px;" data-original-title="">
                <i class="glyphicon glyphicon-list-alt widget-icon"></i>
                <span class="widget-caption themesecondary">系统活动</span>
            </div>
            <div id="echartsLine1" class="box-content" style="width: 32%;height: 300px;float: left;margin-top: 0px;margin-left: 10px;"></div>
	    <div id="echartsLine2" class="box-content" style="width: 32%;height: 300px;float: left;margin-top: 0px;margin-left: 10px;"></div>
	    <div id="echartsLine3" class="box-content" style="width: 32%;height: 300px;float: left;margin-top: 0px;margin-left: 10px;"></div>
        </div>
   </div-->
   <div class="box col-md-4">
        <div class="box-inner widget" style="background: #fff; height: 300px;">
            <div class="box-header well" data-original-title="">
                <i class="glyphicon glyphicon-list-alt widget-icon"></i>
                <span class="widget-caption themesecondary">CPU负载</span>
		<!--a href="/systeminfomore" style="float:right;" ><i class="fa fa-sliders"></i></a-->
	    <div id="echartsLine1" class="box-content" style="width: 100%;height: 270px;float: left;margin-top: 0px;margin-left: 3px;"></div>
	    </div>
        </div>
   </div>
   <div class="box col-md-4">
        <div class="box-inner widget" style="background: #fff; height: 300px;">
            <div class="box-header well" data-original-title="">
                <i class="glyphicon glyphicon-list-alt widget-icon"></i>
                <span class="widget-caption themesecondary">内存使用率</span>
		<!--a href="/systeminfomore" style="float:right;" ><i class="fa fa-sliders"></i></a-->
	    <div id="echartsLine2" class="box-content" style="width: 100%;height: 270px;float: left;margin-top: 0px;margin-left: 3px;"></div>
	    </div>
	</div>
   </div>
   <div class="box col-md-4">
        <div class="box-inner widget" style="background: #fff;height: 300px;">
            <div class="box-header well" data-original-title="">
                <i class="glyphicon glyphicon-list-alt widget-icon"></i>
                <span class="widget-caption themesecondary">网络IO</span>
		<!--a href="/systeminfomore" style="float:right;" ><i class="fa fa-sliders"></i></a-->
            <div id="echartsLine3" class="box-content" style="width: 100%;height: 270px;float: left;margin-top: 0px;margin-left: 3px;"></div>
	    </div>
        </div>
   </div>
  </div-->
</div>

<script src="https://cdn.staticfile.org/echarts/4.2.0-rc.1/echarts.js"></script>
<script type="text/javascript">
    var cpu = {
        'used': [],
        'free': [],
        time: []
    };
    var memory = {
        'used': [],
        'free': [],
        time: []
    };
    var net = {
        'rcvd': [],
        'send': [],
        time: []
    };
    $.ajax({
        type: 'POST',
        dataType: 'html',
        url: '/systeminfo',
        success: function (data) {
            var result = jQuery.parseJSON(data)
            if (result.resultCode == '1') {
                alert(result.result);
                return 0
            };
            $.each(result.result[1], function (i, item) {
                cpu.time.push(item[1]);
                net.time.push(item[1]);
                memory.time.push(item[1]);

                itemJson = jQuery.parseJSON(item[0])
                cpu.used.push(itemJson.cpu.cpuUsed);

                memory.used.push(itemJson.memory.memoryUsed);

                net.rcvd.push(itemJson.net.rcvd);
                net.send.push(itemJson.net.send);
            });
            createEcharts();
        }
    });

    function creatNetEcharts() {
        option = {
            /*title: {
                text: '网络IO'
            },*/
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    type: 'cross',
                    label: {
                        backgroundColor: '#6a7985'
                    }
                },
            },
            legend: {
                data: ['发送', '下载']
            },

            xAxis: [{
                type: 'category',
                boundaryGap: false,
                data: net.time
            }],
            yAxis: [{
                type: 'value'
            }],
            series: [{
                    name: '发送',
                    type: 'line',
                    areaStyle: {},
                    data: net.send
                }, {
                    name: '下载',
                    type: 'line',
                    areaStyle: {},
                    data: net.rcvd
                },

            ],
            backgroundColor: '#FFFFFF',
            color: ['#BE81F7', '#C8FE2E'],
            dataZoom: [{
                start: 85,
                end: 100,
                type: 'inside'
            }, {
                handleIcon: 'M10.7,11.9v-1.3H9.3v1.3c-4.9,0.3-8.8,4.4-8.8,9.4c0,5,3.9,9.1,8.8,9.4v1.3h1.3v-1.3c4.9-0.3,8.8-4.4,8.8-9.4C19.5,16.3,15.6,12.2,10.7,11.9z M13.3,24.4H6.7V23h6.6V24.4z M13.3,19.6H6.7v-1.4h6.6V19.6z',
            }],
        };　　
        echartsLineFunc = echarts.init(echartsLine3);
        echartsLineFunc.setOption(option);
    };

    function creatCPUEcharts() {
        option = {
            /*title: {
                text: 'CPU使用记录'
            },*/
                    

            tooltip: {
                trigger: 'axis',
                formatter: "{b}<br/>{a}:{c}%",
                axisPointer: {
                    type: 'cross',
                    label: {
                        backgroundColor: '#6a7985'
                    }
                }
            },
            xAxis: [{
                type: 'category',
                boundaryGap: false,
                data: cpu.time
            }],
            yAxis: [{
                type: 'value'
            }],
            series: [{
                name: 'CPU已用',
                type: 'line',
                data: cpu.used
            }],
            color: '#FE2EC8',
            backgroundColor: '#FFFFFF',
            dataZoom: [{
                start: 85,
                end: 100,
                type: 'inside'
            }, {
                handleIcon: 'M10.7,11.9v-1.3H9.3v1.3c-4.9,0.3-8.8,4.4-8.8,9.4c0,5,3.9,9.1,8.8,9.4v1.3h1.3v-1.3c4.9-0.3,8.8-4.4,8.8-9.4C19.5,16.3,15.6,12.2,10.7,11.9z M13.3,24.4H6.7V23h6.6V24.4z M13.3,19.6H6.7v-1.4h6.6V19.6z',
            }],
        };　　
        echartsLineFunc = echarts.init(echartsLine1);
        echartsLineFunc.setOption(option);
    };

    function creatMemoryEcharts() {
        option = {
            /*title: {
                text: '内存使用记录'
            },*/
            tooltip: {
                trigger: 'axis',
                formatter: "{b}<br/>{a}:{c}%",
                axisPointer: {
                    type: 'cross',
                    label: {
                        backgroundColor: '#6a7985'
                    }
                }
            },
            xAxis: [{
                type: 'category',
                boundaryGap: false,
                data: memory.time
            }],
            yAxis: [{
                type: 'value'
            }],
            series: [{
                    name: '内存已用',
                    type: 'line',
                    data: memory.used
                },

            ],
            color: '#00FF00',
            backgroundColor: '#FFFFFF',
            dataZoom: [{
                start: 85,
                end: 100,
                type: 'inside',
            }, {
                handleIcon: 'M10.7,11.9v-1.3H9.3v1.3c-4.9,0.3-8.8,4.4-8.8,9.4c0,5,3.9,9.1,8.8,9.4v1.3h1.3v-1.3c4.9-0.3,8.8-4.4,8.8-9.4C19.5,16.3,15.6,12.2,10.7,11.9z M13.3,24.4H6.7V23h6.6V24.4z M13.3,19.6H6.7v-1.4h6.6V19.6z',
            }],

        };　　
        echartsLineFunc = echarts.init(echartsLine2);
        echartsLineFunc.setOption(option);
    };

    function createEcharts() {
        creatNetEcharts();
        creatCPUEcharts();
        creatMemoryEcharts();
    };
</script>
