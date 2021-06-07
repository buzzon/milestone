$('.progress_task').on('mousedown', function(){
    var ids = this.id.split("_");
    $(this).modalForm({ formURL:  taskChangeUrl.replace('1', ids[1]).replace('0', ids[0]) });
});