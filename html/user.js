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



// var preloader = $('#spinner-wrapper');
// $(window).on('load', function() {
// 	var preloaderFadeOutTime = 500;

// 	function hidePreloader() {
// 		preloader.fadeOut(preloaderFadeOutTime);
// 	}
// 	hidePreloader();
// });