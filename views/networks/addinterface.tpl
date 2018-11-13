%rebase base position='添加网络接口', managetopli="networks"
<div class="page-body">
    <div class="row">
        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">
            <div class="widget">
                <div class="widget-header bordered-bottom bordered-themesecondary">
                    <i class="widget-icon fa fa-tags themesecondary"></i>
                    <span class="widget-caption themesecondary">添加接口</span>
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
                            <span class="input-group-addon">物理网卡</span>
                                  <select style="width:420px" class="form-control" name="ifacename">
                    			<option value=''>请选择绑定的网卡</option>
					%for infos in ifacelist_result:
							   <option
                                                		%if infos.get('ifacename',''): 
                                                        		selected 
                                                		%end 
                                                		value='{{infos.get('ifacename','')}}'> {{infos.get('value','')}}
                                             		   </option>
						
					%end
                 		  </select>
                        </div>
                    </div>
                    <div class="modal-body">
                        <div class="input-group">
                            <span class="input-group-addon">连接类型</span>
                            <select style="width:420px" class="form-control" name="ifacetype">
			    	<option 
					%if info.get('ifacetype','')=='STATIC': 
						selected 
					%end 
					value='STATIC'>固定IP
				</option>
                                <!--option 
					%if info.get('ifacetype','')=='DHCP':
						selected 
					%end 
					value='DHCP'>动态获取
				</option>
                                <option 
					%if info.get('ifacetype','')=='ADSL': 
						selected 
					%end 
					value='ADSL'>ADSL拨号
				</option-->
                            </select>
                        </div>
                    </div>
		    <div class="modal-body">
                        <div class="input-group">
                            <span class="input-group-addon">IP&emsp;地址</span>
                            <input type="text" style="width:420px" class="form-control" id="" name="ipaddr" onkeyup="this.value=this.value.replace(/[^\d.]/g,'')" onafterpaste="this.value=this.value.replace(/[^\d.]/g,'')" aria-describedby="inputGroupSuccess4Status" value="{{info.get('ipaddr','')}}">
                        </div>
                    </div>
		    <div class="modal-body">
                        <div class="input-group">
                            <span class="input-group-addon">子网掩码</span>
                            <input type="text" style="width:420px" class="form-control" id="" name="netmask" onkeyup="this.value=this.value.replace(/[^\d.]/g,'')" onafterpaste="this.value=this.value.replace(/[^\d.]/g,'')" aria-describedby="inputGroupSuccess4Status" value="{{info.get('netmask','')}}">
                        </div>
                    </div>
		    <div class="modal-body">
                        <div class="input-group">
                            <span class="input-group-addon">网关地址</span>
                            <input type="text" style="width:210px" class="form-control" id="" name="gateway" onkeyup="this.value=this.value.replace(/[^\d.]/g,'')" onafterpaste="this.value=this.value.replace(/[^\d.]/g,'')" aria-describedby="inputGroupSuccess4Status" value="{{info.get('gateway','')}}">
			    <!--input type="checkbox" style="width:120px" class="form-control" name="defaultgw" value="1" checked="checked" /-->
			    <select style="width:210px" class="form-control" name="defaultgw">
                                        <option 
					%if info.get('defaultgw','') == 0:
						selected
					%end 
					value='0'>非默认网关</option>
                                        <option
					%if info.get('defaultgw','') == 1:
                                                selected
                                        %end 
                                                value='1'> 默认网关
                                        </option>
                            </select>
                        </div>
                    </div>
		    <div class="modal-body">
                      <span class="input-group-addon" style="width:500px">扩展属性</span>
                      <textarea id="extip" name="extip" onkeyup="this.value=this.value.replace(/[^\d.\/\\\n]/g,'')" onafterpaste="this.value=this.value.replace(/[^\d.]/g,'')" placeholder="eg: IP地址/子网掩码/网关地址" style="width:500px;height:100px;">{{info.get('extip','')}}</textarea>
                    </div>
                    <div class="modal-footer">
                        <button type="submit" style="float:left" class="btn btn-primary">提交</button>
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
