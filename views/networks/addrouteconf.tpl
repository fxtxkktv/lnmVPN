%rebase base position='添加路由', managetopli="networks"
<div class="page-body">
    <div class="row">
        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">
            <div class="widget">
                <div class="widget-header bordered-bottom bordered-themesecondary">
                    <i class="widget-icon fa fa-tags themesecondary"></i>
                    <span class="widget-caption themesecondary">添加静态路由</span>
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
                            <span class="input-group-addon">路由类型</span>
                            <select style="width:420px" class="form-control" name="rttype">
			    	<option 
					%if info.get('rttype','')=='net': 
						selected 
					%end 
					value='net'>网络路由
				</option>
                            </select>
                        </div>
                    </div>
		    <div class="modal-body">
                        <div class="input-group">
                            <span class="input-group-addon">IP&emsp;地址</span>
                            <input type="text" style="width:420px" class="form-control" id="" name="ipaddr" onkeyup="this.value=this.value.replace(/[^\d.]/g,'')" onafterpaste="this.value=this.value.replace(/[^
\d.]/g,'')" aria-describedby="inputGroupSuccess4Status" value="{{info.get('ipaddr','')}}">
                        </div>
                    </div>
		    <div class="modal-body">
                        <div class="input-group">
                            <span class="input-group-addon">子网掩码</span>
                            <input type="text" style="width:420px" class="form-control" id="" name="netmask" onkeyup="this.value=this.value.replace(/[^\d.]/g,'')" onafterpaste="this.value=this.value.replace(/[^
\d.]/g,'')" aria-describedby="inputGroupSuccess4Status" value="{{info.get('netmask','')}}">
                        </div>
                    </div>
		    <div class="modal-body">
                        <div class="input-group">
                            <span class="input-group-addon">网关地址</span>
                            <input type="text" style="width:420px" class="form-control" id="" name="gateway" onkeyup="this.value=this.value.replace(/[^\d.]/g,'')" onafterpaste="this.value=this.value.replace(/[^
\d.]/g,'')" aria-describedby="inputGroupSuccess4Status" value="{{info.get('gateway','')}}">
                        </div>
                    </div>
		   <div class="modal-body">
		    	<div class="input-group">
				<span class="input-group-addon">绑定接口</span>
				<select style="width:420px" class="form-control" name="gwiface">
				<option value="auto">自动匹配</option>
				%for ifacelist in ifacelist_result :
                                   <option 
                                        %if info.get('ifacename','') : 
                                                selected 
                                        %end 
                                        value='{{ifacelist.get('ifacename','')}}' > {{ifacelist.get('ifacename','')}}
                                   </option>
				%end
			   </select>
		    	</div>
		    </div>
                    <div class="modal-footer">
                        <button type="submit" style="float:left" class="btn btn-primary">保存</button>
			<a id="rego" style="float:left" class="btn btn-primary" href="#" onclick="javascript:history.back(-1);">返回</a>
                    </div>
               </form>
	      </div>
            </div>
        </div>
    </div>
</div>
<script src="/assets/js/datetime/bootstrap-datepicker.js"></script> 
<script charset="utf-8" src="/assets/kindeditor/kindeditor.js"></script>
<script charset="utf-8" src="/assets/kindeditor/lang/zh_CN.js"></script>
