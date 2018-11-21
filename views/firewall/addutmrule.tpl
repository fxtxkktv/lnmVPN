%rebase base position='添加UTM配置', managetopli="firewall"
<div class="page-body">
    <div class="row">
        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">
            <div class="widget">
                <div class="widget-header bordered-bottom bordered-themesecondary">
                    <i class="widget-icon fa fa-tags themesecondary"></i>
                    <span class="widget-caption themesecondary">添加UTM配置</span>
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
                          <input type="text" style="width:210px" class="form-control" id="" placeholder="规则名称" name="rulename" aria-describedby="inputGroupSuccess4Status" value="{{info.get('rulename','')}}">
			  <input type="text" style="width:210px" class="form-control" id="" placeholder="优先级" name="pronum" aria-describedby="inputGroupSuccess4Status" value="{{info.get('pronum','')}}">
                        </div>
                    </div>
		    <div class="modal-body">
			<div class="input-group">
                          <span class="input-group-addon" style="width:80px">应用区域</span>
                          <select style="width:420px" class="form-control" id="actzone" name="actzone">
                          <option 
                                        %if info.get('actzone','')=="INPUT": 
                                                selected 
                                        %end 
                                        value="INPUT">本机数据
                          </option>
                          <option 
                                        %if info.get('actzone','')=="FORWARD": 
                                                selected 
                                        %end
                                        value="FORWARD">外部转发
                          </option>
			  </select>
			</div>
                    </div>
		    <div class="modal-body">
			<div class="input-group">
                        <span class="input-group-addon" style="width:500px">源地址&emsp;</span>
			</div>
                        <textarea id="srcaddr" name="srcaddr" onkeyup="this.value=this.value.replace(/[^\d.\/\\\n]/g,'')" onafterpaste="this.value=this.value.replace(/[^\d.]/g,'')" placeholder="eg: 192.168.5.0/255.255.255.0" style="width:500px;height:100px;">{{info.get('srcaddr','')}}</textarea>
                    </div>
		    <div class="modal-body">
			<div class="input-group">
		    	<span class="input-group-addon" style="width:500px">目标地址</span>
			</div>
			<textarea id="dstaddr" name="dstaddr" onkeyup="this.value=this.value.replace(/[^\d.\/\\\n]/g,'')" onafterpaste="this.value=this.value.replace(/[^\d.]/g,'')" placeholder="eg: 192.168.5.0/255.255.255.0" style="width:500px;height:100px;">{{info.get('dstaddr','')}}</textarea>
                    </div>
		    <div class="modal-body">
                        <div class="input-group">
                            <span class="input-group-addon">源端口&emsp;</span>
			    <select style="width:150px" class="form-control" id="sproto" name="sproto">
                               <option 
                                        %if info.get('sproto','')=="TCP": 
                                                selected 
                                        %end 
                                        value="TCP">TCP
                               </option>
                               <option 
                                        %if info.get('sproto','')=="UDP": 
                                                selected 
                                        %end 
                                        value="UDP">UDP
                               </option>
                            </select>
                            <input type="text" style="width:270px" class="form-control" id="" name="sport" onkeyup="this.value=this.value.replace(/[^\d,:]/g,'')" onafterpaste="this.value=this.value.replace(/[^\d]/g,'')" placeholder="eg: 53 or 23,25,100:110" aria-describedby="inputGroupSuccess4Status" value="{{info.get('sport','')}}">
                        </div>
                    </div>
		    <div class="modal-body">
                        <div class="input-group">
                            <span class="input-group-addon">目标端口</span>
			    <select style="width:150px" class="form-control" id="dproto" name="dproto">
                              <option 
                                        %if info.get('dproto','')=="TCP": 
                                                selected 
                                        %end 
                                        value="TCP">TCP
                              </option>
                              <option 
                                        %if info.get('dproto','')=="UDP": 
                                                selected 
                                        %end 
                                        value="UDP">UDP
                              </option>
                            </select>
                            <input type="text" style="width:270px" class="form-control" id="" name="dport" onkeyup="this.value=this.value.replace(/[^\d,:]/g,'')" onafterpaste="this.value=this.value.replace(/[^\d.
]/g,'')" placeholder="eg: 53 or 23,25,100:110" aria-describedby="inputGroupSuccess4Status" value="{{info.get('dport','')}}">
                        </div>
                    </div>
		    <div class="modal-body">
			<div class="input-group">
			<span class="input-group-addon" style="width:80px">执行动作</span>
			<select style="width:420px" class="form-control" id="runaction" name="runaction">
                        <option 
                                        %if info.get('runaction','')=="ACCEPT": 
                                                selected 
                                        %end 
                                        value="ACCEPT">允许
                        </option>
                        <option 
                                        %if info.get('runaction','')=="DROP": 
                                                selected 
                                        %end 
                                        value="DROP">禁止
                        </option>
			</select>
			</div>
		    </div>    
                    <div class="modal-footer">
                        <button type="submit" style="float:left" class="btn btn-primary">保存</button>
			<a id="rego" style="float:left" class="btn btn-primary" href="/utmruleconf">返回</a>
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
