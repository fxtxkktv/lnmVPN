%rebase base position='VPN服务主页', managetopli="vpnserv"
<div class="page-body">
    <div class="row">
        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">
            <div class="widget">
                <div class="widget-header bordered-bottom bordered-themesecondary">
                    <i class="widget-icon fa fa-tags themesecondary"></i>
                    <span class="widget-caption themesecondary">服务配置</span>
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
			    <a id="addservconf" href="/addservconf" class="btn btn-primary ">
                                <i class="btn-label fa fa-plus"></i>添加服务端配置
                            </a>
			    <a id="addclientconf" href="/addclientconf" class="btn btn-warning shiny">
                                <i class="btn-label fa fa-cog"></i>客户端配置
                            </a>
			    <a id="showservlog" href="/showservlog" class="btn btn-darkorange">
                                <i class="btn-label fa fa-print"></i>查看服务日志
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
<script type="text/javascript">
$(function(){
    /**
    *表格数据
    */
    var editId;        //定义全局操作数据变量
	var isEdit;
    $('#myLoadTable').bootstrapTable({
          method: 'post',
          url: '/api/getvpnservinfo',
          contentType: "application/json",
          datatype: "json",
          cache: false,
          checkboxHeader: true,
          striped: true,
          pagination: true,
          pageSize: 15,
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
              field: 'authtype',
              title: '验证方式',
              align: 'center',
              valign: 'middle',
              sortable: false,
	      formatter: function(value,row,index){
                        if( value == '0' ){
                                return '证书认证';
                        }
			else if( value == '1' ){
				return '密码认证';
			}
			else{  return '证书+密码认证';
                        }
            }
          },{
	      field: 'servinfo',
              title: '监听配置',
              align: 'center',
              valign: 'middle',
              sortable: false
	  },{
              field: 'virinfo',
              title: '虚拟网段',
              align: 'center',
              valign: 'middle',
              sortable: false
          },{
              field: 'comp',
              title: '启用压缩',
              align: 'center',
	      valign: 'middle',
              sortable: false,
	      formatter: function(value,row,index){
                        if( value == '0' ){
                                return '启用';
                        }else{  return '禁用';
                        }
            }
          },{
              field: 'cisco',
              title: 'AnyConnect支持',
              align: 'center',
              valign: 'middle',
              sortable: false,
	      formatter: function(value,row,index){
                        if( value == '0' ){
                                return '启用';
                        }else{  return '禁用';
                        }
            }
          },{
	      field: 'workstatus',
              title: '工作状态',
              align: 'center',
              valign: 'middle',
              sortable: false,
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
        //定义编辑按钮样式，只有管理员或自己编辑的任务才有权编辑
        if({{session.get('access',None)}} == '1' || "{{session.get('name',None)}}" == rowobj['userid']){
            var style_edit = '<a href="/editvpnservconf/'+rowobj['id']+'" class="btn-sm btn-info" >';
        }else{
            var style_edit = '<a class="btn-sm btn-info" disabled>';
        }
        //定义删除按钮样式，只有管理员或自己编辑的任务才有权删除
        if({{session.get('access',None)}} == '1' || "{{session.get('name',None)}}" == rowobj['userid']){
            var style_del = '&nbsp;<a id="delconf" href="/delvpnservconf/'+rowobj['id']+'" class="btn-sm btn-danger" onClick="return confirm(&quot;确定删除?&quot;)">';
        }else{
            var style_del = '&nbsp;<a class="btn-sm btn-danger" disabled>';
        }

        return [
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
