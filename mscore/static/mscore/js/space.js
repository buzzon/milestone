let col_size = document.body.clientWidth / 8;


var n = 0, loading = false, lastDiv;

function addboxes(){
    let length = 10;
    for( i=0; i < length; i++){
        $('#layer').append('<div class="box" style="left:'+(n+i*col_size)+'px;">' + i + '</div>');
    }
	n+=length*col_size;

	UpdateClassWidth(".box", col_size);
    loading = false;
}

addboxes();

 $('#layer').on('scroll',function(e){
	var lastDiv = $('.box').last();
	var lastLeft = lastDiv[0].getBoundingClientRect().left;
  var windowWidth = $(window).width();

	$("#monitor").text(" lastLeft ="+lastLeft+", windowWidth ="+windowWidth);

	if( lastLeft < windowWidth && !loading ){
  	loading = true;
		addboxes();
    $(window).trigger('resize');
  }

});


function UpdateClassWidth(c, width){
	var elements = document.querySelectorAll(c);
    for(var i=0; i<elements.length; i++){
        elements[i].style.width = width + "px";
    }
}



$.ajax({
	url: '/api/mscore/task',
	method: 'get',
	dataType: 'json',
    data: {space: space_id},
	success: function(data){
		console.log(data);
		postTasks(data);
	},
	failure: function(data) {
        alert('Got an error dude');
    }
});


function postTasks(data){
    data.forEach(element => ganttAppend(element));
}

function ganttAppend(element){
    var $gantt = $('#gantt');
    var timeWidth = Math.abs(Date.parse(element.deadline) - Date.parse(element.initial_date)) / 1000 / 60 / 60 / 24 * col_size;
    var $div = $("<div></div>").width(timeWidth).css( { marginLeft : col_size - 15 + "px" } );
    var $link = $().add("<a></a>").attr("href", taskChangeUrl.replace('0', element.id));
    var $title = $().add("<p>" + element.title + "</p>").width(timeWidth).addClass("task").addClass("task" + element.status);
    $gantt.append($div.append($link.append($title)));
}