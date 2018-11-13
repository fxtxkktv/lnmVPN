%rebase base position='添加高级路由', managetopli="networks"
<div class="page-body">
    <div class="row">
        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">
            <div class="widget">
                <div class="widget-header bordered-bottom bordered-themesecondary">
                    <i class="widget-icon fa fa-tags themesecondary"></i>
                    <span class="widget-caption themesecondary">添加高级路由</span>
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
                        <textarea id="srcaddr" name="srcaddr" placeholder="eg: 192.168.5.0/255.255.255.0 一行一个" style="width:500px;height:100px;">{{info.get('srcaddr','')}}</textarea>
                    </div>
		    <div class="modal-body">
		    	<span class="input-group-addon" style="width:500px">目标地址</span>
			<textarea id="destaddr" name="destaddr" placeholder="eg: 192.168.5.0/255.255.255.0 一行一个" style="width:500px;height:100px;">{{info.get('destaddr','')}}</textarea>
                    </div>
		    <div class="modal-body">
                        <div class="input-group">
                            <span class="input-group-addon">优先级&emsp;</span>
                            <input type="text" style="width:420px" class="form-control" id="pronum" name="pronum" aria-describedby="inputGroupSuccess4Status" onkeyup="if(this.value.length==1){this.value=this.value.replace(/[^1-9]/g,'')}else{this.value=this.value.replace(/\D/g,'')}" onafterpaste="if(this.value.length==1){this.value=this.value.replace(/[^1-9]/g,'')}else{this.value=this.value.replace(/\D/g,'')}" placeholder="该数字必须满足: 100<x<32765" value="{{info.get('pronum','')}}">
                        </div>
                   </div>
		    <div class="modal-body">
		      <div class="input-group">
			<span class="input-group-addon">指定出口</span>
			<select style="width:420px" class="form-control" name="ifacename">
                                        <option value=''>请选择出口设备</option>
                                        %for infos in ifacelist_result:
                                                           <option
                                                                %if info.get('iface','') == infos.get('ifacename',''): 
                                                                        selected 
                                                                %end 
                                                                value='{{infos.get('ifacename','')}}'> {{infos.get('ifacename','')}}
                                                           </option>

                                        %end
                        </select>
		    </div>    
                    <div class="modal-footer">
                        <button type="submit" style="float:left" class="btn btn-primary">保存</button>
			<a id="rego" style="float:left" class="btn btn-primary" href="/advroute">返回</a>
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
