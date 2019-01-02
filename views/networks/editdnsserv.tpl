%rebase base position='DNS服务配置', managetopli="networks"
<div class="page-body">
    <div class="row">
        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">
            <div class="widget">
                <div class="widget-header bordered-bottom bordered-themesecondary">
                    <i class="widget-icon fa fa-tags themesecondary"></i>
                    <span class="widget-caption themesecondary">DNS服务配置</span>
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
                <span class="input-group-addon" style="width:100px">DNS服务状态&emsp;&emsp;</span>
			    %if info.get('dnsstatus','') == 0 :
                    <input type="text" style="width:210px;color:green;font-weight:bold;" class="form-control" id="" name="record" aria-describedby="inputGroupSuccess4Status" value="正在运行" readonly>
			    %else :
                    <input type="text" style="width:210px;color:red;font-weight:bold;" class="form-control" id="" name="record" aria-describedby="inputGroupSuccess4Status" value="服务关闭" readonly>
			    %end
              </div>
            </div>
		    <div class="modal-body">
                        <div class="input-group">
                            <span class="input-group-addon" style="width:100px">DNS中继服务&emsp;&emsp;</span>
			    <select style="width:210px" class="form-control" name="dnsrelay">
                                        <option 
                                        %if info.get('dnsrelay','') == '0':
                                                selected
                                        %end 
                                        value='0'>关闭</option>
                                        <option
                                        %if info.get('dnsrelay','') == '1':
                                                selected
                                        %end 
                                                value='1'>开启
                                        </option>
                            </select>
                        </div>
                    </div>
		    <div class="modal-body">
                        <div class="input-group">
                            <span class="input-group-addon">中继所有DNS请求</span>
			    <select style="width:210px" class="form-control" name="dnsproxy">
                                        <option 
					%if info.get('dnsproxy','') == '0':
						selected
					%end 
					value='0'>关闭</option>
                                        <option
					%if info.get('dnsproxy','') == '1':
                                                selected
                                        %end 
                                                value='1'>开启
                                        </option>
                            </select>
                        </div>
                    </div>
		    <div class="modal-body">
                        <div class="input-group">
                            <span class="input-group-addon">DNS防污染 [VPN]</span>
                            <select style="width:210px" class="form-control" name="dnsrule">
                                        <option 
                                        %if info.get('dnsrule','') == '0':
                                                selected
                                        %end 
                                        value='0'>关闭</option>
                                        <option
                                        %if info.get('dnsrule','') == '1':
                                                selected
                                        %end 
                                                value='1'>开启
                                        </option>
                            </select>
                        </div>
                    </div>
		    <div class="modal-body">
                      <span class="input-group-addon" style="width:350px">DNS中继列表</span>
                      <textarea id="dnslist" name="dnslist" onkeyup="this.value=this.value.replace(/[^\d.\\\n]/g,'')" onafterpaste="this.value=this.value.replace(/[^\d.]/g,'')" placeholder="eg: DNS IP地址" style="width:350px;height:100px;resize:vertical;">{{info.get('dnslist','')}}</textarea>
                    </div>
                    <div class="modal-body">
                        <span style="color:#666666;" id="signc">备注<br/>1.DNS服务默认强制取代本机DNS查询<br/>2.DNS防污染开启时，请确保VPN连接正常，且DNS未被劫持.</span>
                    </div>
                    <div class="modal-footer">
                        <button type="submit" style="float:left" class="btn btn-primary">保存</button>
			<a id="adddnsconf" style="float:left" href="/dnsservconf" class="btn btn-primary ">返回</a>
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
