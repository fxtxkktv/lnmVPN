%rebase base position='添加网络对象配置', managetopli="firewall"
<div class="page-body">
    <div class="row">
        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">
            <div class="widget">
                <div class="widget-header bordered-bottom bordered-themesecondary">
                    <i class="widget-icon fa fa-tags themesecondary"></i>
                    <span class="widget-caption themesecondary">添加网络对象配置</span>
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
                            <span class="input-group-addon">对象名称</span>
                            <input type="text" style="width:300px" class="form-control" id="objname" name="objname" aria-describedby="inputGroupSuccess4Status" value="{{info.get('objname','')}}">
                        </div>
            </div>
		    
            <div class="modal-body">
			    <div class="input-group">
		    	    <span class="input-group-addon" style="width:80px">对象类型</span>
			        <select style="width:300px;height:30px;" class="form-control" id="objtype" name="objtype">
                        <option 
                                        %if info.get('objtype','')== "ipset": 
                                                selected 
                                        %end 
                                        value="ipset">IP组
                        </option>
                        <!--option 
                                        %if info.get('objtype','')== "domainset": 
                                                selected 
                                        %end 
                                        value="domainset">域名组
                        </option-->
                     </select>
                </div>
            </div>
            <div class="modal-body">
                <div class="input-group">
                      <span class="input-group-addon">对象内容</span>
                      <textarea class="input-group" id="objtextA" name="objtextA" onkeyup="this.value=this.value.replace(/[^\d.\-\/\\\n]/g,'')" onafterpaste="this.value=this.value.replace(/[^\d.-\/\\\n]/g,'')" placeholder="IP组: IP地址/IP段(一行一个)" style="width:300px;height:100px;resize:vertical;">{{info.get('objtext','')}}</textarea>
                      <textarea class="input-group" id="objtextB" name="objtextB" onkeyup="this.value=this.value.replace(/[^\w\d.\-\/\\\n]/g,'')" onafterpaste="this.value=this.value.replace(/[^\w\d.-\/\\\n]/g,'')" placeholder="域名组: domain.com(一行一个)" style="width:300px;height:100px;resize:vertical;">{{info.get('objtext','')}}</textarea>
                 </div>
		   </div>    
                    <div class="modal-footer">
                        <button type="submit" style="float:left" class="btn btn-primary">保存</button>
			            <a id="rego" style="float:left" class="btn btn-primary" href="/netobjconf">返回</a>
                    </div>
                </div>
              </form>
            </div>
        </div>
    </div>
</div>
<script src="/assets/js/datetime/bootstrap-datepicker.js"></script> 

<script language="JavaScript" type="text/javascript">
$(function() {
  $('#objtype').click(function() {
    if (this.value == 'ipset') {
        $('#objtextB').hide();
	    $('#objtextA').show();
    } else {
	    $('#objtextB').show();
        $('#objtextA').hide();
    }
  });
  $('#objtype').click()
});
</script>
