import datetime
import random
import string
import hashlib
from app.core.security.model import *
from app.core.ControllerGeneric import *
			
class ControllerUsuario(ControllerGeneric):
	model = Usuario
	col_view = {'insert': ['nombre', 'mail', 'password'], 'update': ['id', 'nombre', 'mail', 'password','estado'], 'delete':['id','nombre', 'mail']}
	
class ControllerRole(ControllerGeneric):
	model = Role
	col_view = {'insert': ['titulo'], 'update': ['id', 'titulo', 'estado'], 'delete':['id','titulo']}

class ControllerAcceso(ControllerGeneric):
	cdb = Database()
	model = Acceso
	col_view = {'insert': ['clave', 'obser'], 'update': ['id', 'clave', 'obser', 'estado'], 'delete':['id','clave','obser']}
	col_view['find'] = ['id', 'clave', 'obser', 'estado']
	
class ControllerRoleAcceso(ControllerGeneric):
	model = RoleAcceso
	col_view = {'insert': ['role','acceso'], 'update': ['id', 'role', 'acceso', 'estado'], 'delete':['id','role', 'acceso']}
	col_view['find'] = ['id', 'role', 'acceso', 'estado']

class ControllerUsuarioRole(ControllerGeneric):
	model = UsuarioRole
	col_view = {'insert': ['usuario','role'], 'update': ['id', 'usuario', 'role', 'estado'], 'delete':['id','usuario', 'role']}

class ControllerMenu(ControllerGeneric):
	model = Menu
	col_view = {'insert': ['titulo','padre', 'acceso', 'posicion', 'url'], 'update': ['id', 'titulo','padre', 'acceso', 'posicion', 'url', 'estado'], 'delete':['id','tiulo', 'url']}
	col_view['find'] = ['id', 'titulo', {'id':'padre>id','name':'padre>titulo'}, {'id':'acceso>id','name':'acceso>clave'}, 'url', 'estado']
	accesos = {'insert': 'ins_menu', 'update': 'upd_menu', 'delete': 'del_menu'}

class ControllerSecurity():
	accesos = {}
	@db_session
	def validate_access(self, usuario, clave):
		validate = False
		acceso = select(ra.acceso.clave for ur in UsuarioRole for ra in RoleAcceso if ur.usuario.id == str(usuario) and ur.role == ra.role )[:]
		if acceso is not None:
			if clave in acceso:
				validate = True
		return validate
	@db_session	
	def logout(self, **data):
		session = Session.get(usuario = data.get('_user_genesis', ''), token = data.get('_token_genesis', ''))
		try:
			session.delete()
			commit()
		except Exception, e:
			return 'No esta logueado correctamente'
		return 'Gracias por salirse correctamente'
class ControllerSession(ControllerGeneric):
	model = Session
	col_view = {'insert': ['tipo_item','titulo','barras','precio','precio_min','cantidad','hash', 'creado'], 'update': ['id','titulo','eestado'], 'delete':['id','titulo']}
	@db_session
	def validate_session(self, ip_ext, navegador_ext, token_ext):
		session = Session.get(token=token_ext)
		if session is not None:
			if session.ip == ip_ext and session.navegador == navegador_ext:
				res = session.usuario.id
			else:
				res = '-1'
		else:
			res = '-1'
		return res

	@db_session
	def validate_credentials(self, **data):
		ip_ext = data.get('ip_ext', '')
		navegador_ext = data.get('navegador_ext', '')
		usuario = Usuario.get(mail=data.get('usuario',''), password= data.get('password',''))
		if usuario is not None:
			session = Session.get(usuario = usuario.id, estado = 1)
			if session is None:
				res = self.create_session(usuario, ip_ext, navegador_ext)
			else:
				now = datetime.now()
				diferencia = now - session.creado
				if diferencia.days > 1 or ip_ext != session.ip or navegador_ext != session.navegador:
					session.estado = 0
					commit()
					res = self.create_session(usuario, ip_ext, navegador_ext)
				else:
					session.sesiones += 1
					commit()
					res = {'cod': '1', 'msj': '%s'%session.token.encode("utf-8")}
		else:
			res = {'cod': '0', 'msj': 'credenciales invalidas'}
		return json.dumps(res, ensure_ascii=False)

	def create_session(self, usuario, ip, navegador):
		token = self.create_token()
		data = {'values': {'token': token, 'usuario': usuario.id, 'ip': ip, 'navegador': navegador, 'creado': datetime.now(), 'sesiones': 1}}
		res = self.insert(**data)
		res = eval(res)
		if res['cod'] == '1':
			res['msj'] = token
		return res

	def create_token(self):
		now = datetime.now()
		caracteres = self.caracter_random(10)
		token = str(now.year)+caracteres[:2]+str(now.month)+caracteres[3]+str(now.day)+caracteres[3:6]+str(now.hour)+caracteres[7]+str(now.minute)+caracteres[2:4]+str(now.second)+caracteres[8:]
		valor_hash = hashlib.md5()
		valor_hash.update(token.encode('utf-8'))
		return valor_hash.hexdigest()

	def caracter_random(self, cantidad = 1):
		cadena = ''
		for i in range(cantidad):
			cadena += random.choice(string.letters)
		return cadena



	
