$(document).ready(function(){
	var root = document.location.hostname;
	var path = document.location.href;
	path = path.split('?');
	variables = path[1];
	get = extraer_varibles_get(variables);
	set_acc(get);
	acc 		= '0';
	tb_activo 	= ''; 
	pt 			= $("#pt").attr("pat");
	//variables

	function set_acc(get){
		$(".cf").attr('acc', get['acc']);
	}
	function extraer_varibles_get(txt_variables_get){
		resultado = [];
		if (txt_variables_get != null){
			if(txt_variables_get.indexOf('&')>0){
				txt_variables_get = txt_variables_get.split('&');
				for(i = 0; i<txt_variables_get.length;i++){
					par = txt_variables_get[i].split('=');
					resultado[par[0]]= par[1];
				}
			}else{
				par = txt_variables_get.split('=');
				resultado[par[0]] = par[1];
			}
		}
		return resultado;
	}
	$(".opcion_abc").click(function(){
		acc = $(this).attr("acc");
		$.traer_vista_formulario();
	});
	$("body").on("click",".boton_ejecutar", function(){
		cf		= $(this).parent();
		obj		= cf.attr('obj');
		acc 	= cf.attr("acc");
		var dt_json = JSON.stringify($.extraer_datos_formulario(cf));
		enviar 	= {values: dt_json, acc: acc};	
		$.ajax({
			type: 'POST',
			data: enviar,
			url: 'http://'+root+'/'+obj+'/'+acc,
			dataType: 'json',
			success: function(res){
				if(res.cod==1){
					if(acc == 'find'){
						cf.html("");
						lineas = crear_lineas_busqueda(res.msj);
						if(lineas==""){
							alert("No hay registros para su busqueda");
							cf.parent().remove();
						}else{
							cf.html(lineas);
							cantidad_label = 0;
							cf.children(".titulo_linea_busqueda").children("label").each(function(){
								cantidad_label +=1;
							});
							cf.children(".titulo_linea_busqueda").children("label").css("width",(98/cantidad_label)+"%");
							cf.children(".linea_busqueda").children("label").css("width",(98/cantidad_label)+"%");	
						}	
					}else{
						alert(res.msj);
						$("input").each(function(){
							if($(this).attr('type')!='button')
								$(this).val("");
						});
						
						$("textarea").val("");
						$("select").val("");	
					}
				}else
					alert(res.msj);
			}, error: function(){
				alert("Error con el servidor, contactate con el administrador");
			}
		});
	});
	
	$("body").on("click",".boton_ejecutar_reporte", function(){
		cf		= $(this).parent();
		obj		= cf.attr('obj');
		acc 	= cf.attr("acc");
		var dt_json = JSON.stringify($.extraer_datos_formulario(cf));
		enviar 	= {values: dt_json, acc: acc};	
		$.ajax({
			type: 'POST',
			data: enviar,
			url: 'http://'+root+'/'+obj+'/'+acc,
			dataType: 'json',
			success: function(res){
				if(res.cod==1){
					if($("#contenedor-reporte").length)
						$("#contenedor-reporte").html("")
					else
						cf.parent().append('<div id="contenedor-reporte"></div>')
					$("#contenedor-reporte").html(res.msj)	
					cantidad_label = 0;
					$("#contenedor-reporte .linea-encabezado-reporte:first label").each(function(){
						cantidad_label +=1;
					});
					
					$("#contenedor-reporte .linea-reporte label").css("width",(98/cantidad_label)+"%")
					$("#contenedor-reporte .linea-encabezado-reporte label").css("width",(98/cantidad_label)+"%")
				}else
					alert(res.msj);
			}, error: function(){
				alert("Error con el servidor, contactate con el administrador");
			}
		});
	});
	function crear_lineas_busqueda(obj){
		encabezado = "";
		txt_linea = "";
		json = $.convert_string_json(obj);
		if(json.length == undefined)
			json = [json]
		for(i=0; i< json.length ; i++){
			txt_linea = txt_linea + "<div class=\"linea_busqueda\">";
			encabezado = "<div class=titulo_linea_busqueda>";
			$.each(json[i], function(puntero, valor){
				encabezado += "<label>"+puntero+"</label>";
				tipo = typeof valor
				if(tipo == 'object'){
					identificador = valor['id'];
					name = valor['name'];
				}else{
					identificador = valor
					name = valor
				}	
				txt_linea = txt_linea + '<label val="'+identificador+'" class="'+(puntero.toLowerCase()).replace(/ /g, "_")+'" >'+name+'</label>';
				
			});
			txt_linea += "</div>";
		}
		if(txt_linea != "")
			txt_linea = encabezado+"</div>"+txt_linea;
		return txt_linea;
	}
	$("body").on("click",".boton_ejecutar_form_archivo", function(){
		cf			= $(this).parent();
		tb_activo 	= cf.attr('tb');
		formdata = new FormData();
		if(acc=='0')
			acc = cf.attr("acc");
		
		var dt_json = JSON.stringify($.extraer_datos_formulario(cf));
		if(acc==1){
			formdata.append("datos",dt_json);
			formdata.append("acc",acc);
			var inputFileImage = document.getElementById("archivo");
			var file = inputFileImage.files[0];
			formdata.append("archivo",file);
			
		}else{
			if(acc==2){
				formdata.append("datos",dt_json);
				formdata.append("acc",acc);
				var inputFileImage = document.getElementById("archivo");
				var file = inputFileImage.files[0];
				formdata.append("archivo",file);
				formdata.append("codigo",cf.children(".form-group").children(".con_codigo").children(".codigo_principal").val());
				
			}else{
				formdata.append("acc",acc);
				formdata.append("codigo",cf.children(".form-group").children(".con_codigo").children(".codigo_principal").val());
				
			}
		}
		
		$.ajax({
			type: 'POST',
			data: formdata,
			url: 'http://'+root+'/modulos/'+tb_activo+'/controlador.php',
			cache: false,
            contentType: false,
            processData: false,
			dataType: 'json',
			success: function(res){
				if(res.codigo==1){
					alert(res.mensaje);
					cf.parent().html("");
				}else
					alert(res.mensaje);
			}
		});
	});
	$.convert_string_json = function(obj){
		obj = obj.replace(/ u'/g, "'");
		obj = obj.replace(/None/g, "''");
		obj = obj.replace(/Decimal\('/g, "('");
		obj = obj.replace(/\\/g, "");
		obj = obj.replace(/\,\)/g, ")");
		var json = JSON.stringify(eval("(" + obj + ")"));
		json = JSON.parse(json);
		return json;
	}
	$.extraer_datos_formulario = function(formulario){
		arr_datos 	= {};
		contenedor_foranea_multiple = {};
		y			= 0;
		formulario.children(".form-group").each(function(){
			if($(this).children(".dato").length){
				dato = $(this).children(".dato").children(".data"); 
				arr_datos[dato.attr("id")] = dato.val();	
			}else if ($(this).children(".linea-foranea-multiple").length){
				foranea_multiple 		= {};
				x 						= 0;
				foranea_multiple['tb'] 	= $(this).attr("tb");
				$(this).children(".linea-foranea-multiple").each(function(){
					if($(this).children(".codigo_foraneo").val()!=""){
						foranea_multiple[x]  = $(this).children(".codigo_foraneo").val(); 
						x++; 
					}
				});
				contenedor_foranea_multiple[y] = foranea_multiple;
				arr_datos['foranea_multiple'] = contenedor_foranea_multiple;
				y++;
			}
		});	
		return arr_datos;
	}
});