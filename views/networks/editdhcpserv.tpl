%rebase base position='DHCP服务配置', managetopli="networks"
<div class="page-body">
    <div class="row">
        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">
            <div class="widget">
                <div class="widget-header bordered-bottom bordered-themesecondary">
                    <i class="widget-icon fa fa-tags themesecondary"></i>
                    <span class="widget-caption themesecondary">DHCP服务配置</span>
                    <div class="widget-buttons">
                        <a href="#" data-toggle="maximize">
                            <i class="fa fa-expand"></i>
                        </a>
                        <a href="#" data-toggle="collapse">
                            <i class="fa fa-minus"></i>
                        </a>
                        <a href="#" data-toggle="dispose">
                            <i class="fa fa-times"></i>
                        </a>
                    </div>
                    
                </div><!--Widget Header-->
            <div style="padding:-10px 0px;" class="widget-body no-padding">
            <form action="" method="post">
            %if msg.get('message'):
                <span style="color:{{msg.get('color','')}};font-weight:bold;">&emsp;{{msg.get('message','')}}</span>
            %end
		    <div class="modal-body">
                        <div class="input-group">
                            <span class="input-group-addon" style="width:100px">DHCP服务开关</span>
                                <select style="width:420px" class="form-control" id="sel" name="dhcpenable">
                                <option 
                                %if info.get('dhcpenable','') == '1':
                                    selected
                                %end 
                                    value="1">开启服务
                                </option>
                                <option 
                                %if info.get('dhcpenable','') == '0':
                                    selected
                                %end 
                                    value="0">关闭服务
                                </option>
                                </select>
			                    <!--p name='dhcpstatus'>
			                        %if info.get('dhcpstatus','') == 0 :
				                        <img  src="/assets/img/run_1.gif" class="img-rounded" >
			                        %else :
				                        <img  src="/assets/img/run_0.gif" class="img-rounded" >
			                         %end
			                    </p-->
                        </div>
            </div>
		    <div class="modal-body" id='zone1'>
                      <div class="input-group">
                        <span class="input-group-addon">DHCP分配范围</span>
                        <input type="text" style="width:140px" class="form-control" id="" name="startip" placeholder="起始IP" onkeyup="this.value=this.value.replace(/[^\d.]/g,'')" onafterpaste="this.value=this.value.replace(/[^\d.]/g,'')" aria-describedby="inputGroupSuccess4Status" value="{{info.get('startip','')}}">
                        <input type="text" style="width:140px" class="form-control" id="" name="stopip" placeholder="结束IP" onkeyup="this.value=this.value.replace(/[^\d.]/g,'')" onafterpaste="this.value=this.value.replace(/[^\d.]/g,'')" aria-describedby="inputGroupSuccess4Status" value="{{info.get('stopip','')}}">
                        <input type="text" style="width:140px" class="form-control" id="" name="otime" placeholder="租期(小时)" onkeyup="this.value=this.value.replace(/[^\d]/g,'')" onafterpaste="this.value=this.value.replace(/[^\d]/g,'')" aria-describedby="inputGroupSuccess4Status" value="{{info.get('otime','')}}">
                        </div>
                    </div>
		    <div class="modal-body" id='zone2'>
                      <div class="input-group">
                        <span class="input-group-addon">DHCP分配参数</span>
                        <input type="text" style="width:140px" class="form-control" id="" name="getgw" placeholder="被分配网关" onkeyup="this.value=this.value.replace(/[^\d.]/g,'')" onafterpaste="this.value=this.value.replace(/[^\d.]/g,'')" aria-describedby="inputGroupSuccess4Status" value="{{info.get('getgw','')}}">
                        <input type="text" style="width:140px" class="form-control" id="" name="getdns1" placeholder="被分配主DNS" onkeyup="this.value=this.value.replace(/[^\d.]/g,'')" onafterpaste="this.value=this.value.replace(/[^\d.]/g,'')" aria-describedby="inputGroupSuccess4Status" value="{{info.get('getdns1','')}}">
			<input type="text" style="width:140px" class="form-control" id="" name="getdns2" placeholder="被分配备DNS" onkeyup="this.value=this.value.replace(/[^\d.]/g,'')" onafterpaste="this.value=this.value.replace(/[^\d.]/g,'')" aria-describedby="inputGroupSuccess4Status" value="{{info.get('getdns2','')}}">
                        </div>
                    </div>
		    <div class="modal-body" id='zone3'>
                      <span class="input-group-addon" style="width:540px">DHCP固定分配</span>
                      <textarea id="dhcplist" name="dhcplist" onkeyup="this.value=this.value.replace(/[^\w\d.,:\\\n]/g,'')" onafterpaste="this.value=this.value.replace(/[^\w\d.,:\\\n]/g,'')" placeholder="格式: F0:79:59:92:C9:92,192.168.0.100" style="width:540px;height:100px;resize:vertical;">{{info.get('dhcplist','')}}</textarea>
                    </div>
                    <div class="modal-footer">
                        <button type="submit" style="float:left" class="btn btn-primary">保存</button>
                    </div>
                </div>
              </form>
            </div>
        </div>
    </div>
</div>
<script src="/assets/js/datetime/bootstrap-datepicker.js"></script> 
<script charset="utf-8" src="/assets/kindeditor/kindeditor.js"></script>
<script charset="utf-8" src="/assets/kindeditor/lang/zh_CN.js"></script>
<script language="JavaScript" type="text/javascript">
$(function(){
  $('#sel').click(function() {
    if (this.value == '1') {
    $('#zone1').show();
    $('#zone2').show();
    $('#zone3').show();
    //document.getElementById("selInput").readOnly=false ;
    /*显示 $('#selInput').show(); */
    } else {
    $('#zone1').hide();
    $('#zone2').hide();
    $('#zone3').hide();
    }
 });
 $('#sel').click();
});
</script>
