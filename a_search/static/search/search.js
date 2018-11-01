
var page = 1;
var timer = 0;
var predoh = 0;
var curLoc = location.href;
var box = document.body.getBoundingClientRect();

function search(page, search_field, genre, sort_by){

    $.ajax({
    	type:"POST",
    	url: '/search/ajax_search_request',
		data: {
    		search_field: search_field.value,
			page:page,
			genre:genre,
			sort_by:sort_by,
			csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
		},
    	success: function(response){
    		console.log(response);
    		if(response['data']['movie_count'] > 0)
    		{
                  let i = 0;
                  if (page == 1) {
                  		if (response['data']['movies'][i]['upl_cover'] != ""){
							$(".result").html('<li class="results-item-wrap"> <a href=""> <div> <img src="/media/' + response['data']['movies'][i]['upl_cover'] + '" class="poster"></div><p>' + response['data']['movies'][i]['title_english'] + '</p><p>' + response['data']['movies'][i]['genres'] + '</p></a></th>');}
						else {
							$(".result").html('<li class="results-item-wrap"> <a href=""> <div> <img src="/static/search/nocover.png" class="poster"></div><p>' + response['data']['movies'][i]['title_english'] + '</p><p>' + response['data']['movies'][i]['genres'] + '</p></a></th>');}
                      i++;
                  }
                  while(i < response['data']['movie_count'] && i < response['data']['limit'])
				  {
				  	if (response['data']['movies'][i]['upl_cover'] != ""){
							$(".result").html('<li class="results-item-wrap"> <a href=""> <div> <img src="/media/' + response['data']['movies'][i]['upl_cover'] + '" class="poster"></div><p>' + response['data']['movies'][i]['title_english'] + '</p><p>' + response['data']['movies'][i]['genres'] + '</p></a></th>');}
						else {
							$(".result").html('<li class="results-item-wrap"> <a href=""> <div> <img src="/static/search/nocover.png" class="poster"></div><p>' + response['data']['movies'][i]['title_english'] + '</p><p>' + response['data']['movies'][i]['genres'] + '</p></a></th>');}
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
    const sort_by_select = document.getElementById('sort_by_select');
    curLoc = search_field.value + "?genere=" + genre_select.value + "&sort_by=" + sort_by_select.value;
    page = 1;
    search(page, search_field, genre_select.value, sort_by_select.value);
    window.history.pushState("", "Search", "/search/film/" + curLoc);
    page++;
});