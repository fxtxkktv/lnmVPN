%rebase base position='添加策略配置', managetopli="vpnserv"
<div class="page-body">
    <div class="row">
        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">
            <div class="widget">
                <div class="widget-header bordered-bottom bordered-themesecondary">
                    <i class="widget-icon fa fa-tags themesecondary"></i>
                    <span class="widget-caption themesecondary">添加策略</span>
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
                            <span class="input-group-addon">策略名称</span>
                            <input type="text" style="width:420px" class="form-control" id="" name="name" aria-describedby="inputGroupSuccess4Status" value="{{info.get('name','')}}">
                        </div>
                    </div>
		    <div class="modal-body">
                        <span class="input-group-addon" style="width:500px">推送DNS</span>
                        <textarea id="pushdns" name="pushdns" onkeyup="this.value=this.value.replace(/[^\d.\\\n]/g,'')" onafterpaste="this.value=this.value.replace(/[^\d.]/g,'')" placeholder="eg: 8.8.8.8" style="width:500px;height:50px;">{{info.get('pushdns','')}}</textarea>
                    </div>
		    <div class="modal-body">
		    	<span class="input-group-addon" style="width:500px">推送安全路由</span>
			<textarea id="pushroute" name="pushroute" onkeyup="this.value=this.value.replace(/[^\d.\/\\\n]/g,'')" onafterpaste="this.value=this.value.replace(/[^\d.]/g,'')" placeholder="eg: 192.168.5.0/255.255.255.0" style="width:500px;height:100px;">{{info.get('pushroute','')}}</textarea>
                    </div>
		    <div class="modal-body">
			<span class="input-group-addon" style="width:500px">推送本地路由</span>
			<textarea id="pushnoroute" name="pushnoroute" onkeyup="this.value=this.value.replace(/[^\d.\/\\\n]/g,'')" onafterpaste="this.value=this.value.replace(/[^\d.]/g,'')" placeholder="eg: 192.168.5.0/255.255.255.0" style="width:500px;height:100px;">{{info.get('pushnoroute','')}}</textarea>
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
