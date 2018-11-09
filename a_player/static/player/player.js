function add_comment() {
    event.preventDefault();
    let comment = document.getElementById('comment_text');
    let imdb_id = document.getElementById('imdb_id');

	$.ajax({
    	type:"POST",
    	url: '/player/ajax_comment',
		data: {imdb_id: imdb_id.innerHTML,
                comment: comment.value,
                csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
		},
    	success: function(response){
        	console.log(response)
    	}
	});
}

function download_torrent(film_id, quality){
	let myPlayer = videojs("player");
	let progress = $("#torrent_info p");
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
            	progress.html(json_resp['progress'] * 100 + "%");

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