var popup_active = false;

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

// for recover password
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

function social_connect(provider) {
    const container = document.getElementsByClassName('b-container')[0];
    const shadow = document.getElementsByClassName('b-popup')[0];
    const text = document.getElementById('popup_text');

    if (provider == 'provider42')    {
        text.innerText = "Activated Intra 42";
    }
    else {
        text.innerText = "Activated " + provider;
    }
    container.classList.remove('invisible');
    shadow.classList.remove('invisible');

    setTimeout(function(){
    	container.classList.add('invisible');
    	shadow.classList.add('invisible');
	}, 40000);
}

$(document).mouseup(function (e)
{
    const container = document.getElementsByClassName('b-container')[0];
    const shadow = document.getElementsByClassName('b-popup')[0];

    const div = $(".b-container");
    const div2 = $("#popup_text");
    if (!div.is(e.target) && div.has(e.target).length === 0
        && !div2.is(e.target) && div2.has(e.target).length === 0)
    {
        container.classList.add('invisible');
        shadow.classList.add('invisible');
    }
    popup_active = false;
});

$('#popup_ok').on( "click", function() {
  document.getElementsByClassName('b-container')[0].classList.add('invisible');
  document.getElementsByClassName('b-popup')[0].classList.add('invisible');
  popup_active = false;
});

function info_change() {
    event.preventDefault();
    console.log("asd");
}