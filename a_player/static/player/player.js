// let film = document.getElementById('film').innerHTML;
// console.log(film);
let i = 0;

function add_comment(event, lang) {
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
            $(".comments").append(
            '<li class="comment">' +
                (user_avatar ? '<img class="comment_avatar" src="/media/'+ user_avatar +'">' : '<div class="no_avatar"></div>') +
                '<div class="com_name_and_del">' +
                    '<div class="com_name"><i class="fas fa-long-arrow-alt-right"></i>'+ user_name +'</div>' +
                    '<i class="fas fa-times del_comm" onclick="del_comm(' + response + ', this)"></i>' +
                '</div>' +
                '<form id="edit_form_' + response + '" class="comm_text edit_comm" onclick="edit_form_onclick(' + response + ')"'+
                    'onsubmit="edit_comm(' + response +')">' +
                    '<input '+
                        'id="edit_input_'+ response +'"'+
                        'onfocus="edit_input_onfocus('+ response + ')"' +
                        'value="' + comment.value + '"'+
                        'onblur="comment_onblur(this, ' + response + ', '+ comment.value + ')">' +
                    '<button ' +
                        'id="edit_comm_'+ response + '"'+
                        'type="submit"'+
                    '>' + (lang === 2 ? 'Исправить' : 'Edit') + '</button>'+
                '</form>' +
            '</li>');
			comment.value = '';
    	}
	});
}

function download_torrent(film_id, quality){
	let myPlayer = videojs("player");
	let progress = $("#loading");
	// console.log(progress);
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
            	// console.log(json_resp);
            	progress.css('width', String(json_resp['progress'] * 100) + "%");

            	if (json_resp['film_file'] && flag==false){
            	    $('#trailer_player').remove();
            	    video.removeClass('none');
            		flag = true;
					myPlayer.src({type: 'video/mp4', src: "/media" + json_resp['film_file']});
					myPlayer.play();
				}

                if (json_resp['error'] == 0 && json_resp['progress'] != 1){
                	// console.log("request in 2 sec");
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

function edit_comm(commentId) {
	let comm = document.getElementById('edit_input_' + commentId),
		imdb_id = document.getElementById('imdb_id');
	event.preventDefault();
	$.ajax({
    	type:"POST",
    	url: '/player/ajax_edit_comment',
		data: {
    		imdb_id: imdb_id.innerHTML,
            commentId: commentId,
			commentText: comm.value,
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
		},
    	success: function(response){
    		let form = document.getElementById('edit_form_' + commentId),
				button = document.getElementById('edit_comm_' + commentId);
			comm.defaultValue = comm.value;
			form.style.background = '#ffffff30';
			button.style.visibility = 'hidden';
    	}
	});
}

function edit_input_onfocus(id) {
	let forms = document.getElementsByClassName('edit_comm');
	for (form of forms) {
		form.style.background = '#ffffff30';
		form.childNodes[3].style.visibility = 'hidden';
		form.childNodes[1].value = form.childNodes[1].defaultValue;
	}
	document.getElementById('edit_form_' + id).style.background = 'white';
	document.getElementById('edit_comm_' + id).style.visibility = 'visible';
}