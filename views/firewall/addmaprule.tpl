%rebase base position='添加MAP配置', managetopli="firewall"

<link rel="stylesheet" href="/assets/bootstrap-select/bootstrap-select.min.css">
<link href="/assets/css/charisma-app.css" rel="stylesheet" type="text/css" />

<div class="page-body">
    <div class="row">
        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">
            <div class="widget">
                <div class="widget-header bordered-bottom bordered-themesecondary">
                    <i class="widget-icon fa fa-tags themesecondary"></i>
                    <span class="widget-caption themesecondary">添加MAP配置</span>
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
                         <input type="text" style="width:210px" class="form-control" id="" placeholder="优先级" name="pronum" aria-describedby="inputGroupSuccess4Status" value="{{info.get('pronum','')}}">
                         <input type="text" style="width:210px" class="form-control" id="" placeholder="规则名称" name="rulename" aria-describedby="inputGroupSuccess4Status" value="{{info.get('rulename','')}}">
                        </div>
                    </div>
		    
		    <div class="modal-body">
                    <div class="input-group">
                        <span class="input-group-addon">外部地址</span>
                        <select style="width:210px;" class="form-control" id="wantype" name="wantype">
                        <option 
                                        %if info.get('wantype','')== 1: 
                                                selected 
                                        %end 
                                        value="1">接口模式
                        </option>
                        <option 
                                        %if info.get('wantype','')== 0: 
                                                selected 
                                        %end 
                                        value="0">IP模式
                        </option>
                        </select>
                         <select style="width:210px" class="form-control" id="waniface" name="waniface">
                        %for infos in ifacelist_result:
                            <option
                            %if info.get('waniface','')==infos.get('ifacename','') : 
                                selected 
                            %end 
                            value='{{infos.get('ifacename','')}}'>{{infos.get('ifacename','')}}
                            </option>
                        %end
                        </select>
                        <input type="text" style="width:210px" class="form-control" id="wanaddr" name="wanaddr" onkeyup="this.value=this.value.replace(/[^\d.]/g,'')" onafterpaste="this.value=this.value.replace(/[^\d.]/g,'')" readonly="readonly" aria-describedby="inputGroupSuccess4Status" value="{{info.get('wanaddr','')}}">
                    </div>
            </div>
		    <div class="modal-body">
			    <div class="input-group">
		    	    <span class="input-group-addon">外部端口</span>
                    <input type="text" style="width:420px" class="form-control" id="wanport" name="wanport" onkeyup="this.value=this.value.replace(/[^\d,:]/g,'')" onafterpaste="this.value=this.value.replace(/[^\d,:]/g,'')" aria-describedby="inputGroupSuccess4Status" value="{{info.get('wanport','')}}">
			    </div>
            </div>
		    <div class="modal-body">
			    <div class="input-group">
			        <span class="input-group-addon">内部地址</span>
			        <input type="text" style="width:420px" class="form-control" id="intaddr" name="intaddr" onkeyup="this.value=this.value.replace(/[^\d.]/g,'')" onafterpaste="this.value=this.value.replace(/[^\d.]/g,'')" aria-describedby="inputGroupSuccess4Status" value="{{info.get('intaddr','')}}">
			    </div>
		    </div>
            <div class="modal-body">
                <div class="input-group">
                    <span class="input-group-addon">内部端口</span>
                    <input type="text" style="width:420px" class="form-control" id="intport" name="intport" readonly="readonly" aria-describedby="inputGroupSuccess4Status" value="{{info.get('intport','')}}">
                </div>
            </div>  
            <div class="modal-body" style="width:520px;">
                    <div class="input-group">
                         <span class="input-group-addon">协议类型</span>
                         <select type="text" style="width:420px" class="selectpicker show-tick form-control" multiple id="prototype" name="prototype" data-live-search="true" data-live-search-placeholder="搜索">
                             <option value='TCP'>TCP类型</option>
                             <option value='UDP'>UDP类型</option>
                             <option value='LAN'>局域网映射</option>
                         </select>
                    </div>
                    <input type="text" id="C" value="{{info.get('proto','')}}">
            </div>  
                    <div class="modal-footer">
                        <button type="submit" style="float:left" class="btn btn-primary">保存</button>
			            <a id="rego" style="float:left" class="btn btn-primary" href="/mapruleconf">返回</a>
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
  $("#prototype").selectpicker({noneSelectedText:'搜索'}); //修改默认显示值
  $('#wantype').click(function() {
    if (this.value == "1" ) {
        $('#waniface').show();
        $('#wanaddr').hide();
        $('#C').hide();
        document.getElementById("wanaddr").readOnly=true ;
    } else {
        $('#waniface').hide();
        $('#wanaddr').show();
        $('#C').hide();
        document.getElementById("wanaddr").readOnly=false ;
    }
  });
  $('#intport').click(function() {
    //console.log(this.value.search(":"))
    var str = document.getElementById("wanport").value
    if (str.search(",|:") != "-1" ) {
        document.getElementById("intport").readOnly=true ;
        $(" #intport").val("");
    } else {
        document.getElementById("intport").readOnly=false ;
    }
  });
  $('#wantype').click();
  $('#wanport').click();
  var result = document.getElementById('C').value;
  var arr = result.split(',');
  $('#prototype').selectpicker('val',arr);
});
</script>
