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

$("#0").width(document.body.clientWidth);
$ajax =  $.ajax;

$.ajax({
	url: '/api/mscore/task/period/',
	method: 'get',
	dataType: 'json',
    data: {space: space_id},
	success: function(data){
//        data.tasks.forEach(element => loadNode($('#0'), element));
          loadNode2($('#0'), data);
	},
	failure: function(data) {
        alert('Got an error dude');
    }
});

function addChildren(parent, box){
    parent.append(box);
}

function loadNode(parent, element){
    $box = Box(element);
    parent.append($box);
    $box.width(180);
    element.task.forEach(children => {
        $box.append(Box(children).width($box.width() / element.task.length));
    })
}

function loadNode2(parent, elements){
    if (elements.task == undefined) return;
    elements.task.forEach(children => {
        var box = Box(children).width(parent.width() / elements.task.length);
        parent.append(box);
        loadNode2(box, children);
    })
}

function addRight(elem, box){
    elem.append(box);
}

function Box(element){
    var $div = $().add('<div>').addClass("constructor_task_container");
    var $title = $().add("<input placeholder=element></input>").addClass("constructor_task_title").addClass("noselect");
    $title.val(element.title);

    $title.change(function() {
        updateTask(element, this.value);
    });

    return $div.append($title);
}

function updateTask(element, value){
        $ajax({
	        url: '/api/mscore/task/change/',
	        method: 'post',
	        dataType: 'json',
            data: { csrfmiddlewaretoken: getCookie('csrftoken'), space: space_id, pk: element.id, title: value},
        });
}

$(window).on('resize',function(e){ resize(); })

function resize(){
    $("#0").width(document.body.clientWidth);
    var $div = $("#0");
    $div_children = $div.children();
    $div_children.each(function(){
        $(this).width($div.width() / $div_children.length);
    })
}



//var last_id = 0;
//var boxes = {};
//
//function setId(elem){
//    if (!elem[0].hasAttribute("id")) {
//        last_id++;
//        elem.attr('id', last_id);
//    }
//}
//
//$.ajax({
//	url: '/api/mscore/task/period/',
//	method: 'get',
//	dataType: 'json',
//    data: {space: space_id},
//	success: function(data){
////        data.tasks.forEach(element => boxPrepend(element, 0));
//        boxAddAppend($('#0'),0);
//	},
//	failure: function(data) {
//        alert('Got an error dude');
//    }
//});
//
//function boxPrepend(parent, element){
//    var $div = $().add('<div class="constructor_task_container">');
//    var $title = $().add("<input class='constructor_task_title' placeholder=" + element +  "></input>").addClass("noselect");
//    parent.before($div.append($title));
//    boxAddAppend($div);
//
//
//    setId(parent.parent());
//    boxes[parent.parent().attr('id')] = boxes[parent.parent().attr('id')] + 1 || 1;
//
//    $title.focus();
//    resize();
//}
//
//function boxAddAppend(constructor){
//    var $div = $().add('<div class="constructor_task_container">');
//    var $title = $().add("<p class='constructor_add_task_title' > + </p>").addClass("noselect");
//    constructor.append($div.append($title));
//
//
//    setId(constructor);
//    boxes[constructor.attr('id')] = boxes[constructor.attr('id')] + 1 || 1;
//
//    resize();
//}
//
//
//$(document).on('click', '.constructor_add_task_title', function () {
//    boxPrepend($(this).parent(), 'element');
//});
//
//$(window).on('keydown',function(e){
//    switch (e.code) {
//        case "Tab":
//            console.log(e.code);
//            e.preventDefault();
//            break;
//        case "Enter":
//            var $focused = $(':focus');
//            boxPrepend($focused.parent(), 'element');
//            break;
//        case "ArrowUp":
//             console.log(e.code);
//            break;
//        case "ArrowDown":
//             console.log(e.code);
//            break;
//        case "ArrowLeft":
//            resize();
//             console.log(e.code);
//            break;
//        case "ArrowRight":
//            resize2();
//            console.log(e.code);
//            break;
//    }
//})
//
//$(window).on('resize',function(e){ resize(); })
//
//function resize(){
//    $("#0").width(document.body.clientWidth);
//    for (var i = 0; i <= last_id; i++) {
//        var $div = $("#"+i);
//        $div.find('div').each(function(){
//            $(this).width($div.width() / boxes[i]);
//        })
//    }
//}
//
//
//function resize2(){
//    $("#1").width(0);
//    var $div = $("#0");
//    console.log($div.children());
//    $div.children().width(0);
//}