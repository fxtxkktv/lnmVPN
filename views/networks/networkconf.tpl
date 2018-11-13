%rebase base position='网络配置', managetopli="networks"
<div class="page-body">
    <div class="row">
        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">
            <div class="widget">
                <div class="widget-header bordered-bottom bordered-themesecondary">
                    <i class="widget-icon fa fa-tags themesecondary"></i>
                    <span class="widget-caption themesecondary">网络配置</span>
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
                            <a id="addinterface" href="/addinterface" class="btn btn-primary ">
                                <i class="btn-label fa fa-plus"></i>添加接口
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
          url: '/api/getifaceinfo',
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
              field: 'ifacename',
              title: '接口名称',
              align: 'center',
              valign: 'middle',
              sortable: false,
          },{
              field: 'ifacetype',
              title: '接入方式',
              align: 'center',
              valign: 'middle',
              sortable: false
          },{
              field: 'ipaddr',
              title: 'IP地址',
              align: 'center',
	      valign: 'middle',
              sortable: false
          },{
              field: 'netmask',
              title: '子网掩码',
              align: 'center',
              valign: 'middle',
              sortable: false
          },{
	      field: 'rxdata',
              title: '发送数据(MB)',
              align: 'center',
              valign: 'middle',
              sortable: false
	  },{
	      field: 'txdata',
              title: '接收数据(MB)',
              align: 'center',
              valign: 'middle',
              sortable: false
	  },{
	      field: 'status',
              title: '网卡状态',
              align: 'center',
              valign: 'middle',
              sortable: false,
	      formatter: function(value,row,index){
			if( value == 'UP' ){
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
//    function getinfo(value,row,index){
//        eval('rowobj='+JSON.stringify(row))
//        return [
//            '<a href="/infoitem/'+rowobj['id']+'" class="btn-sm btn-success">',
//                '<i class="fa fa-arrow-circle-right"> 详情</i>',
//             '</a>',' ',
//            '<a href="/edititem/'+rowobj['id']+'" class="btn-sm btn-info">',
//                '<i class="fa fa-edit"> 编辑</i>',
//             '</a>',' ',
//            '<a href="/delitem/'+rowobj['id']+'" class="btn-sm btn-danger">',
//                '<i class="fa fa-times"> 删除</i>',
//             '</a>'
//        ].join('');
//    }
//
    //定义列操作
    function getinfo(value,row,index){
        eval('rowobj='+JSON.stringify(row));
        //定义编辑按钮样式，只有管理员或自己编辑的任务才有权编辑
        if({{session.get('access',None)}} == '1' || "{{session.get('name',None)}}" == rowobj['userid']){
            var style_edit = '<a href="/editiface/'+rowobj['id']+'" class="btn-sm btn-info" >';
        }else{
            var style_edit = '<a class="btn-sm btn-info" disabled>';
        }
        //定义删除按钮样式，只有管理员或自己编辑的任务才有权删除
        if({{session.get('access',None)}} == '1' || "{{session.get('name',None)}}" == rowobj['userid']){
            var style_del = '&nbsp;<a href="/deliface/'+rowobj['id']+'" class="btn-sm btn-danger" onClick="return confirm(&quot;确定删除?&quot;)"> ';
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


    /**
    *删除按钮操作
    */
    $('#deluser').popover({
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
                setTimeout("$('#deluser').popover('hide')",1000)
            }else{
                $(this).popover("hide");
                for(i in res){
                    str += res[i]['id']+',';
                }
                $.post('/deluser',{str:str},function(data){
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
