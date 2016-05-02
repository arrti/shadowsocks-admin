/**
 * Author arrti.
 */

function pagination(page, uri){
    if(page && page.pages != 1){
        var prev = '<li><a href="javascript:;">&laquo;</a></li>';
        if(page.prev != page.page)
          prev = '<li><a href="' + uri + '/' + page.prev + '">&laquo;</a></li>';

        var next = '<li><a href="javascript:;">&raquo;</a></li>';
        if(page.next != page.page)
          next = '<li><a href="' + uri + '/' + page.next + '">&raquo;</a></li>'

        var page_list = '';
        $.each(page.page_list, function(i, p){
          if(page.page == p)
            page_list += '<li class="active"><a href="' + uri + '/' + p + '">' + p +'</a></li>' + '\n';
          else
            page_list += '<li><a href="' + uri + '/' + p + '">' + p +'</a></li>' + '\n';
        });
        page = prev + '\n' + page_list + next;
        return page;
    }
}

function progress_bar(usage){
  var bar = "progress-bar-danger"
  if(usage <= 0.5)
    bar = "progress-bar-success";
  if (usage > 0.5 && usage <= 0.7)
    bar = "progress-bar-primary";
  if (usage > 0.7 && usage <= 0.95)
    bar = "progress-bar-yellow";

  var td = '<div class="progress progress-xs progress-striped active">' + '\n' +
              '<div class="progress-bar ' + bar + '" style="width: '+ usage * 100 + '%' +'"></div>' + '\n' +
           '</div>';

  return td;
}

function progress_label(usage){
  var label = "bg-red"
  if(usage <= 0.5)
    label = "bg-green";
  if (usage > 0.5 && usage <= 0.7)
    label = "bg-light-blue";
  if (usage > 0.7 && usage <= 0.95)
    label = "bg-yellow";

  var td ='<span class="badge ' + label + '">' + usage * 100 + '%' + '</span>';

  return td;
}

function status_label(status){
  var label = "label-danger";
  if(status == "active")
    label = "label-success";
  if (status == "pending")
    label = "label-warning";
  if (status == "banned")
    label = "label-danger";

  var td ='<span class="label ' + label + '">' + status + '</span>';

  return td;
}
