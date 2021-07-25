function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var first_layer_count = 0;
$('#content').removeClass('row');

$ajax =  $.ajax;

var first_date = new Date();
var last_date = new Date();
first_date.setDate(first_date.getDate() - 10);
last_date.setDate(last_date.getDate() + 10);

$.ajax({
	url: '/api/mscore/task/period/',
	method: 'get',
	dataType: 'json',
    data: {space_id, first_date: first_date.toUTCString(), last_date : last_date.toUTCString()},
	success: function(data){
	    first_layer_count = data.task.length;
	    if (first_layer_count){
	        loadNode($('#0'), data);
            resize();
	    }
	    else{
	        $ajax({
	            url: '/api/mscore/task/create/',
	            method: 'post',
	            dataType: 'json',
	            data: { csrfmiddlewaretoken: getCookie('csrftoken'), space_id, is_nested: false},
	        }).done(function(data){
	            var box = Box(data.task);
	            first_layer_count++;
	            $('#0').append(box);
                resize();
	        });
	    }
	},
	failure: function(data) {
        alert('Got an error dude');
    }
});

function loadNode(parent, elements){
    elements.task.forEach(children => {
        var box = Box(children);
        parent.append(box);
        loadNode(box, children);
    })
}

function Box(element){
    var $div = $().add('<div>').addClass("constructor_task_container");
    var $title = $().add("<input placeholder=element></input>").addClass("constructor_task_title").addClass("noselect");
    $title.val(element.title);

    $title.change(function() {
        updateTask(element, this.value);
    }).on('keydown',function(e){
         switch (e.key) {
            case "Enter":
                if ($(this).parent().parent().attr('id') == 0){
                    first_layer_count++;
                };
                createTask($(this).parent().parent(), element, false);
                break;
            case "Tab":
                createTask($(this).parent(), element, true);
                e.preventDefault();
                break;
            case "Delete":
                if ($(this).parent().parent().attr('id') == 0){
                    first_layer_count--;
                };
                deleteTask($(this).parent(), element);
                e.preventDefault();
                break;
         }
    });

    return $div.append($title);
}

function createTask($parent, element, is_nested){
    $.when($ajax({
	    url: '/api/mscore/task/create/',
	    method: 'post',
	    dataType: 'json',
        data: { csrfmiddlewaretoken: getCookie('csrftoken'), space_id, pk: element.id, is_nested: is_nested?1:0 },
    })).done(function(data){
        var $boxInput = Box(data.task);
        $parent.append($boxInput);
        $boxInput.children(":first").focus();
        resize();
    } );
}

function deleteTask($parent, element){
    $.when($ajax({
	    url: '/api/mscore/task/delete/',
	    method: 'post',
	    dataType: 'json',
        data: { csrfmiddlewaretoken: getCookie('csrftoken'), space_id, pk: element.id},
    })).done(function(data){
        $parent.remove();
        resize();
    } );
}

function updateTask(element, value){
    $ajax({
        url: '/api/mscore/task/change/',
        method: 'post',
        dataType: 'json',
        data: { csrfmiddlewaretoken: getCookie('csrftoken'), space_id, pk: element.id, title: value},
    });
}

$(window).on('resize',function(e){ resize(); })

function resize(){
    var col_size = Math.max(document.body.clientWidth / first_layer_count, 300);

    console.log(document.body.clientWidth / first_layer_count + " " + col_size);

    $("#0").width(col_size * first_layer_count);
    var $div = $("#0");
    resizeChildrenRec($div);
}

function resizeChildrenRec($div){
    var $children = $div.children().filter('.constructor_task_container');
    var parent_width = $div.width();
    var children_width = $div.width() / $children.length;

    for(var j=0; j< $children.length; j++){
        $children.eq(j).width(children_width);
        resizeChildrenRec($children.eq(j));
    }
}
