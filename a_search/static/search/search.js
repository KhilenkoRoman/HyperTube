
$('#search_form').on('submit', function(e) {
    event.preventDefault();
    const search_field = document.getElementById('head_search_input');

    $.ajax({
    	type:"POST",
    	url: '/search/ajax_search_request',
		data: {search_field: search_field.value,
			csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
		},
    	success: function(response){
    		console.log(response);

		}
	});
});