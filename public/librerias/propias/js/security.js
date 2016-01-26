
$("#boton-activador-form-login").click(function(){
	$("#contenedor-form-login").css("display", "block");
});

$("#boton-enviar-form-login").click(function(){
	$.ajax({
		type: 'POST',
		url: 'http://betel.solucionclic.com/Session/validate_credentials/',
		data: {usuario: $('#usuario-form-login').val(), password: $('#password-form-login').val()},
		dataType: 'json',
		success: function(e){
			if(e.cod=='1'){
				$.cookie('genesis_token',e.msj);
				$("#contenedor-form-login").css('display', 'none');
				location.reload();
			}
			else
				alert(e.msj)
		},error: function(){
			alert('Un error inesperado con el servidor comunicate con el administrador')
		}
	});
});