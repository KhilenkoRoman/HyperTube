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

window.onload = function(){
	const film_id = $("#film_id").html();
	const quality = $("#quality").html();
	let video = document.getElementById('player');
	let source = document.createElement('source');
	let downloaded = 0;
	let json_resp;

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

            	if (json_resp['film_file']){
            		source.setAttribute('src', "/media" + json_resp['film_file']);
					video.appendChild(source);
					video.play();
				}

                if (json_resp['error'] == 0 && json_resp['progress'] != 1){
                	console.log("request in 2 sec");
                	timer = setTimeout(get_torrent_info, 2000);
				}

            }
        });
	}, 2000);


};
