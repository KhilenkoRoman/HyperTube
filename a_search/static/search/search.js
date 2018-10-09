
var page = 1;
var predoh = 0;
var curLoc = location.href;
function search(page, search_field){

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
                  if (page == 1) {
                      $(".result").html('<li class="results-item-wrap"> <a href=""> <div> <img src="' + response['data']['movies'][i]['medium_cover_image'] + '" class="poster"></div><p>' + response['data']['movies'][i]['title_english'] + '</p><p>' + response['data']['movies'][i]['genres'] + '</p></a></th>');
                      i++;
                  }
                  while(i < response['data']['movie_count'] && i < response['data']['limit'])
				  {
				  	$( ".result").html($( ".result").html() + '<li class="results-item-wrap"> <a href=""> <div> <img src="' + response['data']['movies'][i]['medium_cover_image'] + '" class="poster"></div><p>' + response['data']['movies'][i]['title_english'] + '</p><p>' + response['data']['movies'][i]['genres'] + '</p></a></th>');
				  	i++;
				  }
    		}else{
    			$(".result").html('<li>The search has not given any results\n</li>');
   		}

		}
	});
}

window.onscroll = function() {
	console.log(window.pageYOffset);
	console.log(document.body.scrollHeight);
	if(document.body.scrollHeight - window.pageYOffset == document.body.scrollHeight)
	{
		const search_field = document.getElementById('head_search_input');
		page++;
		search(page, search_field);
	}
}


$('#search_form').on('submit', function(e) {
    event.preventDefault();
    const search_field = document.getElementById('head_search_input');
	curLoc = "reg=" + search_field.value;
    page = 1;
    search(page, search_field);
    // window.history.pushState("", "Search", curLoc);
    // location.hash = curLoc;
    page++;
});