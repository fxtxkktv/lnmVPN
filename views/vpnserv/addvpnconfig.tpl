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
            <div class="modal-body">
              <div class="input-group">
                <span class="input-group-addon">OC服务状态</span>
                %if info.get('servstatus','') == '0' :
                    <input type="text" style="width:415px;color:green;font-weight:bold;" class="form-control" id="" name="record" aria-describedby="inputGroupSuccess4Status" value="正在运行" readonly>
                %else :
                    <input type="text" style="width:415px;color:red;font-weight:bold;" class="form-control" id="" name="record" aria-describedby="inputGroupSuccess4Status" value="服务关闭" readonly>
                %end
              </div>
            </div>
		    <div class="modal-body">
                        <div class="input-group">
                           <span class="input-group-addon">验证方式&emsp;</span>
                           <select style="width:420px" class="form-control" id="sel" name="authtype">
             <option 
                %if info.get('authtype','') == '2':
                    selected
                %end 
                                value="2">支持证书+密码认证          
                                </option>
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
                %if info.get('authtype','') == '3':
                    selected
                %end 
                                        value="3">关闭服务
                                </option>
                            </select>
                        </div>
                   </div>
            <div class="modal-body" id="p_a">
                        <div class="input-group">
                          <span class="input-group-addon">监听信息&emsp;</span>
                          <input type="text" style="width:210px" class="form-control" id="" name="ipaddr" onkeyup="this.value=this.value.replace(/[^\d.*]/g,'')" onafterpaste="this.value=this.value.replace(/[^\d.]/g,'')" placeholder="IP地址" aria-describedby="inputGroupSuccess4Status"
                           %if info.get('ipaddr',''): 
                                value="{{info.get('ipaddr','')}}"
                           %else :
                                value="*"
                           %end 
             >
			  <input type="text" style="width:210px" class="form-control" id="" name="servport" onkeyup="this.value=this.value.replace(/[^\d]/g,'')" onafterpaste="this.value=this.value.replace(/[^\d.]/g,'')" placeholder="监听端口" aria-describedby="inputGroupSuccess4Status" 
			   %if info.get('servport',''): 
			   	value="{{info.get('servport','')}}"
			   %else :
				value="443"
			   %end 
			   >
                        </div>
                    </div>
		    <div class="modal-body" id="p_b">
                        <div class="input-group">
                          <span class="input-group-addon">虚拟网络段</span>
                          <input type="text" style="width:210px" class="form-control" id="" name="virip" onkeyup="this.value=this.value.replace(/[^\d.]/g,'')" onafterpaste="this.value=this.value.replace(/[^\d.]/g,'')" placeholder="虚拟IP" aria-describedby="inputGroupSuccess4Status"
			  %if info.get('virip',''): 
                                value="{{info.get('virip','')}}"
                           %else :
                                value="66.66.6.0"
                           %end 
			  >
                          <input type="text" style="width:210px" class="form-control" id="" name="virmask" onkeyup="this.value=this.value.replace(/[^\d.]/g,'')" onafterpaste="this.value=this.value.replace(/[^\d.]/g,'')" placeholder="子网掩码" aria-describedby="inputGroupSuccess4Status"
			  %if info.get('virmask',''): 
                                value="{{info.get('virmask','')}}"
                           %else :
                                value="255.255.255.0"
                           %end 
                           >
                        </div>
                    </div>
		    <div class="modal-body" id="p_c">
                        <div class="input-group">
                          <span class="input-group-addon">连接数控制</span>
                          <input type="text" style="width:210px" class="form-control" id="" name="maxclient" onkeyup="this.value=this.value.replace(/[^\d]/g,'')" onafterpaste="this.value=this.value.replace(/[^\d.]/g,'')" placeholder="最大连接数" aria-describedby="inputGroupSuccess4Status" 
			  %if info.get('maxclient',''): 
                                value="{{info.get('maxclient','')}}"
                           %else :
                                value="100"
                           %end 
			  >
			  <input type="text" style="width:210px" class="form-control" id="" name="maxuser" onkeyup="this.value=this.value.replace(/[^\d]/g,'')" onafterpaste="this.value=this.value.replace(/[^\d.]/g,'')" placeholder="最大并发数" aria-describedby="inputGroupSuccess4Status"
			  %if info.get('maxuser',''): 
                                value="{{info.get('maxuser','')}}"
                          %else :
                                value="3"
                          %end 
			 >
                       </div>
                    </div>
		    <div class="modal-body" id="p_d">
		    	<div class="input-group">
			   <span class="input-group-addon">验证控制&emsp;</span>
			   <input type="text" style="width:140px" class="form-control" id="" name="authtimeout" onkeyup="this.value=this.value.replace(/[^\d]/g,'')" onafterpaste="this.value=this.value.replace(/[^\d.]/g,'')" placeholder="验证超时时间(s)" aria-describedby="inputGroupSuccess4Status" 
			   %if info.get('authtimeout',''): 
                                value="{{info.get('authtimeout','')}}"
                           %else :
                                value="120"
                           %end 
			   >
			   <input type="text" style="width:140px" class="form-control" id="" name="authnum" onkeyup="this.value=this.value.replace(/[^\d]/g,'')" onafterpaste="this.value=this.value.replace(/[^\d.]/g,'')" placeholder="验证次数锁定" aria-describedby="inputGroupSuccess4Status"
			   %if info.get('authnum',''): 
                                value="{{info.get('authnum','')}}"
                           %else :
                                value="5"
                           %end 
                           >
			   <input type="text" style="width:140px" class="form-control" id="" name="locktime" onkeyup="this.value=this.value.replace(/[^\d]/g,'')" onafterpaste="this.value=this.value.replace(/[^\d.]/g,'')" placeholder="验证锁定时长(s)" aria-describedby="inputGroupSuccess4Status"
			   %if info.get('locktime',''): 
                                value="{{info.get('locktime','')}}"
                           %else :
                                value="300"
                           %end 
                           >
		    	</div>
		    </div>
		    <div class="modal-body" id="p_e">
                        <div class="input-group">
			   <span class="input-group-addon">启用压缩&emsp;</span>
			   <select style="width:420px" class="form-control" name="comp">
                                <option 
				%if info.get('comp','')=='0' : 
                                    selected    
				%end 
				value="0">启用 
                                </option>
                                <option 
				%if info.get('comp','')=='1' : 
                                    selected    
                                %end 
                                        value="1">禁用
                                </option>
                            </select>
			</div>
		   </div>
		   <div class="modal-body" id="p_f">
			 <div class="input-group">
                           <span class="input-group-addon">AnyConnect支持</span>
                           <select style="width:387px" class="form-control" name="cisco">
                                <option
                                %if info.get('cisco','')=='0' : 
                                    selected
                                %end 
                                value="0">启用                   
                                </option>
                                <option 
                                %if info.get('cisco','')=='1' : 
                                    selected
                                %end 
                                        value="1">禁用
                                </option>
                            </select>
              </div>
           </div>
           <div class="modal-body" id="p_g">
                       <span style="color:red;">备注: 如服务启动失败请检查<strong>&nbsp;证书已初始化&nbsp;</strong>且<strong>&nbsp;已配置组策略ProfileXML属性文件.&nbsp;</strong></span>
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
    if (this.value == '3') {
    $('#p_a').hide();
    $('#p_b').hide();
    $('#p_c').hide();
    $('#p_d').hide();
    $('#p_e').hide();
    $('#p_f').hide();
    $('#p_g').hide();
    } else {
    $('#p_a').show();
    $('#p_b').show();
    $('#p_c').show();
    $('#p_d').show();
    $('#p_e').show();
    $('#p_f').show();
    $('#p_g').show();
    }
 });
 $('#sel').click();
});
</script>
