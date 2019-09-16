%rebase base position='添加高级路由', managetopli="networks"

<link rel="stylesheet" href="/assets/bootstrap-select/bootstrap-select.min.css">
<link href="/assets/css/charisma-app.css" rel="stylesheet" type="text/css" />

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
            <div class="modal-body" style="width:520px">
                <div class="input-group" >
                    <span class="input-group-addon">源对象&emsp;</span>
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
                            <span class="input-group-addon">优先级&emsp;</span>
                            <input type="text" style="width:420px" class="form-control" id="pronum" name="pronum" aria-describedby="inputGroupSuccess4Status" onkeyup="if(this.value.length==1){this.value=this.value.replace(/[^1-9]/g,'')}else{this.value=this.value.replace(/\D/g,'')}" onafterpaste="if(this.value.length==1){this.value=this.value.replace(/[^1-9]/g,'')}else{this.value=this.value.replace(/\D/g,'')}" placeholder="该数字必须满足: 100<x<32765" value="{{info.get('pronum','')}}">
                        </div>
            </div>
            <div class="modal-body">
                        <div class="input-group">
                            <span class="input-group-addon">时间控制</span>
                            <input type="time" style="width:210px" class="form-control" id="starttime" name="starttime" onclick="mytime()" aria-describedby="inputGroupSuccess4Status" 
                            %if info.get('starttime',''): 
                                value="{{info.get('starttime','')}}"
                            %else :
                                value="00:00"
                            %end 
                            >
                            <input type="time" style="width:210px" class="form-control" id="stoptime" name="stoptime" onclick="mytime()" aria-describedby="inputGroupSuccess4Status"
                            %if info.get('stoptime',''): 
                                value="{{info.get('stoptime','')}}"
                            %else :
                                value="23:59"
                            %end 
                            value="{{info.get('stoptime','')}}">
                        </div>
            </div>
		    <div class="modal-body">
		      <div class="input-group">
			  <span class="input-group-addon">指定策略</span>
			  <select style="width:280px" class="form-control" name="ifacename">
                                        <option value=''>请选择出口策略</option>
                                        %for infos in iflist:
                                             <option
                                                %if info.get('iface','') == infos.get('attr',''): 
                                                    selected 
                                                %end 
                                                value='{{infos.get('attr','')}}'> {{infos.get('rtname','')}}
                                             </option>
                                        %end
              </select>
              <a style="width:140px;" class="form-control" href='/advroutepolicy'><font color="red">高级策略管理</font></a>
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
<script src="/assets/bootstrap-select/bootstrap-select.min.js"></script>
<script language="JavaScript" type="text/javascript">
$(function() {
  $("#srcaddr").selectpicker({noneSelectedText:'搜索网络对象'}); //修改默认显示值
  $("#dstaddr").selectpicker({noneSelectedText:'搜索网络对象'}); //修改默认显示值
  $('#srcmatch').click(function() {
    if (this.value == 2) {
        $('#srcaddr').selectpicker('hide');
    } else {
        document.getElementById("starttime").readOnly=false ;
        document.getElementById("stoptime").readOnly=false ;
        $('#srcaddr').selectpicker('show');
    }
  });
  $('#dstmatch').click(function() {
    if (this.value == 2) {
        $('#dstaddr').selectpicker('hide');
    } else {
        document.getElementById("starttime").readOnly=false ;
        document.getElementById("stoptime").readOnly=false ;
        $('#dstaddr').selectpicker('show');
    }
  });
  $('#srcmatch').click() ;
  $('#dstmatch').click() ;
  if ( "{{info.get('srcaddr',None)}}" != "all" ) {
    $('#srcaddr').selectpicker('val',"{{info.get('srcaddr',None)}}");
  };
  var result2="{{info.get('dstaddr',None)}}";
  if ( "{{info.get('dstaddr',None)}}" != "all" ) {
    $('#dstaddr').selectpicker('val',"{{info.get('dstaddr',None)}}");
  };
});

function mytime(){
  //console.log($('#dstmatch option:selected').val())
  if ($('#srcmatch option:selected').val() == 2  && $('#dstmatch option:selected').val() == 2){
     document.getElementById("starttime").readOnly=true ;
     document.getElementById("stoptime").readOnly=true ;
  } else {
     document.getElementById("starttime").readOnly=false ;
     document.getElementById("stoptime").readOnly=false ;
  }
};
</script>
