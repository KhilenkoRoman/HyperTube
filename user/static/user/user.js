$(window).scroll(function () {
    var sc = $(window).scrollTop();
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
	}, 300);
});


$( "#change_pwd_btn" ).on( "click", function() {
    const pwd1 = document.getElementById('id_change_pwd1');
    const pwd2 = document.getElementById('id_change_pwd2');
    const username = document.getElementById('reset_login');
    const key = document.getElementById('reset_key');
    const change_pwd_btn = document.getElementById('change_pwd_btn');
    change_pwd_btn.disabled = true;
    pwd1.classList.remove('unvalid');
    pwd2.classList.remove('unvalid');

    $.ajax({
    	type:"POST",
    	url: '/ajax_new_pwd',
		data: {username: username.value,
			key: key.value,
			pwd1: pwd1.value,
			pwd2: pwd2.value,
			csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
		},
    	success: function(response){
            change_pwd_btn.disabled = false;
            if (response === "error"){
                pwd1.classList.add('unvalid');
                pwd2.classList.add('unvalid');
            }
            if (response === 'sucsess'){
                $("#recover_wrap").addClass("invisible");
                $("#responce_wrap").removeClass("none");

                setTimeout(function(){
                    $("#recover_wrap").addClass("none");
	                $("#responce_wrap").removeClass("invisible");
	            },500);
            }
    	}
	});
});

