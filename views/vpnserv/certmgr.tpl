%rebase base position='证书管理',managetopli="vpnserv"

<div class="page-body">
    <div class="row">
        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">
            <div class="widget">
                <div class="widget-header bordered-bottom bordered-themesecondary">
                    <i class="widget-icon fa fa-tags themesecondary"></i>
                    <span class="widget-caption themesecondary">证书管理</span>
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
                    <div class="tickets-container">
                        <div class="table-toolbar" style="float:left">
                            <a id="initca" href="javascript:void(0);" class="btn  btn-primary ">
                                <i class="btn-label fa fa-plus"></i>初始化服务证书
                            </a>
			    <a id="addusercerts" href="/addusercerts" class="btn btn-warning shiny">
                                <i class="btn-label fa fa-cog"></i>添加客户端证书
                            </a>
                            <a id="delcert" href="javascript:void(0);" class="btn btn-darkorange">
                                <i class="btn-label fa fa-times"></i>删除&吊销证书
                            </a>
                            %if msg.get('message'):
                                <span style="color:{{msg.get('color','')}};font-weight:bold;">&emsp;{{msg.get('message','')}}</span>
                            %end
                        </div>
                       <table id="myLoadTable" class="table table-bordered table-hover"></table>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<div class="modal fade" id="myModalINITCA" tabindex="-1" role="dialog"  aria-labelledby="myModalLabel" aria-hidden="true">
    <div class="modal-dialog" >
      <div class="modal-content" id="contentDiv">
         <div class="widget-header bordered-bottom bordered-blue ">
           <i class="widget-icon fa fa-pencil themeprimary"></i>
           <span class="widget-caption themeprimary" id="modalTitle">初始化服务证书</span>
        </div>
         <div class="modal-body">
            <div>
            <form id="modalForm">
		<div class="form-group">
                  <label class="control-label" for="inputSuccess1">证书类型：</label>
                  <select id="certtype" style="width:100%;" name="certtype">
                    <option value='server'>服务证书</option>
                 </select>
                </div>
		<div class="form-group">
                  <label class="control-label" for="inputSuccess1">证书名称：</label>
		  <select id="commonname" style="width:100%;" name="commonname">
		     <option value='caserver'>CA+Server</option>
		  </select>
                </div>
                <div class="form-group">
                  <label class="control-label" for="inputSuccess1">颁发机构：</label>
                  <input type="text" class="form-control" id="organization" name="organization" require>
                </div>
                <div class="form-group">
                  <label class="control-label" for="inputSuccess1">有效期：</label>
                  <input type="text" class="form-control" id="expiration" name="expiration" placeholder="有效天数(days)" require>
                </div>
                <br></br>
                <input type="hidden" id="hidInput" value="">
                <button type="button" id="subBtn" class="btn btn-primary  btn-sm">提交</button>
                <button type="button" class="btn btn-warning btn-sm" data-dismiss="modal">关闭</button>
             </form>
            </div>
         </div>
      </div>
   </div>
</div>

<script type="text/javascript">
$(function(){
    /**
    *表格数据
    */
    var editId;        //定义全局操作数据变量
	var isEdit;
    $('#myLoadTable').bootstrapTable({
          method: 'post',
          url: '/api/getcertinfo',
          contentType: "application/json",
          datatype: "json",
          cache: false,
          checkboxHeader: true,
          striped: true,
          pagination: true,
          pageSize: 10,
          pageList: [10,20,50],
          search: true,
          showColumns: true,
          showRefresh: true,
          minimumCountColumns: 2,
          clickToSelect: true,
          smartDisplay: true,
          //sidePagination : "server",
          sortOrder: 'asc',
          sortName: 'id',
          columns: [{
              field: 'bianhao',
              title: 'checkbox',      
              checkbox: true,
          },{
              field: 'xid',
              title: '编号',
              align: 'center',
              valign: 'middle',
              width:25,
              //sortable: false,
	      formatter:function(value,row,index){
                return index+1;
              }
          },{

              field: 'commonname',
              title: '证书名称',
              align: 'center',
              valign: 'middle',
              sortable: false
          },{
              field: 'certtype',
              title: '证书类型',
              align: 'center',
              valign: 'middle',
              sortable: false,
	      formatter: function(value,row,index){
                        if( value == 'caserver' ){
                                return '服务证书';
                        }else{  return '用户证书';
                        }
            }
          },{ 
              field: 'organization',
              title: '颁发机构(策略)',
              align: 'center',
              valign: 'middle',
              sortable: false
          },{ 
              field: 'createdate',
              title: '签发时间',
              align: 'center',
              valign: 'middle',
              sortable: false
          },{
              field: 'expiration',
              title: '有效期(days)',
              align: 'center',
              valign: 'middle',
              sortable: false,
	  },{
              field: '',
              title: '操作',
              align: 'center',
              valign: 'middle',
              width:220,
              formatter:getinfo
          }]
      });

    //定义列操作
    function getinfo(value,row,index){
        eval('rowobj='+JSON.stringify(row));
        //定义编辑按钮样式，只有管理员或自己编辑的任务才有权编辑
        if({{session.get('access',None)}} == '1' || "{{session.get('name',None)}}" == rowobj['userid']){
            var style_download = '<a href="/download/certs/'+rowobj['commonname']+'.zip" class="btn-sm btn-info" >';
        }else{
            var style_download = '<a class="btn-sm btn-info" disabled>';
        }

        return [
            style_download,
                	'<i class="fa fa-download">下载</i>',
            		'</a>',
        ].join('');
    }



    /**
    *初始化服务证书 弹出框
    */

        $('#initca').click(function(){
	var r = confirm("提醒：如果初始化服务证书，将导致所有生成证书被清除，建议备份后再执行该操作，还继续吗？");
        if (r==false){
              $('myLoadTable').bootstrapTable('refresh');
              return false;
        }
        $('#modalTitle').html('初始化服务证书');
        $('#hidInput').val('0');
        $('#myModalINITCA').modal('show');
        $('#modalForm')[0].reset();
        isEdit = 1;
    });

    /**
    *提交按钮操作
    */
    $("#subBtn").click(function(){
           var certtype = $('#certtype').val();
           var commonname = $('#commonname').val();
           var organization = $('#organization').val();
           var expiration = $('#expiration').val();
           var postUrl;
           if(isEdit==1){
                postUrl = "/initca";           //初始化证书
           }

           $.post(postUrl,{certtype:certtype,commonname:commonname,organization:organization,expiration:expiration},function(data){
                  if(data==0){
                    $('#myModalINITCA').modal('hide');
		    $('#myModalUSER').modal('hide');
                    $('#myLoadTable').bootstrapTable('refresh');
                    message.message_show(200,200,'成功','操作成功');   
                  }else if(data==-1){
                    message.message_show(200,200,'失败','操作失败');
                  }else{
                        message.message_show(200,200,'失败','填写选项不符合要求');
                        //console.log(data);return false;
                }
            },'html');
    });
	
        /**
        *删除按钮操作
        */        
    $('#delcert').popover({
                html: true,
                container: 'body',
                content : "<h3 class='btn btn-danger'>请选择要删除的记录</h3>",
                animation: false,
                placement : "top"
        }).on('click',function(){
            var res = $("#myLoadTable").bootstrapTable('getSelections');
            var str = '';
            if(res.length <= 0){
                $(this).popover("show");
                setTimeout("$('#delcert').popover('hide')",1000)
            }else{
                var r = confirm("提醒：如果选项中存在CA或Server类证书，将导致所有生成证书被清除，建议备份后再删除，要删除吗？");
                if (r==false){
                	$('myLoadTable').bootstrapTable('refresh');
                	console.log(data);return false;
                }
                $(this).popover("hide");
                for(i in res){
                    str += res[i]['id']+',';
                }
                $.post('/delcert',{str:str},function(data){
                    if(data==0){
                        message.message_show(200,200,'删除成功',res.length+'条记录被删除');
                        $('#myLoadTable').bootstrapTable('refresh');
                    }else{
                        message.message_show(200,200,'失败','删除失败');
                    }
                },'html');  
                
            }
        });
})
</script>
