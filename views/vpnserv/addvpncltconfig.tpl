%rebase base position='添加VPN服务配置', managetopli="vpnserv"
<div class="page-body">
    <div class="row">
        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">
            <div class="widget">
                <div class="widget-header bordered-bottom bordered-themesecondary">
                    <i class="widget-icon fa fa-tags themesecondary"></i>
                    <span class="widget-caption themesecondary">添加配置</span>
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
                           <span class="input-group-addon">验证方式&emsp;</span>
                           <select style="width:420px" class="form-control" id="sel" name="authtype">
                                <option 
                        		%if info.get('authtype','') == '0':
                                    selected
                                %end 
                                    value="0">证书认证
                                </option>
                                <option 
                                %if info.get('authtype','') == '1':
                                    selected
                                %end 
                                    value="1">密码认证
                                </option>
                                <option 
                                %if info.get('authtype','') == '2':
                                    selected
                                %end 
                                    value="2">关闭服务 
                                </option>
                            </select>
                        </div>
                   </div>
		    <div class="modal-body" id="servinfo">
                 <div class="input-group">
                      <span class="input-group-addon">服务器地址</span>
			          <input type="text" style="width:210px" class="form-control" id="ipaddr" name="ipaddr" placeholder="服务器地址" aria-describedby="inputGroupSuccess4Status"
			                %if info.get('ipaddr',''): 
                                value="{{info.get('ipaddr','')}}"
                            %end 
			          >
			          <input type="text" style="width:210px" class="form-control" id="servport" name="servport" onkeyup="this.value=this.value.replace(/[^\d]/g,'')" onafterpaste="this.value=this.value.replace(/[^\d]/g,'')" placeholder="服务端口" aria-describedby="inputGroupSuccess4Status" 
			                 %if info.get('servport',''): 
			   	                 value="{{info.get('servport','')}}"
			                 %else :
				                 value="443"
			                 %end 
			          >
                 </div>
            </div>
             <div class="modal-body" id="servopts">
                 <div class="input-group">
                      <span class="input-group-addon">连接参数&emsp;</span>
                      <input type="text" style="width:210px" class="form-control" onkeyup="this.value=this.value.replace(/[^\d]/g,'')" id="tunid" name="tunid" placeholder="虚拟接口ID" aria-describedby="inputGroupSuccess4Status"
                            %if info.get('tunid',''): 
                                value="{{info.get('tunid','')}}"
                            %end 
                      readonly>
                      <input type="text" style="width:210px" class="form-control" id="vmtu" name="vmtu" onkeyup="this.value=this.value.replace(/[^\d]/g,'')" onafterpaste="this.value=this.value.replace(/[^\d]/g,'')" placeholder="MTU值" aria-describedby="inputGroupSuccess4Status" 
                             %if info.get('vmtu',''): 
                                 value="{{info.get('vmtu','')}}"
                             %end 
                      >
                 </div>
            </div>
		    <div class="modal-body" id="chkconn">
                 <div class="input-group">
                      <span class="input-group-addon" hidden>连接检测&emsp;</span>
                      <select style="width:420px" class="form-control" name="chkconn">
                                <option 
                                %if info.get('chkconn','') == '1':
                                        selected
                                %end 
                                     value="1">启用VPN自动检测连接
                                </option>
                                <option 
                                %if info.get('chkconn','') == '0':
                                        selected
                                %end 
                                     value="0">禁用VPN自动检测连接
                                </option>
                         </select>
                 </div>
            </div>
		    <div class="modal-body" id="signa">
                 <div class="input-group">
                          <span class="input-group-addon">验证信息&emsp;</span>
                          <input type="text" style="width:210px;" class="form-control" id="vpnuser" name="vpnuser" placeholder="用户名" aria-describedby="inputGroupSuccess4Status" 
			              %if info.get('vpnuser',''): 
                                value="{{info.get('vpnuser','')}}"
                          %end
			              >
			              <input type="password" style="width:210px;" class="form-control" id="vpnpass" name="vpnpass" placeholder="密码" aria-describedby="inputGroupSuccess4Status"
			              %if info.get('vpnpass',''): 
                                value="{{info.get('vpnpass','')}}"
                          %end 
			              >
                 </div>
            </div>
		    <div class="modal-body" id="signb">
                        <span class="input-group-addon" style="width:520px">CA签名信息</span>
                        <textarea id="cainfo" name="cainfo" style="width:520px;height:100px;resize:vertical;">{{info.get('cainfo','')}}</textarea>
             </div>
             <div class="modal-body" id="signc">
                        <span class="input-group-addon" style="width:520px">客户端证书信息</span>
                        <textarea id="certinfo" name="certinfo" style="width:520px;height:100px;resize:vertical;">{{info.get('certinfo','')}}</textarea>
             </div>
		     <div class="modal-body" id="signd">
                        <span style="color:#666666;">备注:<br/>1.当连接检测启用时,务必确保配置信息可连接,否则容易出现网络不稳定.<br/>2.VPN网络接口ID默认为1000,即tun1000表示<br/>3.MTU值1000~1500(须整除4) </span>
             </div>
             <div class="modal-footer">
                        <button type="submit" style="float:left" class="btn btn-primary">保存配置</button>
			            <a id="rego" style="float:left" class="btn btn-primary" href="/vpnservconf">返回</a>
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
    if (this.value == '0') {
    $('#servinfo').show();
    $('#chkconn').show();
	$('#signa').hide();
	$('#signb').show();
    $('#signc').show();
    $('#signd').show();
    //document.getElementById("selInput").readOnly=false ;
    /*显示 $('#selInput').show(); */
    } else if (this.value == '1'){
    $('#servinfo').show();
    $('#chkconn').show();
	$('#signb').hide();
	$('#signc').hide();
	$('#signa').show();
    $('#signd').show();
    } else {
    $('#servinfo').hide();
    $('#chkconn').hide();
    $('#signb').hide();
    $('#signc').hide();
    $('#signa').hide();
    $('#signd').hide();
    }
 });
 $('#sel').click();
});
</script>
