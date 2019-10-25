%rebase base position='添加NAT配置', managetopli="firewall"

<link rel="stylesheet" href="/assets/bootstrap-select/bootstrap-select.min.css">
<link href="/assets/css/charisma-app.css" rel="stylesheet" type="text/css" />

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
                            <input type="text" style="width:210px" class="form-control" id="" name="rulename" aria-describedby="inputGroupSuccess4Status" value="{{info.get('rulename','')}}">
                            <input type="text" style="width:210px" class="form-control" id="" placeholder="优先级" name="pronum" aria-describedby="inputGroupSuccess4Status" value="{{info.get('pronum','')}}">
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
            <div class="modal-body" id="p_g">
                 <span style="color:red;">备注: 当源或目的对象均为任意地址时<strong>&nbsp;建议使用源地址伪装MASQ，SNAT容易造成高级路由异常.&nbsp;</strong></span>
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
<script src="/assets/bootstrap-select/bootstrap-select.min.js"></script>
<script language="JavaScript" type="text/javascript">
$(function() {
  $("#srcaddr").selectpicker({noneSelectedText:'搜索网络对象'}); //修改默认显示值
  $("#dstaddr").selectpicker({noneSelectedText:'搜索网络对象'}); //修改默认显示值
  $('#srcmatch').click(function() {
    if (this.value == 2) {
        console.log(this.value)
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
  $('#srcmatch').click() ;
  $('#dstmatch').click() ;
  $('#runaction').click(function() {
    if (this.value == 'MASQ') {
        $('#runobject').hide();
	$('#runobject2').show();
    } else {
	$('#runobject').show();
        $('#runobject2').hide();
    }
  });
  $('#runaction').click();
  console.log({{info.get('srcaddr',None)}})
  if ( "{{info.get('srcaddr',None)}}" != "all" ) {
    $('#srcaddr').selectpicker('val',"{{info.get('srcaddr',None)}}");
  };
  var result2="{{info.get('dstaddr',None)}}";
  if ( "{{info.get('dstaddr',None)}}" != "all" ) {
    $('#dstaddr').selectpicker('val',"{{info.get('dstaddr',None)}}");
  };
});
</script>
