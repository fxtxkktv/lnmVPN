%rebase base position='更改密码', managetopli="system"
<div class="page-body">
    <div class="row">
        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">
            <div class="widget">
                <div class="widget-header bordered-bottom bordered-themesecondary">
                    <i class="widget-icon fa fa-tags themesecondary"></i>
                    <span class="widget-caption themesecondary">修改密码</span>
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
			%if msg.get('message'):
                            <span style="color:{{msg.get('color','')}};font-weight:bold;">&emsp;{{msg.get('message','')}}</span>
                        %end
                        <div class="input-group">
                            <span class="input-group-addon">旧&nbsp;&nbsp;密&nbsp;&nbsp;码</span>
                            <input type="password" style="width:140px" class="form-control" id="" name="oldpwd" aria-describedby="inputGroupSuccess4Status" value="{{info.get('oldpwd','')}}">
                        </div>
                    </div>
		    <div class="modal-body">
                        <div class="input-group">
                            <span class="input-group-addon">新&nbsp;&nbsp;密&nbsp;&nbsp;码</span>
                            <input type="password" style="width:140px" class="form-control" id="" name="newpwd" aria-describedby="inputGroupSuccess4Status" value="{{info.get('newpwd','')}}">
                        </div>
                    </div>
		    <div class="modal-body">
                        <div class="input-group">
                            <span class="input-group-addon">重复密码</span>
                            <input type="password" style="width:140px" class="form-control" id="" name="newpwds" aria-describedby="inputGroupSuccess4Status" value="{{info.get('newpwds','')}}">
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="submit" style="float:left" class="btn btn-primary">提交</button>
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
