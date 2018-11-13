%rebase base position='修改用户', managetopli="vpnserv"
<div class="page-body">
    <div class="row">
        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">
            <div class="widget">
                <div class="widget-header bordered-bottom bordered-themesecondary">
                    <i class="widget-icon fa fa-tags themesecondary"></i>
                    <span class="widget-caption themesecondary">修改用户</span>
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
		<form id="modalForm" action="" method="post">
		<div class="modal-body">
                        <div class="input-group">
                            <span class="input-group-addon">账号: </span>
                            <input type="text" style="width:420px" class="form-control" id="" name="username" aria-describedby="inputGroupSuccess4Status" value="{{info.get('username','')}}">
                        </div>
                </div>
		<div class="modal-body">
                        <div class="input-group">
                            <span class="input-group-addon">密码: </span>
                            <input type="password" style="width:420px" class="form-control" id="passwd" name="passwd" aria-describedby="inputGroupSuccess4Status" value="{{info.get('passwd','')}}">
                        </div>
                </div>

                <div class="modal-body">
			 <div class="input-group">
				<span class="input-group-addon">策略: </span>
                  		<select id="policy" style="width:420px;" name="policy">
                    		<option value=''>请选择策略</option>
                    		%for name in plylist_result:
                        		<option 
                                	%if name.get('id','') == info.get('policy',''): 
                                   	 selected 
                               		%end
                                	value='{{name.get('id','')}}'>{{name.get('name','')}}
                        		</option>
                    		%end
                 		</select>
			</div>
                </div>
		<div class="modal-body">
			<div class="input-group">
			   <span class="input-group-addon">权限: </span>
                  		<select id="access" style="width:420px;" name="access">
				%if info.get('access','') == 0:
                    			<option value='0'>普通</option>
				%else :
                    			<option value='1'>管理</option>
				%end
                 		</select>
			</div>
		</div>
		<div class="modal-body">
		  <span class="input-group-addon" style="width:480px">备注信息: </span>
                  <textarea id="comment" name="comment" style="width:480px;" >{{info.get('comment','')}}</textarea>
                </div>
		<div class="modal-footer">
                  <button type="submit" style="float:left" class="btn btn-primary">提交</button>
		</div>
             </form>
          </div>
        </div>
    </div>
</div>
<script src="/assets/js/datetime/bootstrap-datepicker.js"></script> 
<script charset="utf-8" src="/assets/kindeditor/kindeditor.js"></script>
<script charset="utf-8" src="/assets/kindeditor/lang/zh_CN.js"></script>
