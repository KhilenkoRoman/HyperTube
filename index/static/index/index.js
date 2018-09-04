/* ------------------------------------ Click on login and Sign Up to  changue and view the effect
---------------------------------------
*/

function actvate_login()
{
	document.querySelector('.cont_forms').className = "cont_forms cont_forms_active_login";  
	document.querySelector('.cont_form_login').style.display = "block";
	document.querySelector('.cont_form_sign_up').style.opacity = "0";
	document.querySelector('.cont_form_forgot').style.opacity = "0";                 

	setTimeout(function(){  document.querySelector('.cont_form_login').style.opacity = "1"; },100);  
  
	setTimeout(function(){    
	document.querySelector('.cont_form_sign_up').style.display = "none";
	document.querySelector('.cont_form_forgot').style.display = "none";
	},200);  
}

function return_login()
{
	document.querySelector('.cont_forms').className = "cont_forms cont_forms_active_login";  
	document.querySelector('.cont_form_login').style.display = "block";
	document.querySelector('.cont_form_sign_up').style.opacity = "0";
	document.querySelector('.cont_form_forgot').style.opacity = "0";                 

	setTimeout(function(){  document.querySelector('.cont_form_login').style.opacity = "1"; },400);  
  
	setTimeout(function(){    
	document.querySelector('.cont_form_sign_up').style.display = "none";
	document.querySelector('.cont_form_forgot').style.display = "none";
	},500);  
}

function actvate_forgot()
{
	document.querySelector('.cont_forms').className = "cont_forms cont_forms_active_login";  
	document.querySelector('.cont_form_forgot').style.display = "block";
	document.querySelector('.cont_form_sign_up').style.opacity = "0";
	document.querySelector('.cont_form_login').style.opacity = "0";


	setTimeout(function(){  document.querySelector('.cont_form_forgot').style.opacity = "1"; },400);  
  
	setTimeout(function(){
	document.querySelector('.cont_form_login').style.display = "none";
	},500);  
}

function activate_sign_up()
{
	document.querySelector('.cont_forms').className = "cont_forms cont_forms_active_sign_up";
	document.querySelector('.cont_form_sign_up').style.display = "block";
	document.querySelector('.cont_form_login').style.opacity = "0";
	document.querySelector('.cont_form_forgot').style.opacity = "0";
  
	setTimeout(function(){
		document.querySelector('.cont_form_sign_up').style.opacity = "1";
		},100);  

	setTimeout(function(){
		document.querySelector('.cont_form_login').style.display = "none";
		document.querySelector('.cont_form_forgot').style.display = "none";
		},400);  
}    



function ocultar_login_sign_up() {

document.querySelector('.cont_forms').className = "cont_forms";  
document.querySelector('.cont_form_sign_up').style.opacity = "0";               
document.querySelector('.cont_form_login').style.opacity = "0"; 

setTimeout(function(){
document.querySelector('.cont_form_sign_up').style.display = "none";
document.querySelector('.cont_form_login').style.display = "none";
document.querySelector('.cont_form_forgot').style.display = "none";
},500);  
  
}

// $(document).mouseup(function (e)
// {
// 		var div = $("#form");
// 		var div2 = $("#forms_wrap");
// 		if (!div.is(e.target) && div.has(e.target).length === 0
// 			&& !div2.is(e.target) && div2.has(e.target).length === 0)
// 		{
// 			ocultar_login_sign_up();
// 		}
// });

$(document).on('submit', '#login_form', function(e){
	e.preventDefault();
	$.ajax({
    	type:"POST",
    	url: '/ajax_login',
		data: {login: document.getElementById('id_login').value,
			password: document.getElementById('id_password').value,
			csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
		},
    	success: function(response){
        	alert(response);
    	}
	});
});

$(document).on('submit', '#login_forgot', function(e){
    const forgot_email = document.getElementById('forgot_email');
    const recover_btn = document.getElementById('recover_btn');
    forgot_email.classList.remove('unvalid');
    recover_btn.disabled = true;

	$.ajax({
    	type:"POST",
    	url: '/ajax_reset',
		data: {email: forgot_email.value,
			csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
		},
    	success: function(response){
    		if (response != "error"){
    		    console.log(response);
                $(".col_md_login").addClass("none");
                $(".col_md_sign_up").addClass("none");
                const col_md_recover = $(".col_md_recover");
                col_md_recover.removeClass("none");
                $("#go_to_recover_btn").attr('href', response);
                ocultar_login_sign_up();

                setTimeout(function(){
	                col_md_recover.addClass("visible");
	            },300);
            }
			else
            {
                forgot_email.classList.add('unvalid');
                recover_btn.disabled = false;
            }

		}
	});
	e.preventDefault();
});

$(document).on('submit', '#register_form', function(e){
    const login = document.getElementById('register_login');
    const email = document.getElementById('register_email');
    const first_name = document.getElementById('register_first_name');
    const last_name = document.getElementById('register_last_name');
    const register_pwd_1 = document.getElementById('register_pwd_1');
    const register_pwd_2 = document.getElementById('register_pwd_2');
    const register_btn = document.getElementById('register_btn');

    register_btn.disabled = true;
    login.classList.remove('unvalid');
    email.classList.remove('unvalid');
    first_name.classList.remove('unvalid');
    last_name.classList.remove('unvalid');
    register_pwd_1.classList.remove('unvalid');
    register_pwd_2.classList.remove('unvalid');

	e.preventDefault();
	$.ajax({
    	type:"POST",
    	url: '/ajax_register',
		data: {login: login.value,
            email: email.value,
			first_name: first_name.value,
			last_name: last_name.value,
			pwd1: register_pwd_1.value,
			pwd2: register_pwd_2.value,
			csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
		},
    	success: function(response){
            register_btn.disabled = false;
            if (response.includes("error_login"))
                login.classList.add('unvalid');
            if (response.includes("error_email"))
                email.classList.add('unvalid');
            if (response.includes("error_first_name"))
                first_name.classList.add('unvalid');
            if (response.includes("error_last_name"))
                last_name.classList.add('unvalid');
            if (response.includes("error_pwd"))
            {
                register_pwd_1.classList.add('unvalid');
                register_pwd_2.classList.add('unvalid');
            }
            if (response.includes("success")){
                $(".col_md_login").addClass("none");
                $(".col_md_sign_up").addClass("none");
                const col_md_succses = $(".col_md_succses");
                col_md_succses.removeClass("none");
                $("#go_to_email_btn").attr('href', response[1]);
                ocultar_login_sign_up();

                setTimeout(function(){
	                col_md_succses.addClass("visible");
	            },300);
            }
    	}
	});

});

$("#register_pwd_1").on("change paste keyup", function(key) {
	let str = $('#register_pwd_1').val();
	let complexity = 0;
	let len = str.length;
	let upper = 0;
	let lower = 0;
	let num = 0;

	if (len < 20){
		complexity += 40*(len/20);
	}
	else{
		complexity += 40;
	}

    for (let i = 0; i < len; i++) {
		let charCode = str.charCodeAt(i);
		if (charCode >= 65 && charCode <=90){
			upper++;
		}
		else if (charCode >= 97 && charCode <=122){
			lower++;
		}
		else if (charCode >= 48 && charCode <=57) {
            num++;
        }
    }
    if (upper < 5){
		complexity += 20*(upper/5);
	}
	else{
		complexity += 20;
	}
	if (lower < 5){
		complexity += 20*(lower/5);
	}
	else{
		complexity += 20;
	}
	if (num < 5){
		complexity += 20*(num/5);
	}
	else{
		complexity += 20;
	}
	$(".pwd_over").width(100 - complexity + "%");
});