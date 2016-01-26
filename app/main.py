import cgi
import json
import re
from sys import path

path.append('/home/server/vm_genesis/lib/python3.4/site-packages/')
path.append('/home/server/project/genesis_contabilidad/')

from pony.orm import *

from app.core.contabilidad.controller import *
from app.core.security.controller import *

def cast_get(string):
	out = {}
	if string != '':
		if string.find('&')>0:
			get = string.split('&')
			for value in get:
				par = value.split('=')
				out[par[0]] = par[1]
		else:
			par = string.split('=')
			out[par[0]] = par[1]
	return out		
def cast_post(environ):
	out = {}
	post_env = environ.copy()
   	post_env['QUERY_STRING'] = ''
   	post = cgi.FieldStorage(fp=environ['wsgi.input'], environ=post_env, keep_blank_values=True)
	for encabezado in post:
		if encabezado.find('{')>0 and encabezado.find('}')>0:
			out[encabezado] = eval(post[encabezado].value)
		else:
			out[encabezado]= post[encabezado].value
	return out
def cast_cookie(environ):
	cookies = {}
	str_cookies = environ.get('HTTP_COOKIE', '')
	if str_cookies != '':
		arr_cookies = str_cookies.split(',')
		for par in arr_cookies:
			var = par.split('=')
			cookies[var[0]] = var[1]
	return cookies

def validate_session(environ,cookie):
	token = cookie['token']
	parametros = {values: {token: token, estatus: '1'}, col: ['mac','ip','estatus','usuario','finaliza']}
	session = ControllerSession()
	respuesta = session.find(parametros)


def application(environ, start_response):
	ext_img = ['png','jpg','jpeg', 'gif']
	formato = 'text/html'
	status = '200 OK'
	cookies = cast_cookie(environ)
	usuario = '-1'
	token = ''
	if 'genesis_token' in cookies:
		session = ControllerSession()
		usuario = session.validate_session(environ['REMOTE_ADDR'],environ['HTTP_USER_AGENT'],cookies['genesis_token'])	
		token = cookies['genesis_token']
	output = ''
	if environ['PATH_INFO'] == "/":
		ruta_view = '/home/server/project/genesis_contabilidad/app/core/view/themes/black_red_software/skeleton.html'
		archivo = open(ruta_view, "r")
		output = archivo.read()	
		output = output.replace('CONTENIDO_PAGINA', 'Pagina de Inicio')
		menu = traer_menu(usuario = usuario)
		output = output.replace('MENU-PAGINA', menu)
		#output = 'Pagina Inicio'
	elif environ['PATH_INFO'].find('.') > 0:
		path_info = environ['PATH_INFO']
		ruta_view = '/home/server/project/genesis_contabilidad/public/librerias/'+path_info
		try:
			archivo = open(ruta_view, "r")
		except Exception, e:
			output += 'Page not found'
			status = '404 Not Found'
		else:
			output = archivo.read()
			if path_info[-3:] == 'css':
				formato = 'text/css'
			elif path_info[-3:] in ext_img:
				formato = 'img/'+path_info[-3:]	
	else:
		str_peticion = ''
		get = cast_get(str(environ['QUERY_STRING']))
		post = cast_post(environ)
		valores = post.copy()
		valores.update(get)
		valores.update({'_user_genesis': usuario, '_token_genesis': token})	
		acceso = True
		try:
			path_info = environ['PATH_INFO']
			if path_info[-1] == '/':
				path_info = path_info[:-1]
			peticion = path_info.split('/')
			obj_sec = eval('Controller'+peticion[1]+'()')
			if obj_sec.accesos.get(peticion[-1], '') != '':
				acceso = False
				security = ControllerSecurity()
				if int(usuario) > 0:
					acceso = security.validate_access(usuario, obj_sec.accesos.get(peticion[-1]))	
				if acceso == False:
					output = 'No tiene acceso a este lugar'
			if acceso == True:
				for pt_peticion in peticion[1:]:
					if pt_peticion != "":
						str_peticion += pt_peticion+'().'
				str_peticion = str_peticion[:-3]
				funcion = eval('Controller'+str_peticion)
				if peticion[-1] == 'validate_credentials':
					valores.update({'ip_ext': environ['REMOTE_ADDR'], 'navegador_ext': environ['HTTP_USER_AGENT']})
				output = funcion(**valores)
				menu = traer_menu(usuario = usuario)
				output = output.replace('MENU-PAGINA', menu)
			
		except Exception, e:
			output = 'Pagina no existe: '+str(peticion)+', pagina inicio '+str(e)

	if type(output) is not str:
		output = str(output)
		
	response_headers = [('Content-type', formato), ('Content-Length', str(len(output)))]
	start_response(status, response_headers)
	return output
@db_session
def traer_menu(padre_ext = None, usuario = ''):
	security = ControllerSecurity()
	cdb = Database()
	if padre_ext is None:
		salida = '<ul class="nav">'
	else:
		salida = '<ul>'
	menus = select('m for m in Menu if m.padre.id is '+str(padre_ext)+' and m.estado is 1').order_by(Menu.posicion)[:]
	if menus is not None:
		for menu in menus:
			acceso = True
			try:
				#salida += '<li>'+usuario+', '+menu.acceso.clave+'</li>'
				acceso = security.validate_access(usuario, menu.acceso.clave)
			except Exception, e:
				pass
			if acceso is True:
				salida += '<li><a href="'+str(menu.url)+'" >'+menu.titulo+'</a>'
				salida += traer_menu(menu.id, usuario)
				salida += '</li>'

	salida += '</ul>'
	return salida
