%rebase base position='系统检查', managetopli="system"
<div class="page-body">
    <div class="row">
        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">
            <div class="widget">
                <div class="widget-header bordered-bottom bordered-themesecondary">
                    <i class="widget-icon fa fa-tags themesecondary"></i>
                    <span class="widget-caption themesecondary">环境检查</span>
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
                            <a id="syschk" href="/syscheck" class="btn btn-primary ">
                                <i class="btn-label fa fa-plus"></i>重新检测
                            </a>
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
          url: '/api/getsyschkinfo',
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
              field: 'name',
              title: '组件名称',
              align: 'center',
              valign: 'middle',
              sortable: false,
	      },{
	          field: 'value',
              title: '系统状态',
              align: 'center',
              valign: 'middle',
              sortable: false,
	          formatter: function(value,row,index){
			  if( value == '0' ){
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
              //暂时不开放此功能
              //formatter:getinfo
          }]
      });
})
</script>
