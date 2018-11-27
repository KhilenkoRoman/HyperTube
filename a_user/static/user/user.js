var popup_active = false;

$(window).scroll(function () {
    var sc = $(window).scrollTop();
    if (sc > 100) {
        $("#header-scroll").addClass("small");
        $("#sub_header").addClass("small");
        $("#head_logout_btn").addClass("small");
        $("#menu").addClass("small");
    }
    else {
        $("#header-scroll").removeClass("small");
        $("#sub_header").removeClass("small");
        $("#head_logout_btn").removeClass("small");
        $("#menu").removeClass("small");
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

function usr_pwd_change(event){
    event.preventDefault();
    const pwd1 = document.getElementById('usr_pwd1');
    const pwd2 = document.getElementById('usr_pwd2');
    const change_pwd_btn = document.getElementById('usr_pwd_btn');
    change_pwd_btn.disabled = true;
    pwd1.classList.remove('unvalid');
    pwd2.classList.remove('unvalid');

    $.ajax({
    	type:"POST",
    	url: '/user/ajax_user_change_pwd',
		data: {pwd1: pwd1.value,
			pwd2: pwd2.value,
			csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
		},
    	success: function(response){
    	    // console.log(response);

            if (response === "error"){
                change_pwd_btn.disabled = false;
                pwd1.classList.add('unvalid');
                pwd2.classList.add('unvalid');
            }
            if (response === 'sucsess'){
                change_pwd_btn.innerText = "Done";
                change_pwd_btn.style.backgroundColor = "#00800069";
                pwd1.value = "";
                pwd2.value = "";
                pwd1.classList.remove('unvalid');
                pwd2.classList.remove('unvalid');

                setTimeout(function(){

                    change_pwd_btn.disabled = false;
                    change_pwd_btn.style.backgroundColor = "#ef4646bd";
                    change_pwd_btn.innerText = "Save";
	            },2000);
            }
    	}
	});
}

function usr_info_change(event){
    event.preventDefault();
    const first_name = document.getElementById('f_name');
    const last_name = document.getElementById('l_name');
    const email = document.getElementById('email');
    const change_info_btn = document.getElementById('change_info_btn');
    change_info_btn.disabled = true;
    first_name.classList.remove('unvalid');
    last_name.classList.remove('unvalid');
    email.classList.remove('unvalid');

    $.ajax({
    	type:"POST",
    	url: '/user/ajax_user_change_info',
		data: {first_name: first_name.value,
			last_name: last_name.value,
            email: email.value,
			csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
		},
    	success: function(response){
    	    if (response.includes("error_first_name"))
                first_name.classList.add('unvalid');
    	    if (response.includes("error_last_name"))
                last_name.classList.add('unvalid');
    	    if (response.includes("error_email"))
                email.classList.add('unvalid');

    	    if (!response.includes("success"))
    	        change_info_btn.disabled = false;
    	    else {
                change_info_btn.innerText = "Done";
                change_info_btn.style.backgroundColor = "#00800069";
                setTimeout(function(){
                    change_info_btn.disabled = false;
                    change_info_btn.style.backgroundColor = "#ef4646bd";
                    change_info_btn.innerText = "Save";
	            },2000);
            }
    	}
	});
}

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
//    if (!div.is(e.target) && div.has(e.target).length === 0
//        && !div2.is(e.target) && div2.has(e.target).length === 0)
//    {
////        container.classList.add('invisible');
////        shadow.classList.add('invisible');
//    }
    popup_active = false;
});

$('#popup_ok').on( "click", function() {
  document.getElementsByClassName('b-container')[0].classList.add('invisible');
  document.getElementsByClassName('b-popup')[0].classList.add('invisible');
  popup_active = false;
});


$("#image_to_upload").on("change", function() {
    let formdata = new FormData();
    let file = this.files[0];
    const img = document.getElementById('photo_section').getElementsByTagName('img')[0];
    const input = document.getElementById('image_to_upload');
    const label = document.getElementById('image_to_upload_label');

    if (formdata) {
        formdata.append('csrfmiddlewaretoken', document.getElementsByName('csrfmiddlewaretoken')[0].value);
        formdata.append("avatar", file);

        input.disabled = true;
        $.ajax({
            url: "/user/ajax_change_avatar",
            type: "POST",
            data: formdata,
            processData: false,
            contentType: false,
            success:function(response){
                if (response == "img_size_error"){
                    label.innerHTML = "Too large";
                    label.style.backgroundColor = "#ef4646bd";
                    setTimeout(function(){
                        input.disabled = false;
    	                label.style.backgroundColor = "#26c6dac7";
    	                label.innerHTML = "Upload";
	                }, 2000);
                }
                else if (response == "img_format_error"){
                    label.innerHTML = "Wrong format";
                    label.style.backgroundColor = "#ef4646bd";
                    setTimeout(function(){
                        input.disabled = false;
    	                label.style.backgroundColor = "#26c6dac7";
    	                label.innerHTML = "Upload";
	                }, 2000);
                }
                else if (response == "error"){
                    label.innerHTML = "Error";
                    label.style.backgroundColor = "#ef4646bd";
                    setTimeout(function(){
                        input.disabled = false;
    	                label.style.backgroundColor = "#26c6dac7";
    	                label.innerHTML = "Upload";
	                }, 2000);
                }
                else {
                    // console.log(response);
                    img.src=response;
                    label.innerHTML = "Done";
                    label.style.backgroundColor = "#00800069";
                    setTimeout(function(){
                        input.disabled = false;
    	                label.style.backgroundColor = "#26c6dac7";
    	                label.innerHTML = "Upload";
	                }, 2000);
                }
            }
        });
    }
});