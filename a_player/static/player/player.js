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