
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
    		if(response['data']['movie_count'] > 0)
    		{
    		       console.log($(".search_row").html());
                   let i = 0;
                    $( ".search_row").html('<th class="search_item"> <a href=""> <div> <img src="' + response['data']['movies'][i]['medium_cover_image'] + '" class="poster"></div><p>' + response['data']['movies'][i]['title_english'] + '</p><p>' + response['data']['movies'][i]['genres'] + '</p></a></th>');
                    i++;
                    while(i < response['data']['movie_count'])
                    {
                        $( ".search_row").html($( ".search_row").html() + '<th class="search_item"> <a href=""> <div> <img src="' + response['data']['movies'][i]['medium_cover_image'] + '" class="poster"></div><p>' + response['data']['movies'][i]['title_english'] + '</p><p>' + response['data']['movies'][i]['genres'] + '</p></a></th>');
                        i++;
                    }
    		}else{
    		     console.log("kek\n");
    		}

		}
	});
});