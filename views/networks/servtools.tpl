%rebase base position='运维工具', managetopli="networks"
<div class="page-body">
    <div class="row">
        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">
            <div class="widget">
                <div class="widget-header bordered-bottom bordered-themesecondary">
                    <i class="widget-icon fa fa-tags themesecondary"></i>
                    <span class="widget-caption themesecondary">运维工具</span>
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
                            <span class="input-group-addon">工具类型</span>
                            <select style="width:420px" class="form-control" id="sel" name="toolsname">
                    <option 
                    %if info.get('toolsname','')=='PING': 
                        selected 
                    %end 
                    value='PING'>PING检测
                    </option>
                    <option 
                    %if info.get('toolsname','')=='TRACE':
                        selected 
                    %end 
                    value='TRACE'>路由跟踪
                    </option>
                    <option 
                    %if info.get('toolsname','')=='IPLIB': 
                        selected 
                    %end 
                    value='IPLIB'>IP地址库
                    </option>
                    <option 
                    %if info.get('toolsname','')=='IP2PTR': 
                        selected 
                    %end 
                    value='IP2PTR'>IP转PTR格式
                    </option>
                    <option 
                    %if info.get('toolsname','')=='DEVACT': 
                        selected 
                    %end 
                    value='DEVACT'>设备维护
                    </option>
                    
                            </select>
                        </div>
                    </div>
            <div class="modal-body" id="zone01">
              <div class="input-group">
              <span class="input-group-addon">查询内容</span>
              <input type="text" style="width:420px" class="form-control" id="" name="servname" placeholder="请输入主机名或IP地址" aria-describedby="inputGroupSuccess4Status" onkeyup="value=value.replace(/[^\w\.\/]/ig,'')" value="{{info.get('servname','')}}">
              </div>
            </div>
            <div class="modal-body" id="zone02">
              <div class="input-group">
              <span class="input-group-addon">目标动作</span>
              <select style="width:420px" class="form-control" name="servname2">
                <option 
                    %if info.get('devaction','')=='REBOOT': 
                        selected 
                    %end 
                    value='REBOOT'>立即重启设备
                    </option>
                </select>
              </div>
            </div>
                    <div class="modal-body" id="zone03">
                        <div class="input-group">
                          <textarea id="result" name="result"
                          %if info.get('result','') == '':
                             style="width:500px;height:250px;overflow:hidden;background-color:#000000;color:#33FF33;resize:vertical;display:none"
                          %else:
                             style="width:500px;height:250px;overflow:hidden;background-color:#000000;color:#33FF33;resize:vertical;font-family:sans-serif;"
                          %end
                          readonly>{{info.get('result','')}}
                          </textarea>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button id="zone05" type="submit" style="float:left" class="btn btn-primary" >提交</button>
                        <button id="zone06" type="submit" style="float:left" class="btn btn-primary" onClick="return confirm(&quot;确定设备现在重启吗?&quot;)">提交</button>
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
<script language="JavaScript" type="text/javascript">
$(function() {
  $('#sel').click(function() {
    if (this.value == 'DEVACT') {
        $('#zone01').hide();
        $('#zone02').show();
        $('#zone03').hide();
        $('#zone05').hide();
        $('#zone06').show();
    } else {
        $('#zone01').show();
        $('#zone02').hide();
        $('#zone05').show();
        $('#zone06').hide();
    }
  });
  $('#sel').click();
});
</script>
