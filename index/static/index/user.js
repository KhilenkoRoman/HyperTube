$(window).scroll(function () {
    var sc = $(window).scrollTop()
    if (sc > 100) {
        $("#header-scroll").addClass("small");
        $("#sub_header").addClass("small");
    }
    else {
        $("#header-scroll").removeClass("small");
        $("#sub_header").removeClass("small")
    }
});




$(window).on('load', function() {
	var preloaderFadeOutTime = 500;
	var preloader = $('#preloader');

	setTimeout(function(){
    	preloader.fadeOut(preloaderFadeOutTime);
	}, 500);
});