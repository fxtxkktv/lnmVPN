%rebase base position='添加用户证书', managetopli="vpnserv"
<div class="page-body">
    <div class="row">
        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">
            <div class="widget">
                <div class="widget-header bordered-bottom bordered-themesecondary">
                    <i class="widget-icon fa fa-tags themesecondary"></i>
                    <span class="widget-caption themesecondary">添加客户端证书</span>
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
                            <span class="input-group-addon">证书类型</span>
			       <select id="policy" style="width:420px;" name="certtype">
                    			<option value='client'>用户证书</option>
                 		</select>
                        </div>
                    </div>
		    <div class="modal-body">
                        <div class="input-group">
                            <span class="input-group-addon">使用者&emsp;</span>
                            <input type="text" style="width:420px" class="form-control" id="" name="commonname" aria-describedby="inputGroupSuccess4Status" value="{{info.get('netmask','')}}">
                        </div>
                    </div>
		    <div class="modal-body">
                         <div class="input-group">
                                <span class="input-group-addon">应用策略</span>
                                <select id="organization" style="width:420px;" name="organization">
                                <option value=''>请选择策略</option>
                                %for name in plylist_result:
                                        <option 
                                        value='{{name.get('id','')}}'>{{name.get('name','')}}
                                        </option>
                                %end
                                </select>
                        </div>
                    </div>
		    <div class="modal-body">
                        <div class="input-group">
                            <span class="input-group-addon">有效期&emsp;</span>
                            <input type="text" style="width:420px" class="form-control" id="" name="expiration" onkeyup="if(this.value.length==1){this.value=this.value.replace(/[^1-9]/g,'')}else{this.value=this.value.replace(/\D/g,'')}" onafterpaste="if(this.value.length==1){this.value=this.value.replace(/[^1-9]/g,'')}else{this.value=this.value.replace(/\D/g,'')}"placeholder="有效天数(days)" aria-describedby="inputGroupSuccess4Status" 
			    %if info.get('authtimeout',''): 
                                value="{{info.get('authtimeout','')}}"
                            %else :
                                value="365"
                            %end 
			    >
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="submit" style="float:left" class="btn btn-primary">提交</button>
			<a id="rego" style="float:left" class="btn btn-primary" href="/certmgr">返回</a>
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
