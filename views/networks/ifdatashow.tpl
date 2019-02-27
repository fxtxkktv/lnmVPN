%rebase base position='接口流量', managetopli="networks"

<link rel="stylesheet" href="/assets/bootstrap-select/bootstrap-select.min.css">
<link href="/assets/css/charisma-app.css" rel="stylesheet" type="text/css" />

<div class="page-body">
    <div class="row">
        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">
            <div class="widget" style="background: #fff;">
                <div class="widget-header bordered-bottom bordered-themesecondary">
                    <i class="widget-icon fa fa-tags themesecondary"></i>
                    <span class="widget-caption themesecondary">接口流量</span>
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
          <div class="box col-md-6" style="padding-left:0px;">
            <div class="box-inner widget" style="background: #fff;">
            <div class="box-header well" data-original-title>
                <i class="glyphicon glyphicon-list-alt widget-icon"></i>
                <span class="widget-caption themesecondary">操作信息</span>
            </div>
            <div class="box-content" style="height:680px;padding:0px;">
            <div class="modal-body" style="width:100%">
                  <label class="" for="inputSuccess1">网络接口</label>
                  <select type="text" class="form-control" id="ifname" name="ifname">
                          %for name in iflist:
                               <option 
                               %if sel.get('ifname','') == name.get('attr'):
                                   selected
                               %end
                                value='{{name.get('ifacename')}}'>{{name.get('ifacename')}}</option>
                          %end
                  </select>
            </div>
            <div class="modal-body" style="width:100%">
                  <label class="" for="inputSuccess1">显示条数</label>
                  <select class="form-control" id="shownum" name="shownum">
                    <option
                     %if sel.get('shownum','') == '5':
                        selected
                     %end
                     value='5'>5</option>
                     <option
                     %if sel.get('shownum','') == '10':
                        selected
                     %end
                     value='10'>10</option>
                     <option
                     %if sel.get('shownum','') == '20':
                        selected
                     %end
                     value='20'>20</option>
                  </select>
            </div>
            <div class="modal-body" style="width:100%">
                  <label class="" for="inputSuccess1">统计时间</label>
                  <select class="form-control" id="rftime" name="rftime" >
                     <option
                     %if sel.get('rftime','') == '10':
                        selected
                     %end
                     value='10'>10秒</option>
                     <option
                     %if sel.get('rftime','') == '30':
                        selected
                     %end
                     value='30'>30秒</option>
                     <option
                     %if sel.get('rftime','') == '60':
                        selected
                     %end
                     value='60'>60秒</option>
                  </select>
            </div>
            <div class="modal-body" id="submit">
                    <div class="" style="padding-top: 3px;padding-bottom:3px;">
                        <button type="submit" style="float:left;" class="btn btn-primary">开始统计</button>
                    </div>
            </div>
          </div></div></div>
          <!--right-->
          <div class="box col-md-6" style="padding-right:0px;">
            <div class="box-inner widget" style="background: #fff;">
            <div class="box-header well" data-original-title>
                <i class="glyphicon glyphicon-list-alt widget-icon"></i>
                <span class="widget-caption themesecondary">运行结果</span>
            </div>
            <div class="box-content" style="height:680px;padding:0px;">
             <div class="modal-body" style="width:100%">
                  <textarea id="runresult" name="runresult" 
                    style="width:100%;height:650px;background-color:#000000;color:#33ff33;resize:none;font-family:sans-serif;" 
                  readonly >{{runresult}}</textarea>
            </div>
          </div></div></div>  
         </div>
       </form>
      </div>
     </div>
    </div>
</div>
<script src="/assets/js/datetime/bootstrap-datepicker.js"></script> 
<script src="/assets/bootstrap-select/bootstrap-select.min.js"></script>
