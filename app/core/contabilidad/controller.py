import datetime
from app.core.contabilidad.model import *
from app.core.ControllerGeneric import *
from app.core.FormGeneric import Formulario

class ControllerTipoActividad(ControllerGeneric):
	cdb = Database()
	model = TipoActividad
	col_view = {'insert': ['titulo'], 'update': ['id','titulo','estatus'], 'delete':['id','titulo']}
	col_view['find'] = ['id','titulo']
	accesos = {'insert': 'ins_tipo_actividad'}

class ControllerCuenta(ControllerGeneric):
	cdb = Database()
	model = Cuenta
	col_view = {'insert': ['titulo', 'monto'], 'update': ['id','titulo', 'monto'], 'delete':['id','titulo']}
	col_view['find'] = ['id','titulo', 'monto']
	accesos = {'insert': 'ins_cuenta'}

class ControllerAgrupador(ControllerGeneric):
	cdb = Database()
	model = Agrupador
	col_view = {'insert': ['titulo'], 'update': ['id','titulo','estatus'], 'delete':['id','titulo']}
	col_view['find'] = ['id','titulo']
	accesos = {'insert': 'ins_agrupador'}

class ControllerIngreso(ControllerGeneric):
	cdb = Database()
	model = Ingreso
	col_view = {'insert': ['fecha_referencia','identificador_documento','tipo_actividad','observacion', 'monto', 'agrupador', 'cuenta'], 'update': ['id','fecha_referencia','identificador_documento','tipo_actividad','observacion', 'monto', 'agrupador', 'cuenta','estatus'], 'delete':['id','fecha_referencia','identificador_documento','observacion','tipo_actividad', 'monto', 'agrupador', 'cuenta',]}
	col_view['find'] = ['id','tipo_actividad', 'observacion', 'monto', 'agrupador', 'cuenta']
	accesos = {'insert': 'ins_ingreso'}

class ControllerEgreso(ControllerGeneric):
	cdb = Database()
	model = Egreso
	col_view = {'insert': ['fecha_referencia','identificador_documento','tipo_actividad','observacion', 'monto', 'agrupador', 'cuenta'], 'update': ['id','fecha_referencia','identificador_documento','tipo_actividad','observacion', 'monto', 'agrupador', 'cuenta','estatus'], 'delete':['id','fecha_referencia','identificador_documento','observacion','tipo_actividad', 'monto', 'agrupador', 'cuenta',]}
	col_view['find'] = ['id', 'tipo_actividad', 'observacion', 'monto', 'agrupador', 'cuenta']
	accesos = {'insert': 'ins_egreso'}

class ControllerTraslado(ControllerGeneric):
	accesos = {'insert': 'ins_egreso'}
	col_view = {'find': ['id', 'observacion', 'monto', 'usuario']}
	model = Traslado
	ruta_tema = 'app/core/view/themes/black_red_software/skeleton.html'
	cdb = Database()
	@db_session
	def insert(self,**data):
		if 'values' in data:
			if type(data.get('values')) is not dict:
				values = eval(data.get('values'))
			else:
				values = data.get('values')
			if '_user_genesis' in data:
				values['usuario'] = data.get('_user_genesis')
			for value in values:
				if values[value] == '':
					if type(eval('self.model.'+value)) is not str:
						values[value] = None
				
			try:
				id_traslado = TipoActividad.get(titulo='Traslado')
				if id_traslado is not None:
					datos = {}
					datos['cuenta'] =  cuenta=values.get('cuenta_origen','')
					datos['monto'] = values.get('monto','')
					datos['observacion'] = values.get('observacion', '')
					datos['tipo_actividad'] = id_traslado
					datos['usuario'] = values.get('usuario','')
					egreso = Egreso(**datos)
					datos['cuenta'] =  cuenta=values.get('cuenta_destino','')
					ingreso = Ingreso(**datos)
					flush()
					if ingreso.id > 0 and egreso.id >0:
						datos = {}
						datos['ingreso'] = ingreso.id
						datos['egreso'] = egreso.id
						datos['usuario'] = values.get('usuario','')
						datos['monto'] = values.get('monto','')
						datos['observacion'] = values.get('observacion', '')
						traslado = Traslado(**datos)
						flush()
						if traslado.id>0:
							commit()
						else:
							rollback()
					else:
						rollback()

					res = {'cod': '1', 'msj': 'Insert Ok'}
			except Exception, e:
				rollback()
				res = {'cod': '0', 'msj': str(e)}
			return json.dumps(res, ensure_ascii=False)	
		else:
			dict_formulario = []
			dict_formulario.append({'name': 'cuenta_origen', 'tipo': 'Cuenta'})
			dict_formulario.append({'name': 'cuenta_destino', 'tipo': 'Cuenta'})
			dict_formulario.append({'name': 'monto', 'tipo': 'Decimal'})
			dict_formulario.append({'name': 'observacion', 'tipo': 'str', 'size': '1000'})
			
			formulario = Formulario()
			template = formulario.cargar_pagina(self.ruta_tema)
			view_form = formulario.diccionario(dict_formulario)
			output = template.replace('CONTENIDO_PAGINA', view_form)
			output = output.replace('ACCION-FORMULARIO', 'insert')
			output = output.replace('TITULO-PAGINA', 'Ingresar Traslado')
			output = output.replace('OBJETO-FORMULARIO', 'Traslado')
			return output
	@db_session
	def anular(self, **data):	
		if 'values' in data:
			if type(data.get('values')) is not dict:
				values = eval(data.get('values'))
			else:
				values = data.get('values')
			if '_user_genesis' in data:
				values['usuario'] = data.get('_user_genesis')
			for value in values:
				if values[value] == '':
					if type(eval('self.model.'+value)) is not str:
						values[value] = None
				
			try:
				traslado = Traslado[values.get('id')]
				if traslado is not None:
					ingreso = traslado.ingreso
					egreso = traslado.egreso
					ingreso.estatus = 0
					egreso.estatus = 0
					flush()
					traslado.estatus = '0'
					traslado.observacion = str(ingreso.observacion)+values.get('observacion')
					commit()
					res = {'cod': '1', 'msj': 'Anulacion Ok'}
				else:
					res = {'cod': '0', 'msj': 'No existe identificador'}	
			except Exception, e:
				rollback()
				res = {'cod': '0', 'msj': str(e)}
			return json.dumps(res, ensure_ascii=False)	
		else:
			dict_formulario = []
			dict_formulario.append({'name': 'Codigo', 'tipo': 'Traslado', 'identificador': 'id'})
			dict_formulario.append({'name': 'observacion', 'tipo': 'str', 'size': '1000'})
			
			formulario = Formulario()
			template = formulario.cargar_pagina(self.ruta_tema)
			view_form = formulario.diccionario(dict_formulario)
			output = template.replace('CONTENIDO_PAGINA', view_form)
			output = output.replace('ACCION-FORMULARIO', 'anular')
			output = output.replace('TITULO-PAGINA', 'Anular Traslado')
			output = output.replace('OBJETO-FORMULARIO', 'Traslado')
			return output

class ControllerReporte():
	accesos = {}
	ruta_tema = 'app/core/view/themes/black_red_software/skeleton.html'
	@db_session
	def cuentas(self, **data):
		if 'values' in data:
			rev_values = {}
			if type(data.get('values')) is not dict:
				values = eval(data.get('values'))
			else:
				values = data.get('values')
			for value in values:
				if values[value] != '':
					rev_values[value] = values[value]
			try:
				str_select = 'p for p in Ingreso '
				if 'cuenta' in rev_values:
					str_select += ' if p.cuenta.id == '+str(rev_values['cuenta'])
				str_select += ' if p.estatus is 1'
				resultado_ingreso = select(str_select).order_by(Ingreso.cuenta, Ingreso.fecha_referencia)[:]
				str_select = 'p for p in Egreso '
				if 'cuenta' in rev_values:
					str_select += ' if p.cuenta.id == '+str(rev_values['cuenta'])
				str_select += ' if p.estatus is 1'
				resultado_egreso = select(str_select).order_by(Egreso.cuenta, Egreso.fecha_referencia)[:]
				 
				encabezado  = '<div class="linea-encabezado-reporte">'
				encabezado += '<label class= "columna">ID</label>'
				encabezado += '<label class= "columna">Cuenta</label>'
				encabezado += '<label class= "columna">Observacion</label>'
				encabezado += '<label class= "columna">Ingresado</label>'
				encabezado += '<label class= "columna">Fecha Realizacion</label>'
				encabezado += '<label class= "columna">Credito</label>'
				encabezado += '<label class= "columna">Debito</label>'
				encabezado += '<label class= "columna">Saldo</label>'
				encabezado += '</div>'
				salida = ''
				arreglo_final = []
				for ingreso in resultado_ingreso:
					arreglo_final.append(ingreso)
				for egreso in resultado_egreso:
					egreso.egreso = True
					arreglo_final.append(egreso)
				cuentas = []
				for obj in arreglo_final:
					if obj.cuenta.titulo not in cuentas:
						cuentas.append(obj.cuenta.titulo)
				orden_cuenta = []
				for cuenta in cuentas:
					for obj in arreglo_final:
						if obj.cuenta.titulo == cuenta:
							orden_cuenta.append(obj)
				
				cuenta = ''
				total_cuenta = None
				for linea in orden_cuenta:
					if cuenta is not linea.cuenta.titulo:
						if total_cuenta is not None:
							salida += '<div class="linea-final-reporte">'
							salida += '<label>Total cuenta</label><label>'+str(total_cuenta)+'</label>'
							salida += '</div>'
							salida += '<div class="linea-subencabezado-reporte"><label>Cuenta: '+linea.cuenta.titulo+'</label></div>'
							salida += encabezado
						else:
							salida += '<div class="linea-subencabezado-reporte"><label>Cuenta: '+linea.cuenta.titulo+'</label></div>'
							salida += encabezado
						cuenta = linea.cuenta.titulo
						total_cuenta = 0
						
					
					salida += '<div class="linea-reporte">'
					salida += '<label class= "columna">'+str(linea.id)+'</label>'
					salida += '<label class= "columna">'+str(linea.cuenta.titulo)+'</label>'
					salida += '<label class= "columna">'+str(linea.observacion)+'</label>'
					salida += '<label class= "columna">'+str(linea.creado)+'</label>'
					salida += '<label class= "columna">'+str(linea.fecha_referencia)+'</label>'
					
					
					try:
						egreso = linea.egreso
						salida += '<label class= "columna"></label><label class="columna">'+str(linea.monto)+'</label>'
						total_cuenta -= linea.monto
					except Exception, e:
						salida += '<label class= "columna">'+str(linea.monto)+'</label><label class="columna"></label>'
						total_cuenta += linea.monto					
					salida += '<label class= "columna">'+str(total_cuenta)+'</label>'
					salida += '</div>'
				salida += '<div class="linea-final-reporte">'
				salida += '<label>Total cuenta</label><label>'+str(total_cuenta)+'</label>'
				salida += '</div>'
					
				res = {'cod': '1', 'msj': salida}
			except Exception, e:
				res = {'cod': '0', 'msj': str(e)}
			return json.dumps(res, ensure_ascii=False)
		else:
			dict_formulario = []
			dict_formulario.append({'name': 'cuenta', 'tipo': 'Cuenta'})
			formulario = Formulario()
			template = formulario.cargar_pagina(self.ruta_tema)
			view_form = formulario.diccionario(dict_formulario)
			output = template.replace('CONTENIDO_PAGINA', view_form)
			output = output.replace('ACCION-FORMULARIO', 'cuentas')
			output = output.replace('OBJETO-FORMULARIO', 'Reporte')
			output = output.replace('TITULO-PAGINA', ' Reporte de cuentas')
			output = output.replace('boton_ejecutar', 'boton_ejecutar_reporte')
			return output
	@db_session
	def ingresos(self, **data):
		if 'values' in data:
			rev_values = {}
			if type(data.get('values')) is not dict:
				values = eval(data.get('values'))
			else:
				values = data.get('values')
			for value in values:
				if values[value] != '':
					rev_values[value] = values[value]
			try:
				str_select = 'p for p in Ingreso '
				if 'inicio' in rev_values:
					str_select += ' if creado >= '+str(rev_values['inicio'])
					if 'fin' in rev_values:
						str_select += ' and creado <= '+str(rev_values['fin'])
				if 'tipo_actividad' in rev_values:
					str_select += ' if tipo_actividad is '+str(rev_values['tipo_actividad'])
				if 'cuenta' in rev_values:
					str_select += ' if cuenta is '+str(rev_values['cuenta'])
				if 'agrupador' in rev_values:
					str_select += ' if agrupador is '+str(rev_values['agrupador'])
				resultado = select(str_select)[:]
				salida = self.formato_ingreso_egreso(resultado)
				res = {'cod': '1', 'msj': salida}
			except Exception, e:
				res = {'cod': '0', 'msj': str(e)}
			return json.dumps(res, ensure_ascii=False)
		else:
			dict_formulario = []
			dict_formulario.append({'identificador': 'inicio', 'name': 'Fecha Inicio', 'tipo': 'datetime'})
			dict_formulario.append({'identificador': 'fin', 'name': 'Fecha Fin', 'tipo': 'datetime'})
			dict_formulario.append({'name': 'tipo_actividad', 'tipo': 'TipoActividad'})
			dict_formulario.append({'name': 'cuenta', 'tipo': 'Cuenta'})
			dict_formulario.append({'name': 'agrupador', 'tipo': 'Agrupador'})
			formulario = Formulario()
			template = formulario.cargar_pagina(self.ruta_tema)
			view_form = formulario.diccionario(dict_formulario)
			output = template.replace('CONTENIDO_PAGINA', view_form)
			output = output.replace('ACCION-FORMULARIO', 'ingresos')
			output = output.replace('OBJETO-FORMULARIO', 'Reporte')
			output = output.replace('TITULO-PAGINA', ' Reporte de Ingresos')
			output = output.replace('boton_ejecutar', 'boton_ejecutar_reporte')
			return output

	@db_session
	def egresos(self, **data):
		if 'values' in data:
			rev_values = {}
			if type(data.get('values')) is not dict:
				values = eval(data.get('values'))
			else:
				values = data.get('values')
			for value in values:
				if values[value] != '':
					rev_values[value] = values[value]
			try:
				str_select = 'p for p in Egreso '
				if 'inicio' in rev_values:
					str_select += ' if creado >= '+str(rev_values['inicio'])
					if 'fin' in rev_values:
						str_select += ' and creado <= '+str(rev_values['fin'])
				if 'tipo_actividad' in rev_values:
					str_select += ' if tipo_actividad is '+str(rev_values['tipo_actividad'])
				if 'cuenta' in rev_values:
					str_select += ' if cuenta is '+str(rev_values['cuenta'])
				if 'agrupador' in rev_values:
					str_select += ' if agrupador is '+str(rev_values['agrupador'])
				resultado = select(str_select)[:]
				salida = self.formato_ingreso_egreso(resultado)
				res = {'cod': '1', 'msj': salida}
			except Exception, e:
				res = {'cod': '0', 'msj': str(e)}
			return json.dumps(res, ensure_ascii=False)
		else:
			dict_formulario = []
			dict_formulario.append({'identificador': 'inicio', 'name': 'Fecha Inicio', 'tipo': 'datetime'})
			dict_formulario.append({'identificador': 'fin', 'name': 'Fecha Fin', 'tipo': 'datetime'})
			dict_formulario.append({'name': 'tipo_actividad', 'tipo': 'TipoActividad'})
			dict_formulario.append({'name': 'cuenta', 'tipo': 'Cuenta'})
			dict_formulario.append({'name': 'agrupador', 'tipo': 'Agrupador'})
			formulario = Formulario()
			template = formulario.cargar_pagina(self.ruta_tema)
			view_form = formulario.diccionario(dict_formulario)
			output = template.replace('CONTENIDO_PAGINA', view_form)
			output = output.replace('ACCION-FORMULARIO', 'egresos')
			output = output.replace('OBJETO-FORMULARIO', 'Reporte')
			output = output.replace('TITULO-PAGINA', ' Reporte de egresos')
			output = output.replace('boton_ejecutar', 'boton_ejecutar_reporte')
			return output
			
	def formato_ingreso_egreso(self, resultado):
		salida = '<div class="linea-encabezado-reporte">'
		salida += '<label class= "columna">ID</label>'
		salida += '<label class= "columna">Actividad</label>'
		salida += '<label class= "columna">Fecha Realizacion</label>'
		salida += '<label class= "columna">Documento</label>'
		salida += '<label class= "columna">Observacion</label>'
		salida += '<label class= "columna">Agrupador</label>'
		salida += '<label class= "columna">Cuenta</label>'
		salida += '<label class= "columna">Ingresado</label>'
		salida += '<label class= "columna">Usuario</label>'
		salida += '<label class= "columna">Monto</label>'
		salida += '</div>'
		
		total = 0;
		for p in resultado:
			salida += '<div class="linea-reporte">'
			salida += '<label class= "columna">'+str(p.id)+'</label>'
			salida += '<label class= "columna">'+str(p.tipo_actividad.titulo)+'</label>'
			salida += '<label class= "columna">'+str(p.fecha_referencia)+'</label>'
			salida += '<label class= "columna">'+str(p.identificador_documento)+'</label>'
			salida += '<label class= "columna">'+str(p.observacion)+'</label>'
			
			salida += '<label class= "columna">'
			if p.agrupador is None:
				salida += 'Null'
			else:
				salida += p.agrupador.titulo
			salida +='</label>'
			salida += '<label class= "columna">'+str(p.cuenta.titulo)+'</label>'
			salida += '<label class= "columna">'+str(p.creado)+'</label>'
			salida += '<label class= "columna">'+str(p.usuario)+'</label>'
			salida += '<label class= "columna">'+str("{:,}".format(p.monto))+'</label>'
			salida += '</div>'
			total += Decimal(p.monto)
		
		salida += '<div class="linea-final-reporte">'
		salida += '<label class="columna-6">Total de Ingresos</label><label>Q. '+"{:,}".format(total)+'</label>'
		salida += '</div>' 

		return salida