var col_size = [];
var count_block = [];
var active_level = 0;

var last_id = 0;
var boxes = {};

function setId(elem){
    if (!elem[0].hasAttribute("id")) {
        last_id++;
        elem.attr('id', last_id);
    }
}

$.ajax({
	url: '/api/mscore/task/period/',
	method: 'get',
	dataType: 'json',
    data: {space: space_id},
	success: function(data){
//        data.tasks.forEach(element => boxPrepend(element, 0));
        boxAddAppend($('#0'),0);
	},
	failure: function(data) {
        alert('Got an error dude');
    }
});

function boxPrepend(parent, element, level){
    count_block[level]++;
    var $div = $().add('<div class="constructor_task_container '+ "l_" + level +'">');
    var $title = $().add("<input class='constructor_task_title' placeholder=" + element +  "></input>").addClass("noselect");
    $title[0].level = level;
    parent.before($div.append($title));
    boxAddAppend($div, level + 1);


    setId(parent.parent());
    boxes[parent.parent().attr('id')] = boxes[parent.parent().attr('id')] + 1 || 1;

    resize();

    return $title;
}

function boxAddAppend(constructor, level){
    count_block[level] = count_block[level] + 1 || 1;
    var $div = $().add('<div class="constructor_task_container '+ "l_" + level +'">');
    var $title = $().add("<p class='constructor_add_task_title' > + </p>").addClass("noselect");
    $title[0].level = level;
    constructor.append($div.append($title));


    setId(constructor);
    boxes[constructor.attr('id')] = boxes[constructor.attr('id')] + 1 || 1;

    resize();
}


$(document).on('click', '.constructor_add_task_title', function () {
    boxPrepend($(this).parent(), 'element', this.level).focus();
});

$(window).on('keydown',function(e){
    switch (e.code) {
        case "Tab":
            console.log(e.code);
            e.preventDefault();
            break;
        case "Enter":
            var $focused = $(':focus');
            boxPrepend($focused.parent(), 'element', $focused[0].level).focus();
            break;
        case "ArrowUp":
             console.log(e.code);
            break;
        case "ArrowDown":
             console.log(e.code);
            break;
        case "ArrowLeft":
             console.log(e.code);
            break;
        case "ArrowRight":
             console.log(e.code);
             boxAddAppend($('#0'),0);
            break;
    }
})

$(window).on('resize',function(e){ resize(); })

function resize(){
    $("#0").width(document.body.clientWidth);
    for (var i = 0; i <= last_id; i++) {
        var $div = $("#"+i);
        console.log($div.width());
        $div.find('div').each(function(){
            $(this).width($div.width() / boxes[i]);
        })
    }
}
