
var page = 1;
var predoh = 0;

function search(page){
	const search_field = document.getElementById('head_search_input');

    $.ajax({
    	type:"POST",
    	url: '/search/ajax_search_request',
		data: {
    		search_field: search_field.value,
			page:page,
			csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
		},
    	success: function(response){
            console.log(response);
    		if(response['data']['movie_count'] > 0)
    		{
                  let i = 0;
                  if (page == 0) {
                      $(".result").html('<li class="results-item-wrap"> <a href=""> <div> <img src="' + response['data']['movies'][i]['medium_cover_image'] + '" class="poster"></div><p>' + response['data']['movies'][i]['title_english'] + '</p><p>' + response['data']['movies'][i]['genres'] + '</p></a></th>');
                      i++;
                  }
                  while(i < response['data']['movie_count'] && i < response['data']['limit'])
				  {
				  	$( ".result").html($( ".result").html() + '<li class="results-item-wrap"> <a href=""> <div> <img src="' + response['data']['movies'][i]['medium_cover_image'] + '" class="poster"></div><p>' + response['data']['movies'][i]['title_english'] + '</p><p>' + response['data']['movies'][i]['genres'] + '</p></a></th>');
				  	i++;
				  }
    		}else{
    			$(".result").html("The search has not given any results\n");
   		}

		}
	});
}

$('#search_form').on('submit', function(e) {
    event.preventDefault();
    search(page);
    page++;
});