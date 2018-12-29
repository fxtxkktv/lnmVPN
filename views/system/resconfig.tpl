%rebase base position='资源监控配置', managetopli="system"
<div class="page-body">
    <div class="row">
        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">
            <div class="widget">
                <div class="widget-header bordered-bottom bordered-themesecondary">
                    <i class="widget-icon fa fa-tags themesecondary"></i>
                    <span class="widget-caption themesecondary">资源监控配置</span>
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
                    %if msg.get('message'):
                      <span style="color:{{msg.get('color','')}};font-weight:bold;">&emsp;{{msg.get('message','')}}</span>
                    %end
		    <div class="modal-body">
                        <div class="input-group">
                            <span class="input-group-addon">资源监控开关</span>
                            <select style="width:100px" class="form-control" name="ResState">
                                        <option 
                                        %if info.get('ResState','') == 'False':
                                                selected
                                        %end 
                                        value='False'>关闭</option>
                                        <option
                                        %if info.get('ResState','') == 'True':
                                                selected
                                        %end 
                                                value='True'>开启
                                        </option>
                            </select>
                        </div>
                    </div>
		    <div class="modal-body">
                      <div class="input-group">
                        <span class="input-group-addon">默认显示天数</span>
                        <input type="text" style="width:100px" class="form-control" id="" name="ResSaveDay" onkeyup="this.value=this.value.replace(/[^\d]/g,'')" onafterpaste="this.value=this.value.replace(/[^\d]/g,'')" aria-describedby="inputGroupSuccess4Status" value="{{info.get('ResSaveDay','')}}">
                        </div>
                    </div>
		    <div class="modal-body">
                      <div class="input-group">
                        <span class="input-group-addon">数据保存天数</span>
                        <input type="text" style="width:100px" class="form-control" id="" name="visitDay" onkeyup="this.value=this.value.replace(/[^\d]/g,'')" onafterpaste="this.value=this.value.replace(/[^\d]/g,'')" aria-describedby="inputGroupSuccess4Status" value="{{info.get('visitDay','')}}">
                        </div>
                    </div>
		    <div class="modal-body">
                    <div class="input-group">
                      <span class="input-group-addon">数据获取间隔</span>
                      <input type="text" style="width:100px" class="form-control" id="" name="ResInv" onkeyup="this.value=this.value.replace(/[^\d]/g,'')" onafterpaste="this.value=this.value.replace(/[^\d]/g,'')" aria-describedby="inputGroupSuccess4Status" value="{{info.get('ResInv','')}}">
                    </div>
                    <div class="modal-body">
                        <span style="color:#666666;" id="signc">备注<br/>1.数据获取间隔越大，占用系统资源越小，建议最小值为60s<br/>2.当配置过低时，可考虑关闭该功能</span>
                    </div>
                    <div class="modal-footer">
                        <button type="submit" style="float:left" class="btn btn-primary">保存</button>
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
