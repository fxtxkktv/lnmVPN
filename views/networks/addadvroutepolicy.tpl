%rebase base position='添加策略接口', managetopli="networks"

<link rel="stylesheet" href="/assets/bootstrap-select/bootstrap-select.min.css">
<link href="/assets/css/charisma-app.css" rel="stylesheet" type="text/css" />

<div class="page-body">
    <div class="row">
        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">
            <div class="widget">
                <div class="widget-header bordered-bottom bordered-themesecondary">
                    <i class="widget-icon fa fa-tags themesecondary"></i>
                    <span class="widget-caption themesecondary">新增路由出口</span>
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
                <div style="padding:-10px 0px;width=500px;" class="widget-body no-padding">
                  <form action="" method="post">
                    %if msg.get('message'):
                      <span style="color:{{msg.get('color','')}};font-weight:bold;">&emsp;{{msg.get('message','')}}</span>
                    %end
                    <div class="modal-body" style="width:420px;">
                        <div class="input-group">
                            <span class="input-group-addon">策略名称</span>
                            <input type="text" style="width:420px" class="form-control" id="" name="rtname" aria-describedby="inputGroupSuccess4Status" value="{{info.get('rtname','')}}">
                        </div>
                    </div>
                    <div class="modal-body">
                        <div class="input-group">
                          <span class="input-group-addon">路由模式</span>
                          <select style="width:420px" class="form-control" id="sel" name="rttype">
                            <option 
                            %if info.get('rttype','')=='A': 
                                selected 
                            %end 
					        value='A'>单线路由模式
				            </option>
                            <option 
                            %if info.get('rttype','')=='B':
                                selected 
                            %end 
                            value='B'>多线权重模式
                            </option>
                          </select>
                        </div>
                    </div>
		            <div class="modal-body" style="width:520px;">
                        <div class="input-group" id="A">
                            <span class="input-group-addon">选择线路</span>
                            <select type="text" class="form-control selectpicker show-tick" id="ifname" name="ifname" data-live-search="true" data-live-search-placeholder="搜索网络接口">
                              %for name in ifacelist_result:
                                <option 
                                value='{{name.get('ifacename')}}'>{{name.get('ifacename')}}</option>
                              %end
                            </select>
                        </div>
                        <div class="input-group" id="B">
                            <span class="input-group-addon">选择线路</span>
                            <select type="text" class="selectpicker show-tick form-control" multiple id="ifnames" name="ifnames" data-live-search="true" data-live-search-placeholder="搜索网络接口">
                              %for name in ifacelist_result:
                                <option value='{{name.get('ifacename')}}'>{{name.get('ifacename')}}</option>
                              %end
                            </select>
                        </div>
                        <input type="text" id="C" value="{{info.get('iflist','')}}">
                    </div>
                   </div>
                   <div class="modal-footer">
                        <button type="submit" style="float:left" class="btn btn-primary">提交</button>
                        <a id="rego" style="float:left" class="btn btn-primary" href="/advroutepolicy">返回</a>
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
  $("#ifname").selectpicker({noneSelectedText:'搜索网络接口'}); //修改默认显示值
  $("#ifnames").selectpicker({noneSelectedText:'搜索网络接口'}); //修改默认显示值
  $('#sel').click(function() {
    if (this.value == 'A') {
       $('#A').show();
       $('#B').hide();
       $('#C').hide();
       var result = document.getElementById('C').value;
       //console.log(result)
       $('#ifname').selectpicker('val',result);
    } else {
        $('#A').hide();
        $('#B').show();
        $('#C').hide();
        var result = document.getElementById('C').value;
        var arr = result.split(',');
        $('#ifnames').selectpicker('val',arr);
    }
  });
  $('#sel').click();
});
</script>
