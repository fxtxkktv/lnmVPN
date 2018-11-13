%rebase base position='文件上传页面', managetopli="system"
<div class="page-body">
    <div class="row">
        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">
            <div class="widget">
                <div class="widget-header bordered-bottom bordered-themesecondary">
                    <i class="widget-icon fa fa-tags themesecondary"></i>
                    <span class="widget-caption themesecondary">文件上传</span>
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
                  <form action="/uploadfile" method="post" enctype="multipart/form-data">
		    %if msg.get('message'):
                        <span style="color:{{msg.get('color','')}};font-weight:bold;">&emsp;{{msg.get('message','')}}</span>
                    %end
		   <div class="modal-body">
                        <div class="input-group">
                             <input type="file" name="upload" />
                        </div>
                  </div>
		  <div class="modal-footer">
			<button type="submit" style="float:left" class="btn btn-primary">保存</button>
                        <a id="rego" style="float:left" class="btn btn-primary" href="#" onclick="javascript:history.back(-1);">返回</a>
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
$(function(){
  $('#sel').click(function() {
    if (this.value == '0') {
	$('#vpnuser').hide();
	$('#vpnpass').hide();
	$('#signa').hide();
	$('#cainfo').show();
	$('#certinfo').show();
	$('#signb').show();
	$('#signc').show();
        //document.getElementById("selInput").readOnly=false ;
        /*显示 $('#selInput').show(); */
    } else {
	$('#cainfo').hide();
	$('#certinfo').hide();
	$('#signb').hide();
	$('#signc').hide();
	$('#signa').show();
	$('#vpnuser').show();
        $('#vpnpass').show();
        //document.getElementById("selInput").readOnly=true ;
        /*隐藏 $('#selInput').hide(); */
    }
 });
 $('#sel').click();
});
</script>
