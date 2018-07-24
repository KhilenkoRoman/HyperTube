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

$(document).mouseup(function (e)
{
		var div = $("#form"); 
		var div2 = $("#forms_wrap");
		if (!div.is(e.target) && div.has(e.target).length === 0 
			&& !div2.is(e.target) && div2.has(e.target).length === 0)
		{
			ocultar_login_sign_up();
		}
});




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
	$.ajax({
    	type:"POST",
    	url: '/ajax_reset',
		data: {email: document.getElementById('forgot_email').value,
			csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
		},
    	success: function(response){
    		if (response === "sucsess")
			{
				document.getElementById('login_forgot').submit();
			}
    		console.log("1");
		}
	});
	e.preventDefault();
});

$(document).on('submit', '#register_form', function(e){
	e.preventDefault();
	$.ajax({
    	type:"POST",
    	url: '/ajax_register',
		data: {login: document.getElementById('register_login').value,
    		email: document.getElementById('register_email').value,
			pwd1: document.getElementById('register_pwd_1').value,
			pwd2: document.getElementById('register_pwd_2').value,
			csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
		},
    	success: function(response){
    		console.log(response);
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