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
                            <a id="addvnode" href="/addclientconf" class="btn  btn-primary ">
                                <i class="btn-label fa fa-plus"></i>新增节点
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
           <span class="widget-caption themeprimary" id="modalTitle">新增节点</span>
        </div>
         <div class="modal-body">
            <div>
            <form id="modalForm">
		        <div class="form-group">
                  <label class="control-label" for="inputSuccess1">证书类型：</label>
                  <select id="certtype" style="width:100%;" name="certtype">
                    <option value='server'>CA服务证书</option>
                 </select>
                </div>
		        <div class="form-group">
                  <label class="control-label" for="inputSuccess1">服务名称：</label>
                  <input type="text" class="form-control" id="servname" name="servname" placeholder="完整主机域名" require>
                  <!--select id="commonname" style="width:100%;" name="commonname">
                    <option value='caserver'>CA+Server</option>
                  </select-->
                </div>
                <div class="form-group">
                  <label class="control-label" for="inputSuccess1">颁发机构：</label>
                  <input type="text" class="form-control" id="organization" name="organization" onkeyup="value=value.replace(/[^\w\/]/ig,'')" require>
                </div>
                <div class="form-group">
                  <label class="control-label" for="inputSuccess1">有效期：</label>
                  <input type="text" class="form-control" id="expiration" name="expiration" onkeyup="this.value=this.value.replace(/\D/g,'')" placeholder="有效天数(days)" require>
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
          url: '/api/getvnodelist',
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

              field: 'vnodename',
              title: '节点名称',
              align: 'center',
              valign: 'middle',
              sortable: false
          },{
              field: 'authtype',
              title: '认证方式',
              align: 'center',
              valign: 'middle',
              sortable: false,
	          formatter: function(value,row,index){
                        if( value == '1' ){
                                return '密码验证';
                        }else{  return '证书验证';
                        }
            }
          },{ 
              field: 'vconn',
              title: '服务器信息',
              align: 'center',
              valign: 'middle',
              sortable: false
          },{ 
              field: 'chkdtls',
              title: 'DTLS连接',
              align: 'center',
              valign: 'middle',
              sortable: false
          },{
              field: 'vconninfo',
              title: '连接信息',
              align: 'center',
              valign: 'middle',
              sortable: false,
              visible: false,
          },{
              field: 'tunid',
              title: '设备编号',
              align: 'center',
              valign: 'middle',
              sortable: false,
              visible: false,
          },{
              field: 'vmtu',
              title: 'MTU值',
              align: 'center',
              valign: 'middle',
              sortable: false,
          },{
              field: 'chkconn',
              title: ' 连接检测',
              align: 'center',
              valign: 'middle',
              sortable: false,
          },{
              field: 'status',
              title: ' 服务状态',
              align: 'center',
              valign: 'middle',
              sortable: false,
              width:25,
              formatter: function(value,row,index){
                if( value == '1' ){
                        return '<img  src="/assets/img/run_1.gif" class="img-rounded" >';
                }else{  return '<img  src="/assets/img/run_0.gif" class="img-rounded" >';
                }
            }
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
        //定义显示启用停用按钮，只有管理员或自己编辑的任务才有权操作
        if({{session.get('access',None)}} == '1' || "{{session.get('name',None)}}" == rowobj['userid']){
            if(rowobj['status'] == '1'){
               var style_action = '<a href="/chgstatus/vnodedisable/'+rowobj['tunid']+'" class="btn-sm btn-success" >';
            }else{
               var style_action = '<a href="/chgstatus/vnodeactive/'+rowobj['tunid']+'" class="btn-sm btn-danger active" >';
            }
        }else{
            var style_action = '<a class="btn-sm btn-info" disabled>';
        }
        //定义编辑按钮样式，只有管理员或自己编辑的任务才有权编辑
        if({{session.get('access',None)}} == '1' || "{{session.get('name',None)}}" == rowobj['userid']){
            var style_edit = '&nbsp;<a href="/editcltconf/'+rowobj['tunid']+'" class="btn-sm btn-info" >';
        }else{
            var style_edit = '&nbsp;<a class="btn-sm btn-info" disabled>';
        }
        //定义删除按钮样式，只有管理员或自己编辑的任务才有权删除
        if({{session.get('access',None)}} == '1' || "{{session.get('name',None)}}" == rowobj['userid']){
            var style_del = '&nbsp;<a href="/delcltconf/'+rowobj['tunid']+'" class="btn-sm btn-danger" onClick="return confirm(&quot;确定删除?&quot;)">';
        }else{
            var style_del = '&nbsp;<a class="btn-sm btn-danger" disabled>';
        }

        return [
            style_action,
                '<i class="fa fa-power-off"> 开关</i>',
            '</a>', 

            style_edit,
                '<i class="fa fa-edit"> 编辑</i>',
            '</a>',

            style_del,
                '<i class="fa fa-times"> 删除</i>',
            '</a>'
        ].join('');
    }
})
</script>
