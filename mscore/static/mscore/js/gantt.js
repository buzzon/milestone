var first_date = new Date();
var last_date = new Date();
var col_size = 0;

window.onload = function(){
    first_date.setDate(first_date.getDate() - 20);
    last_date.setDate(last_date.getDate() + 5);

    $.ajax({
	    url: '/api/mscore/task/period/',
	    method: 'get',
	    dataType: 'json',
        data: {space_id, first_date: first_date.toUTCString(), last_date : last_date.toUTCString()},
	    success: function(data){
            DrawGantPeriod(data.task);
	    }
    });
}

function resize(){
    col_size = $('.time-column').width();
}

$(window).resize(function() {
    resize();
});

function DrawGantPeriod(tasks){
    for(var i = new Date(first_date); i < last_date; i.setDate(i.getDate() + 1)){
        $('#time-list').append('<div class="time-column noselect"><div class="time-data">'
        + formatDate(i) + '</div><div class="time-border"></div></div>');
    }
    resize();
    tasks.forEach(element => addTaskGantt(element));
}

function addTaskGantt(element){
    var $tasks = $('#tasks');
    $div = taskCreate($tasks, element);
    console.log(element);

    $div.on('click', function(){
        console.log(this.id);
        window.location.href = taskChangeUrl.replace('0', this.id);
    });
}


function taskCreate($parent, element){
    var time_width = (Date.parse(element.deadline) - Date.parse(element.initial_date)) / 1000 / 60 / 60 / 24 * col_size;
    var $task = $('').add('<div id="' + element.id + '" class="task noselect" style="width:'+ time_width + 'px; margin-left:' + getPreindent(element) + 'px"></div>');
    var $state = $('').add('<div class="state task' + element.status + '"></div>');
    var $title = $('').add('<div class="task-title">' + element.title  + '</div>');
    $task.append($state).append($title);
    $parent.append($task);
    return $task;
}

function getPreindent(element){
    var initial_date = new Date(element.initial_date);
    var pre_indent_minutes = (initial_date.getUTCHours() + initial_date.getMinutes() / 60) * col_size / 24;
    var pre_indent_days = (parseInt((initial_date-first_date)/(24*3600*1000)) + 1) * col_size;
    return pre_indent_minutes + pre_indent_days;
}

function formatDate(date) {
  var days = ["Вc", "Пн", "Вт", "Ср", "Чт", "Пт", "Сб"];
  var dd = date.getDate();
  if (dd < 10) dd = '0' + dd;

  var mm = date.getMonth() + 1;
  if (mm < 10) mm = '0' + mm;

  var day = date.getDay();
  return dd + '.' + mm + ', ' + days[day];
}

var mouse_controller = {
    pos_x: 0,
    down: false,
    scrollLeft: 0,
    x: 0,
    down_event: function(elem, e) {
        this.down = true;
        this.scrollLeft = elem.scrollLeft;
        this.x = e.clientX;
    },
    up_event: function() {
        this.down = false;
    },
    move_event: function(elem, e) {
        pos_x = e.clientX;
        if (this.down){
            elem.scrollLeft = this.scrollLeft + this.x - e.clientX;
        }
    }
}

$('.task-gantt').on('mousemove',function(e){
    mouse_controller.move_event(this, e);
}).on('mousedown',function(e){
    mouse_controller.down_event(this, e);
}).on('mouseup',function(e){
    mouse_controller.up_event();
});

$('.task_on_list').on('mousedown', function(){
    var currentElement = $("#" + this.id.split("_")[1]);
    $('#time-list').animate({scrollLeft:  $(currentElement).css('margin-left')}, 1000);
});

