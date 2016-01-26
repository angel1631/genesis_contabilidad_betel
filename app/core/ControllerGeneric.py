import json
from datetime import datetime, date
from pony.orm import *
from app.core.FormGeneric import Formulario

class ControllerGeneric():
	error = ''
	accesos = {'insert': '', 'update': '', 'delete': '', 'search': ''}
	ruta_tema = 'app/core/view/themes/black_red_software/skeleton.html'
	@db_session
	def insert(self, **data):
		#user = -1
			
		if 'values' in data:
			if type(data.get('values')) is not dict:
				values = eval(data.get('values'))
			else:
				values = data.get('values')
				
			if '_user_genesis' in data:
				obj_adict = self.model._adict_
				if 'usuario' in obj_adict:
					values['usuario'] = data.get('_user_genesis')
		
			try:
				for value in values:
					if values[value] == '':
						if eval('self.model.'+value+'.default') != '':
							values[value] = eval('self.model.'+value+'.default')
						else:
							tipo_value = type(eval('self.model.'+value+'.py_type.__name__'))
							if tipo_value is not str:
								values[value] = None
				model = self.model(**values)
				commit()
				res = {'cod': '1', 'msj': 'Insert Ok'}
			except Exception, e:
				res = {'cod': '0', 'msj': str(e)}
			return json.dumps(res, ensure_ascii=False)	
		else:
			formulario = Formulario()
			view_form = formulario.modelo(self.model,self.col_view['insert'])
			template = formulario.cargar_pagina(self.ruta_tema)
			output = template.replace('CONTENIDO_PAGINA', view_form)
			output = output.replace('ACCION-FORMULARIO', 'insert')
			output = output.replace('TITULO-PAGINA', ' Insertar '+str(self.model.__name__))
			output = output.replace('OBJETO-FORMULARIO', str(self.model.__name__))
			return output
	@db_session	
	def update(self, **data):
		if 'values' in data:
			if type(data.get('values')) is not dict:
				values = eval(data.get('values'))
			else:
				values = data.get('values')
			try:
				model = self.model[values['id']]
				model.set(**values)
				commit()
				res = {'cod': '1', 'msj': 'Update Ok'}
			except Exception, e:
				res = {'cod': '0', 'msj': str(e)}
			return json.dumps(res, ensure_ascii=False)
		else:
			formulario = Formulario()
			view_form = formulario.modelo(self.model,self.col_view['update'])
			template = formulario.cargar_pagina(self.ruta_tema)
			output = template.replace('CONTENIDO_PAGINA', view_form)
			output = output.replace('ACCION-FORMULARIO', 'update')
			output = output.replace('TITULO-PAGINA', ' Actualizar '+str(self.model.__name__))
			output = output.replace('OBJETO-FORMULARIO', str(self.model.__name__))
			return output

	@db_session
	def delete(self, **data):
		if 'values' in data:
			if type(data.get('values')) is not dict:
				values = eval(data.get('values'))
			else:
				values = data.get('values')
			try:
				model = self.model[values['id']].delete()
				commit()
				res = {'cod': '1', 'msj': 'Delelte Ok'}
			except Exception, e:
				res = {'cod': '0', 'msj': str(e)}
			return json.dumps(res, ensure_ascii=False)
		else:
			formulario = Formulario()
			view_form = formulario.modelo(self.model,self.col_view['delete'])
			template = formulario.cargar_pagina(self.ruta_tema)
			output = template.replace('CONTENIDO_PAGINA', view_form)
			output = output.replace('ACCION-FORMULARIO', 'delete')
			output = output.replace('TITULO-PAGINA', 'Eliminar '+str(self.model.__name__))
			output = output.replace('OBJETO-FORMULARIO', str(self.model.__name__))
			return output
		
	@db_session
	def find(self, **data):
		if 'values' in data:
			datos = {}
			rev_values = {}
			if type(data.get('values')) is not dict:
				values = eval(data.get('values'))
			else:
				values = data.get('values')
			for value in values:
				if values[value] != '':
					rev_values[value] = values[value]
			values = rev_values
			col_find = self.col_view['find']
			str_select = ''
			for col in col_find:
				if type(col) is dict:
					for c in col:
						enc = c
						if col[c].find(">") > 0:
							attr = col[c].split(">")
							enc = attr[0]+'.'+attr[1]
						str_select += 'p.'+enc+', '
				else:
					if col.find(">") > 0:
							attr = col.split(">")
							col = attr[0]
					str_select += 'p.'+col+', '
			model = self.model
			str_select = '('+(str_select[:-2])+') for p in model'
			restricciones = ''
			for value in values:
				if value == 'id':
					restricciones += "p."+value+" == "+str(values[value])+" and "
				else:
					restricciones += '"'+values[value]+'" in '+'p.'+str(value)+' and '
			if restricciones != '':
				str_select += ' if '+(restricciones[:-4])
			
			objeto = select(str_select)[:]
			tupla = {}
			datos = []
			if objeto is not None:
				
				for obj in objeto:
					pos = 0
					for columna in col_find:
						if type(columna) is dict:
							for col in columna:
								if columna[col].find(">") > 0:
									attr = columna[col].split(">")
									if not attr[0] in tupla:
										tupla[attr[0]] = {}
									try:
										tupla[attr[0]][col] = obj[pos]
									except Exception, e:
										tupla[attr[0]][col] = ''
								else:
									tupla[columna[col]][col] = obj[pos]
								pos += 1
						else:
							tupla[columna] = obj[pos]
							pos += 1
					datos.append(tupla)
					tupla = {}
				res = {'cod': '1', 'msj': str(datos)}
				
				#res = {'cod': '1', 'msj': str(objeto)}
			else:
				res = {'cod': '0', 'msj': 'No existe'}
			return json.dumps(res, ensure_ascii=False)
		else:
			if 'tema' in data:
				formulario = Formulario()
				output = formulario.modelo(self.model,self.col_view['find'])
			else:
				formulario = Formulario()
				view_form = formulario.modelo(self.model,self.col_view['find'])
				template = formulario.cargar_pagina(self.ruta_tema)
				output = template.replace('CONTENIDO_PAGINA', view_form)
			output = output.replace('TITULO-PAGINA', ' Busqueda '+str(self.model.__name__))
			output = output.replace('ACCION-FORMULARIO', 'find')
			output = output.replace('OBJETO-FORMULARIO', str(self.model.__name__))
			return output

		
	
