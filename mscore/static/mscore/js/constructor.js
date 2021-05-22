var selected_box;


$.ajax({
	url: '/api/mscore/task/period/',
	method: 'get',
	dataType: 'json',
    data: {space: space_id},
	success: function(data){
//        data.tasks.forEach(element => boxPrepend(element, 0));
//        boxAddAppend($('#0'),0);
        addChildren($('#0'), Box());
	},
	failure: function(data) {
        alert('Got an error dude');
    }
});

function addChildren(parent, box){
    selected_box = box;
    parent.append(box);
    selected_box.children().first().focus();
    resize();
}

function Box(){
    var $div = $().add('<div>').addClass("constructor_task_container");
    var $title = $().add("<input placeholder=element></input>").addClass("constructor_task_title").addClass("noselect");
    return $div.append($title);
}

$(window).on('resize',function(e){ resize(); })

function resize(){
    selected_box.width(document.body.clientWidth);
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