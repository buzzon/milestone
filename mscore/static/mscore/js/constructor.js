var col_size = [];
var count_block = [];
var active_level = 0;

$.ajax({
	url: '/api/mscore/task/period/',
	method: 'get',
	dataType: 'json',
    data: {space: space_id},
	success: function(data){
		count_block[0] = data.tasks.length;
	    col_size[0] = document.body.clientWidth / count_block[0];
//        data.tasks.forEach(element => boxPrepend(element, 0));
        boxAddAppend($('#constructor'),0);
	},
	failure: function(data) {
        alert('Got an error dude');
    }
});

function boxPrepend(parent, element, level){
    count_block[level]++;
    var $div = $().add('<div class="constructor_task_container '+ "l_" + level +'">').width(col_size[level]);
    var $title = $().add("<input class='constructor_task_title' placeholder=" + element +  "></input>").addClass("noselect");
    parent.before($div.append($title));
    boxAddAppend($div, level + 1);
    resize();
    return $title;
}

function boxAddAppend(constructor, level){
    count_block[level] = count_block[level] + 1 || 1;
    var $div = $().add('<div class="constructor_task_container '+ "l_" + level +'">').width(col_size[level]);
    var $title = $().add("<p class='constructor_add_task_title' > + </p>").addClass("noselect");
    $title[0].level = level;
    constructor.append($div.append($title));
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
//            boxPrepend('element', active_level).focus();
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
            break;
    }
})

$(window).on('resize',function(e){ resize(); })

function resize(){
    for (var j = 0; j <  count_block.length; j++){
        for (var i = 0; i < count_block[j]; i++) {
        var s = col_size[j - 1];
        var ss = (col_size[j - 1] || document.body.clientWidth - 4);
            col_size[i] = ss / count_block[j];
            $('.l_' + j).width(col_size[i]);
        }
    }
}
