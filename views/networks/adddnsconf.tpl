%rebase base position='添加DNS记录', managetopli="networks"
<div class="page-body">
    <div class="row">
        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">
            <div class="widget">
                <div class="widget-header bordered-bottom bordered-themesecondary">
                    <i class="widget-icon fa fa-tags themesecondary"></i>
                    <span class="widget-caption themesecondary">添加记录</span>
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
                            <span class="input-group-addon">记录类型</span>
                            <select style="width:420px" class="form-control" id="sel" name="dnstype">
			    	<option 
					%if info.get('dnstype','')=='A': 
						selected 
					%end 
					value='A'>A记录
				</option>
                                <option 
					%if info.get('dnstype','')=='MX':
						selected 
					%end 
					value='MX'>MX记录
				</option>
				<option 
                                        %if info.get('dnstype','')=='CNAME':
                                                selected 
                                        %end 
                                        value='CNAME'>CNAME记录
                                </option>
				<option 
                                        %if info.get('dnstype','')=='NS':
                                                selected 
                                        %end 
                                        value='NS'>NS转发记录
                                </option>
                                <option 
					%if info.get('dnstype','')=='PTR': 
						selected 
					%end 
					value='PTR'>PTX记录
				</option>
				<!--option 
                                        %if info.get('dnstype','')=='TXT': 
                                                selected 
                                        %end 
                                        value='TXT'>TXT记录
                                </option-->
                            </select>
                        </div>
                    </div>
		    <div class="modal-body">
                        <div class="input-group">
                            <span class="input-group-addon">域名名称</span>
                            <input type="text" style="width:420px" class="form-control" id="" name="domain" aria-describedby="inputGroupSuccess4Status" value="{{info.get('domain','')}}">
                        </div>
                    </div>
		    <div class="modal-body">
                        <div class="input-group">
                            <span class="input-group-addon">记录数据</span>
                            <input type="text" style="width:420px" class="form-control" id="" name="record" aria-describedby="inputGroupSuccess4Status" value="{{info.get('record','')}}">
                        </div>
                    </div>
		    <div class="modal-body">
                        <div class="input-group">
                            <span class="input-group-addon">优先级&emsp;</span>
                            <input type="text" style="width:420px" class="form-control" id="selInput" name="pronum" aria-describedby="inputGroupSuccess4Status" onkeyup="if(this.value.length==1){this.value=this.value.replace(/[^1-9]/g,'')}else{this.value=this.value.replace(/\D/g,'')}" onafterpaste="if(this.value.length==1){this.value=this.value.replace(/[^1-9]/g,'')}else{this.value=this.value.replace(/\D/g,'')}" value="{{info.get('pronum','')}}">
                        </div>
                   </div>
		   <div class="modal-footer">
                        <button type="submit" style="float:left" class="btn btn-primary">提交</button>
			<a id="rego" style="float:left" class="btn btn-primary" href="#" onclick="javascript:history.back(-1);">返回</a>
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
$(function() {
  $('#sel').click(function() {
    if (this.value == 'MX') {
	document.getElementById("selInput").readOnly=false ;
        /*显示 $('#selInput').show(); */
    } else {
	document.getElementById("selInput").readOnly=true ;
        /*隐藏 $('#selInput').hide(); */
    }
  });
  $('#sel').click();
});
</script>
