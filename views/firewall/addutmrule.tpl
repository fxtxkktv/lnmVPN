%rebase base position='添加UTM配置', managetopli="firewall"

<link rel="stylesheet" href="/assets/bootstrap-select/bootstrap-select.min.css">
<link href="/assets/css/charisma-app.css" rel="stylesheet" type="text/css" />

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
		    <div class="modal-body" style="width:520px">
                <div class="input-group">
                     <span class="input-group-addon" >源对象&emsp;</span>
                     <select class="form-control" id="srcmatch" name="srcmatch">
                        <option 
                                        %if info.get('srcmatch','')== 2: 
                                                selected 
                                        %end 
                                        value="2">任意地址
                        </option>
                        <option 
                                        %if info.get('srcmatch','')== 1: 
                                                selected 
                                        %end 
                                        value="1">匹配
                        </option>
                        <option 
                                        %if info.get('srcmatch','')== 0: 
                                                selected 
                                        %end 
                                        value="0">非匹配
                        </option>
                     </select>
                     <select type="text" class="selectpicker show-tick form-control" id="srcaddr" name="srcaddr" data-live-search="true" data-live-search-placeholder="搜索网络对象">
                              %for name in setlist:
                                <option value='{{name.get('id')}}'>{{name.get('objname')}}</option>
                              %end
                     </select>
                </div>
            </div>
		    <div class="modal-body" style="width:520px">
			    <div class="input-group" >
		    	    <span class="input-group-addon">目的对象</span>
                    <select class="form-control" id="dstmatch" name="dstmatch">
                        <option 
                                        %if info.get('dstmatch','')== 2: 
                                                selected 
                                        %end 
                                        value="2">任意地址
                        </option>
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
                    <select type="text" class="selectpicker show-tick form-control" id="dstaddr" name="dstaddr" data-live-search="true" data-live-search-placeholder="搜索网络对象">
                            %for name in setlist:
                                <option value='{{name.get('id')}}'>{{name.get('objname')}}</option>
                            %end
                    </select>
                </div>
            </div>
            <div class="modal-body">
                        <div class="input-group">
                            <span class="input-group-addon">网络协议</span>
                            <select style="width:420px" class="form-control" id="netproto" name="netproto">
                               <option 
                                        %if info.get('sport','')== "ALL": 
                                                selected 
                                        %end 
                                        value="ALL">不限
                               </option>
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
                        </div>
            </div>
		    <div class="modal-body">
                        <div class="input-group">
                            <span class="input-group-addon">源端口&emsp;</span>
                            <input type="text" style="width:420px" class="form-control" id="sport" name="sport" onkeyup="this.value=this.value.replace(/[^\d,:]/g,'')" onafterpaste="this.value=this.value.replace(/[^\d]/g,'')" placeholder="eg: 53 or 23,25,100:110" aria-describedby="inputGroupSuccess4Status" value="{{info.get('sport','')}}">
                        </div>
                    </div>
		    <div class="modal-body">
                        <div class="input-group">
                            <span class="input-group-addon">目标端口</span>
                            <input type="text" style="width:420px" class="form-control" id="dport" name="dport" onkeyup="this.value=this.value.replace(/[^\d,:]/g,'')" onafterpaste="this.value=this.value.replace(/[^\d.]/g,'')" placeholder="eg: 53 or 23,25,100:110" aria-describedby="inputGroupSuccess4Status" value="{{info.get('dport','')}}">
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
<script src="/assets/bootstrap-select/bootstrap-select.min.js"></script>
<script language="JavaScript" type="text/javascript">
$(function() {
  $("#srcaddr").selectpicker({noneSelectedText:'搜索网络对象'}); //修改默认显示值
  $("#dstaddr").selectpicker({noneSelectedText:'搜索网络对象'}); //修改默认显示值
  $('#srcmatch').click(function() {
    if (this.value == 2) {
        $('#srcaddr').selectpicker('hide');
    } else {
        $('#srcaddr').selectpicker('show');
    }
  });
  $('#dstmatch').click(function() {
    if (this.value == 2) {
        $('#dstaddr').selectpicker('hide');
    } else {
        $('#dstaddr').selectpicker('show');
    }
  });
  $('#netproto').click(function() {
    if (this.value == "ALL") {
        document.getElementById("sport").readOnly=true ;
        document.getElementById("dport").readOnly=true ;
    } else {
        document.getElementById("sport").readOnly=false ;
        document.getElementById("dport").readOnly=false ;
    }
  });
  $('#srcmatch').click() ;
  $('#dstmatch').click() ;
  $('#netproto').click() ;
  if ( "{{info.get('srcaddr',None)}}" != "all" ) {
    $('#srcaddr').selectpicker('val',"{{info.get('srcaddr',None)}}");
  };
  var result2="{{info.get('dstaddr',None)}}";
  if ( "{{info.get('dstaddr',None)}}" != "all" ) {
    $('#dstaddr').selectpicker('val',"{{info.get('dstaddr',None)}}");
  };
});
</script>
