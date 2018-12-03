%rebase base position='添加NAT配置', managetopli="firewall"
<div class="page-body">
    <div class="row">
        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">
            <div class="widget">
                <div class="widget-header bordered-bottom bordered-themesecondary">
                    <i class="widget-icon fa fa-tags themesecondary"></i>
                    <span class="widget-caption themesecondary">添加NAT配置</span>
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
                            <span class="input-group-addon">规则描述</span>
                            <input type="text" style="width:420px" class="form-control" id="" name="rulename" aria-describedby="inputGroupSuccess4Status" value="{{info.get('rulename','')}}">
                        </div>
                    </div>
		    
		    <div class="modal-body">
                        <span class="input-group-addon" style="width:500px">源地址</span>
                        <textarea id="srcaddr" name="srcaddr" onkeyup="this.value=this.value.replace(/[^\d.\/\\\n]/g,'')" onafterpaste="this.value=this.value.replace(/[^\d.]/g,'')" placeholder="eg: 192.168.5.0/255.255.255.0" style="width:500px;height:100px;resize:vertical;">{{info.get('srcaddr','')}}</textarea>
                    </div>
		    <div class="modal-body">
			<div class="input-group">
		    	<span class="input-group-addon" style="width:80px">目标网络</span>
			<select style="width:100px;height:30px;" class="form-control" name="dstmatch">
                        <option 
                                        %if info.get('dstmatch','')== 1: 
                                                selected 
                                        %end 
                                        value="1">匹配
                        </option>
                        <option 
                                        %if info.get('dstmatch','')== 0: 
                                                selected 
                                        %end 
                                        value="0">非匹配
                        </option>
                        </select>
			</div>
			<textarea id="dstaddr" name="dstaddr" onkeyup="this.value=this.value.replace(/[^\d.\/\\\n]/g,'')" onafterpaste="this.value=this.value.replace(/[^\d.]/g,'')" placeholder="eg: 192.168.5.0/255.255.255.0" style="width:500px;height:100px;resize:vertical;">{{info.get('dstaddr','')}}</textarea>
                    </div>
		    <div class="modal-body">
			<div class="input-group">
			<span class="input-group-addon" style="width:80px">执行动作</span>
			<select style="width:150px" class="form-control" id="runaction" name="runaction">
                        <option 
                                        %if info.get('runaction','')=="SNAT": 
                                                selected 
                                        %end 
                                        value="SNAT">源地址转换SNAT
                        </option>
                        <option 
                                        %if info.get('runaction','')=="MASQ": 
                                                selected 
                                        %end 
                                        value="MASQ">源地址接口伪装
                        </option>
                        </select>
			<input type="text" style="width:270px" class="form-control" id="runobject" name="runobject" onkeyup="this.value=this.value.replace(/[^\d.]/g,'')" onafterpaste="this.value=this.value.replace(/[^\d.]/g,'')" aria-describedby="inputGroupSuccess4Status" value="{{info.get('runobject','')}}">
			<select style="width:270px" class="form-control" id="runobject2" name="runobject2">
                        %for infos in ifacelist_result:
                            <option
			                %if info.get('runobject2','')==infos.get('ifacename','') : 
                                selected 
                            %end 
                            value='{{infos.get('ifacename','')}}'>{{infos.get('ifacename','')}}
                            </option>
                        %end
                        </select>
			</div>
		    </div>    
                    <div class="modal-footer">
                        <button type="submit" style="float:left" class="btn btn-primary">保存</button>
			<a id="rego" style="float:left" class="btn btn-primary" href="/natruleconf">返回</a>
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
  $('#runaction').click(function() {
    if (this.value == 'MASQ') {
        $('#runobject').hide();
	$('#runobject2').show();
    } else {
	$('#runobject').show();
        $('#runobject2').hide();
    }
  });
  $('#runaction').click()
});
</script>
