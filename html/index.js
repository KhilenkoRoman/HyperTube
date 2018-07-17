/* ------------------------------------ Click on login and Sign Up to  changue and view the effect
---------------------------------------
*/

function cambiar_login()
{
	document.querySelector('.cont_forms').className = "cont_forms cont_forms_active_login";  
	document.querySelector('.cont_form_login').style.display = "block";
	document.querySelector('.cont_form_sign_up').style.opacity = "0";               

	setTimeout(function(){  document.querySelector('.cont_form_login').style.opacity = "1"; },400);  
  
	setTimeout(function(){    
	document.querySelector('.cont_form_sign_up').style.display = "none";
	},200);  
}

function cambiar_sign_up(at)
{
	// alert("1");
	document.querySelector('.cont_forms').className = "cont_forms cont_forms_active_sign_up";
	document.querySelector('.cont_form_sign_up').style.display = "block";
	document.querySelector('.cont_form_login').style.opacity = "0";
  
	setTimeout(function(){
		document.querySelector('.cont_form_sign_up').style.opacity = "1";
		},100);  

	setTimeout(function(){
		document.querySelector('.cont_form_login').style.display = "none";
		},400);  
}    



function ocultar_login_sign_up() {

document.querySelector('.cont_forms').className = "cont_forms";  
document.querySelector('.cont_form_sign_up').style.opacity = "0";               
document.querySelector('.cont_form_login').style.opacity = "0"; 

setTimeout(function(){
document.querySelector('.cont_form_sign_up').style.display = "none";
document.querySelector('.cont_form_login').style.display = "none";
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