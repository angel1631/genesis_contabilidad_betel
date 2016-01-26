from app.core.contabilidad.model import *
from app.core.security.model import *
from pony.orm import *

class Formulario():
	def modelo(self,modelo,vista):
		view_form = '<div class="cf form-horizontal" obj="OBJETO-FORMULARIO" acc="ACCION-FORMULARIO">'
		for columna in vista:
			punter = columna
			if type(columna) is dict:
				for col in columna:
					if col.find(">") > 0:
						attr = col.split(">")
						punter = attr[0]
					else: 
						punter = columna[col] 
			if punter in modelo._adict_:
				identificador = ''
				tipo = eval('modelo.'+columna+'.py_type.__name__')
				default = eval('modelo.'+columna+'.default')
				extra = eval('modelo.'+columna+'.kwargs')
				name = eval('modelo.'+columna+'.name')
				size = extra.get('size', 100)
				if name is 'id':
					identificador = 'id'
					name = 'Codigo'
					tipo = modelo.__name__
				view_form += self.make_formulario(tipo,default,name,size,identificador)
		view_form += '<div class="boton_ejecutar btn btn-primary btn-lg btn-block" id="boton_ejecutar">Ejecutar</div></div>'
		return view_form
	def diccionario(self, diccionario):
		view_form = '<div class="cf form-horizontal" obj="OBJETO-FORMULARIO" acc="ACCION-FORMULARIO">'
		for elemento in diccionario:
			tipo = elemento.get('tipo', '')
			default = elemento.get('default','')
			identificador = elemento.get('identificador', '')
			name = elemento.get('name','')
			size = elemento.get('size',100)
			view_form += self.make_formulario(tipo,default,name,size, identificador)
		view_form += '<div class="boton_ejecutar btn btn-primary btn-lg btn-block" id="boton_ejecutar">Ejecutar</div></div>'
		return view_form

	def make_formulario(self,tipo,default,name, size, identificador = ''):
		if identificador == '':
			identificador = name
		view_form = ''
		view_form += '<div class="form-group" ><label class="col-sm-2 control-label">'+(name.capitalize()).replace('_', ' ')+'</label><div class="col-sm-10 dato">'
		if tipo == 'int':
			view_form += '<input type="number"  class="data form-control"  id="'+identificador+'" max-length="'+str(size)+'" />'
		elif tipo == 'str':
			if size < 250:
				view_form += '<input type="text"  class="data form-control"  id="'+identificador+'" max-length="'+str(size)+'" />'
			else:
				view_form += '<textarea  class="data form-control"  id="'+identificador+'"></textarea>'					
		elif tipo == 'datetime':
			view_form += '<input type="date"  class="data "  id="'+identificador+'" />'
		elif tipo == 'date':
			view_form += '<input type="date"  class="data "  id="'+identificador+'" />'
		elif tipo == 'Decimal':
			view_form += '<input type="number"  class="data "  id="'+identificador+'" />'
		else:
			try:
				buscar = False
				objetos = select(o for o in eval(tipo))[:]
				option = '<select class="data" id="'+identificador+'">'
				option += '<option value="">Seleccione una opcion</option>'
				if not objetos:
					pass 
					#option += '<option value="">No hay objetos de este tipo</option>'
				else:
					buscar = True
					for objeto in objetos:
						option += '<option value="'+str(objeto.id)+'">'+str(objeto.titulo)+'</option>'
				option += '</select>'
				if buscar is True:
					option += '<input obj="'+tipo+'" type="button" value="..." class="boton_buscar" />'
				view_form += option
			except Exception, e:
				view_form += '<input type="text"  class="data "  id="'+identificador+'" />'
				view_form += '<input obj="'+tipo+'" type="button" value="..." class="boton_buscar" />'
				#view_form += str(e)
		view_form += '</div></div>'
		return view_form

	def cargar_pagina(self, ruta):
		output = ""
		ruta_view = '/home/server/project/genesis_contabilidad/'+ruta
		try:
			archivo = open(ruta_view, "r")
			output = archivo.read()	
		except Exception, e:
			output = 'Page not found '+str(e)	
		return output

