let col_count = 8,
    col_quantity_add = 10,
    col_size = document.body.clientWidth / col_count;

var loading = false;

function AddBoxesRight(){
    for(i = 0; i < col_quantity_add; i++){
        $('#layer').append('<div class="box">' + i + '</div>');
    }
    loading = false;
}

function AddBoxesLeft(){
    for(i=0; i < col_quantity_add; i++){
        $('#layer div:first-child').before('<div class="box">before' + i + '</div>');
    }
    loading = false;
}

function UpdateClassWidth(c, width){
    var elements = document.querySelectorAll(c);
    for(var i=0; i<elements.length; i++){
        elements[i].style.width = width + "px";
    }
}

AddBoxesRight();
AddBoxesLeft();
UpdateClassWidth(".box", col_size);

$('#layer').scrollLeft(col_size * (col_quantity_add + 1));

$('#layer').on('scroll',function(e){
    var $firstDiv = $('.box').first();
    var $lastDiv = $('.box').last();

    var firstBound = $firstDiv[0].getBoundingClientRect().left;
    var lastBound = $lastDiv[0].getBoundingClientRect().left;

    var windowWidth = $(window).width();

    if (!loading) {
        if(lastBound < windowWidth){
            loading = true;
            AddBoxesRight();
            UpdateClassWidth(".box", col_size);
            $(window).trigger('resize');
        }
        if( -firstBound < windowWidth){
            loading = true;
            $('#layer').scrollLeft(col_size * -20);
            AddBoxesLeft();
            UpdateClassWidth(".box", col_size);
            $(window).trigger('resize');
        }
    }
});

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
