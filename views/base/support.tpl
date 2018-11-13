%rebase base position='问题反馈', managetopli="help"
<div class="page-body">
    <div class="row">
        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">
            <div class="widget">
                <div class="widget-header bordered-bottom bordered-themesecondary">
                    <i class="widget-icon fa fa-tags themesecondary"></i>
                    <span class="widget-caption themesecondary">问题反馈</span>
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
		    <div class="modal-footer">
                        <a style="float:left" href="mailto:{{session.get('admemail','')}}" >使用本地客户端编辑</a>
                    </div>
		    <div class="modal-body">
                        <div class="input-group">
                           <span class="input-group-addon">主题&emsp;&emsp;</span>
                           <input type="text" style="width:590px" class="form-control" id="" name="subject" placeholder="请输入" aria-describedby="inputGroupSuccess4Status" value="">
                        </div>
                    </div>
		    <div class="modal-body">                        
			<div class="form-group">
                            <textarea id="editor_id" name="content" style="width:670px;height:320px;"></textarea>
                        </div>                    
		    </div>
                    <div class="modal-footer">
                        <button type="submit" style="float:left" class="btn btn-primary">发送</button>
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
<script>    
	$('.date-picker').datepicker();     //时间插件    
	KindEditor.ready(function(K) {
            		window.editor = K.create('#editor_id');    
		});
</script>
