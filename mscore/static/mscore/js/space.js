let col_count = 8,
    col_quantity_add = 10,
    col_size = document.body.clientWidth / col_count;

var loading = false;
var last_date = new Date();
var first_date = new Date();
first_date.setDate(first_date.getDate() - 1);
var day_count_before = 0;

function formatDate(date) {

  var dd = date.getDate();
  if (dd < 10) dd = '0' + dd;

  var mm = date.getMonth() + 1;
  if (mm < 10) mm = '0' + mm;

  return dd + '.' + mm;
}

function AddBoxesRight(){
    for(i = 0; i < col_quantity_add; i++){
        $('#timeline').append('<div class="box">' + formatDate(last_date) + '</div>');
        last_date.setDate(last_date.getDate() + 1);
    }
    UpdateClassWidth(".box", col_size);
    loading = false;
    $("#gantt").trigger( "mouseup" );
}

function AddBoxesLeft(){
    for(i=0; i < col_quantity_add; i++){
        $('#timeline div:first-child').before('<div class="box">' + formatDate(first_date) + '</div>');
        first_date.setDate(first_date.getDate() - 1);
    }
    day_count_before += 1;
    UpdateClassWidth(".box", col_size);
    $gantt = $('#gantt');
    $gantt.scrollLeft($gantt.scrollLeft() + col_size * col_quantity_add);
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

var mouse_controller = {
    pos_x: 0,
    down: false,
    scrollLeft: 0,
    x: 0,
    'down_event': function(elem, e) {
        console.log('mouse_controller: down');
        this.down = true;
        this.scrollLeft = elem.scrollLeft;
        this.x = e.clientX;
    },
    'down_last_pos': function(elem) {
        console.log('mouse_controller: down_last_pos');
        this.down = true;
        this.scrollLeft = elem.scrollLeft;
        this.x = pos_x;
    },
    'up_event': function() {
        console.log('mouse_controller: mouseup');
        this.down = false;
    },
    'move_event': function(elem, e) {
        pos_x = e.clientX;
        if (this.down){
            console.log('mouse_controller: move_event');
            elem.scrollLeft = this.scrollLeft + this.x - e.clientX;
        }
    }
}
var down=false, scrollLeft=0, x = 0;


$('#gantt').on('mousemove',function(e){
    mouse_controller.move_event(this, e);
}).on('mousedown',function(e){
    mouse_controller.down_event(this, e);
}).on('mouseup',function(e){
    mouse_controller.up_event();
}).on('scroll',function(e){
    var $firstDiv = $('.box').first();
    var $lastDiv = $('.box').last();

    var firstBound = $firstDiv[0].getBoundingClientRect().right;
    var lastBound = $lastDiv[0].getBoundingClientRect().left;

    var windowWidth = $(window).width();

    if (!loading) {
        if(lastBound < windowWidth){
            loading = true;
            AddBoxesRight();
            $(window).trigger('resize');
        }
        if( -firstBound < col_size){
            loading = true;

            mouse_controller.up_event();
            AddBoxesLeft();
            mouse_controller.down_last_pos(this);

            $(window).trigger('resize');
        }
    }
});

$("#gantt").trigger( "mouseup" );

$.ajax({
	url: '/api/mscore/task/period/',
	method: 'get',
	dataType: 'json',
    data: {space: space_id},
	success: function(data){
		console.log(data);
//		data.forEach(element => ganttAppend(element));
//		data.tasks.forEach(element => $('#tasks').append("<div>" + element.title + "<div/>"));

	},
	failure: function(data) {
        alert('Got an error dude');
    }
});



function ganttAppend(element){
    var $gantt = $('#gantt');
    var timeWidth = Math.abs(Date.parse(element.deadline) - Date.parse(element.initial_date)) / 1000 / 60 / 60 / 24 * col_size;
    var $div = $("<div></div>").width(timeWidth).css( { marginLeft : col_size - 15 + "px" } );
    var $link = $().add("<a></a>").attr("href", taskChangeUrl.replace('0', element.id));
    var $title = $().add("<p>" + element.title + "</p>").width(timeWidth).addClass("task").addClass("task" + element.status);
    $gantt.append($div.append($link.append($title)));
}
