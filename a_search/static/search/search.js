
var page = 1;
var timer = 0;
var predoh = 0;
var curLoc = location.href;
var box = document.body.getBoundingClientRect();

function search(page, search_field, genre){

    $.ajax({
    	type:"POST",
    	url: '/search/ajax_search_request',
		data: {
    		search_field: search_field.value,
			page:page,
			genre:genre,
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

function pagin() {
  timer = 0;
}

window.onscroll = function() {
	if(box.bottom + window.pageYOffset > document.body.scrollHeight && timer == 0)
	{
		const search_field = document.getElementById('head_search_input');
		page++;
		search(page, search_field);
		timer = 1;
		setTimeout(pagin, 1000);
	}
}

$('#search_form').on('submit', function(e) {
    event.preventDefault();
    curLoc = "";
    const search_field = document.getElementById('head_search_input');
    const genre_select = document.getElementById('genre_select');
    curLoc = search_field.value + "?genere=" + genre_select.value;
    page = 1;
    search(page, search_field, genre_select.value);
    if(curLoc == "")
       window.history.pushState("", "Search", "/search/film/");
    else
        window.history.pushState("", "Search", curLoc);
    page++;
});