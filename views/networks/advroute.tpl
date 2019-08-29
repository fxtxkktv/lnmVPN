%rebase base position='路由配置', managetopli="networks"
<div class="page-body">
    <div class="row">
        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">
            <div class="widget">
                <div class="widget-header bordered-bottom bordered-themesecondary">
                    <i class="widget-icon fa fa-tags themesecondary"></i>
                    <span class="widget-caption themesecondary">路由配置——高级路由</span>
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
                            <a id="routeconf" href="/routeconf" class="btn btn-info ">
                                <i class="btn-label fa fa-cog"></i>系统路由
                            </a>
                            <a id="staticroute" href="/staticroute" class="btn btn-primary ">
                                <i class="btn-label fa fa-cog"></i>静态路由
                            </a>
                            <a id="advroute" href="#" class="btn btn-darkorange">
                                <i class="btn-label fa fa-cog"></i>高级路由
                            </a>
                            <a id="advroutepolicy" href="/advroutepolicy" class="btn btn-success">
                                <i class="btn-label fa fa-cog"></i>高级策略
                            </a>
                            <a id="addadvroute" href="/addadvroute" class="btn btn-warning shiny">
                                <i class="btn-label fa fa-plus"></i>添加记录
                            </a>
                            <!--a id="showadvroute" href="/showadvroute" class="btn btn-success">
                                <i class="btn-label fa fa-print"></i>打印高级路由表
                            </a-->
                            %if msg.get('message'):
                              <span style="color:{{msg.get('color')}};font-weight:bold;">&emsp;&emsp;&emsp;&emsp;{{msg.get('message')}}</span>
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
          url: '/api/getrouteinfo3',
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
          /*columns: [{
              field: 'id',
              title: '编号',
              align: 'center',
              valign: 'middle',
              width:25,
              sortable: false, */
          },{
	      field: 'rulename',
              title: '规则描述',
              align: 'center',
              valign: 'middle',
              sortable: false,
              //formatter:url_link
          },{
              field: 'srcaddr',
              title: '源地址',
              align: 'center',
              valign: 'middle',
              sortable: false,
              //formatter:url_link
          },{
              field: 'destaddr',
              title: '目标地址',
              align: 'center',
              valign: 'middle',
              sortable: false
          },{
              field: 'stime',
              title: '时间控制',
              align: 'center',
              valign: 'middle',
              sortable: false
          },{
              field: 'pronum',
              title: '优先级',
              align: 'center',
	      valign: 'middle',
              sortable: false
          },{
              field: 'rtname',
              title: '出口策略',
              align: 'center',
              valign: 'middle',
              sortable: false
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
            var style_edit = '<a href="/editadvroute/'+rowobj['id']+'" class="btn-sm btn-info" >';
        }else{
            var style_edit = '<a class="btn-sm btn-info" disabled>';
        }
        //定义删除按钮样式，只有管理员或自己编辑的任务才有权删除
        if({{session.get('access',None)}} == '1' || "{{session.get('name',None)}}" == rowobj['userid']){
            var style_del = '&nbsp;<a href="/delroute/adv/'+rowobj['id']+'" class="btn-sm btn-danger" onClick="return confirm(&quot;确定删除?&quot;)">';
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


    //任务名的URL链接
    function url_link(value,row,index){
        eval('rowobj='+JSON.stringify(row))
        return [
            '<a href="/infoitem/'+rowobj['id']+'" style="text-decoration:none">',
                rowobj['name'],
             '</a>'
        ].join('');
    }

})
</script>
