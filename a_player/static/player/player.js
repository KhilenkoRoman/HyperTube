// let film = document.getElementById('film').innerHTML;
// console.log(film);

function add_comment() {
	event.preventDefault();
    let comment = document.getElementById('comment_text'),
		imdb_id = document.getElementById('imdb_id'),
    	user_name = document.getElementById('user_info').innerHTML,
		user_avatar = document.getElementById('user_avatar').innerHTML;

	$.ajax({
    	type:"POST",
    	url: '/player/ajax_comment',
		data: {imdb_id: imdb_id.innerHTML,
                comment: comment.value,
                csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
		},
    	success: function(response){
    		if (user_avatar) {
    			$(".comments").append(
    			'<li class="comment">' +
					'<img class="comment_avatar" src="/media/'+ user_avatar +'">' +
                	'<div class="com_name_and_del">' +
						'<div class="com_name"><i class="fas fa-long-arrow-alt-right"></i>'+ user_name +'</div>' +
						'<i class="fas fa-times del_comm" onclick="del_comm('+ response +', this)"></i>' +
					'</div>' +
                	'<p>' + comment.value + '</p>' +
				'</li>');
			}
			else {
				$(".comments").append(
    			'<li class="comment">' +
					'<div class="no_avatar"></div>' +
                	'<div class="com_name_and_del">' +
						'<div class="com_name"><i class="fas fa-long-arrow-alt-right"></i>'+ user_name +'</div>' +
						'<i class="fas fa-times del_comm" onclick="del_comm('+ response +', this)"></i>' +
					'</div>' +
                	'<p>' + comment.value + '</p>' +
				'</li>');
			}
    	}
	});
}

function download_torrent(film_id, quality){
	let myPlayer = videojs("player");
	let progress = $("#loading");
	console.log(progress);
	let flag = false;
	let video = $("#player");
	// let source = document.createElement('source');
	let json_resp;
	$('.download_btn').remove();


	let timer = setTimeout(function get_torrent_info() {
  		$.ajax({
            type: "POST",
            url: '/player/ajax_torr_info',
            data: {
                film_id: film_id,
				quality: quality,
                csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
            },
            success: function (response) {
            	json_resp = JSON.parse(response);
            	console.log(json_resp);
            	progress.css('width', String(json_resp['progress'] * 100) + "%");

            	if (json_resp['film_file'] && flag==false){
            	    $('#trailer_player').remove();
            	    video.removeClass('none');
            		flag = true;
					myPlayer.src({type: 'video/mp4', src: "/media" + json_resp['film_file']});
					myPlayer.play();
				}

                if (json_resp['error'] == 0 && json_resp['progress'] != 1){
                	console.log("request in 2 sec");
                	timer = setTimeout(get_torrent_info, 2000);
				}

            }
        });
	}, 2000);

}

function del_comm(commentId, element) {
    event.preventDefault();
    let imdb_id = document.getElementById('imdb_id');
	$.ajax({
    	type:"POST",
    	url: '/player/ajax_del_comment',
		data: {
    		imdb_id: imdb_id.innerHTML,
            commentId: commentId,
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
		},
    	success: function(response){
    		element.parentElement.parentElement.remove();
    	}
	});
}

function comment_onblur(input, id, text) {
	document.getElementById('edit_comm_' + id).style.visibility = 'hidden';
	input.value = text;
}

function edit_form_onclick(id) {
	let forms = document.getElementsByClassName('edit_comm');
	for (form of forms) {
		form.childNodes[3].style.visibility = 'hidden';
	}
	document.getElementById('edit_comm_' + id).style.visibility = 'visible';
}

function edit_comm(commentId) {
	event.preventDefault();
	$.ajax({
    	type:"POST",
    	url: '/player/ajax_edit_comment',
		data: {
    		imdb_id: imdb_id.innerHTML,
            commentId: commentId,
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
		},
    	success: function(response){

    	}
	});
}