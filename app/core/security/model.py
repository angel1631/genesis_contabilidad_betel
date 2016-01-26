from decimal import Decimal
from datetime import datetime
from pony.orm import *
from app.core.cdb import cdb

#from app.core.contabilidad.model import egreso

db = cdb()

class Usuario(db.Entity):
	from app.core.contabilidad.model import Ingreso
	nombre = Required(str,255)
	mail = Required(str, 255)
	password = Required(str, 255)
	creado = Required(datetime, 0, default = datetime.now())
	estado = Required(int, size = 8, default = 1)
	##Relaciones
	_sessions = Set("Session")
	_roles = Set("UsuarioRole")
	#_ingresos = Set("Ingreso")
	#_egresos = Set("Egreso")

class Role(db.Entity):
	titulo = Required(str, 255)
	estado = Required(int, size = 8, default = 1)
	##Relaciones
	_accesos = Set("RoleAcceso")
	_usuarios = Set("UsuarioRole")

class Acceso(db.Entity):
	clave = Required(str, 255)
	obser = Optional(str, 1024)
	estado = Required(int, size = 8, default = 1)
	##Relaciones
	_roles = Set("RoleAcceso")
	_menus = Set("Menu")

class RoleAcceso(db.Entity):
	_table_ = 'role_acceso'
	role = Required(Role)
	acceso = Required(Acceso)
	estado = Required(int, size = 8, default = 1)

class UsuarioRole(db.Entity):
	_table_ = 'usuario_role'
	usuario = Required(Usuario)
	role = Required(Role)
	estado = Required(int, size = 8, default = 1)

class Session(db.Entity):
	'''manejara todas las sesiones de la aplicacion'''
	token = Required(str, 255)
	usuario = Required(Usuario)
	ip = Required(str, 255)
	navegador = Required(str, 255)
	creado = Required(datetime, 0, default = datetime.now())
	sesiones = Required(int, size = 8)
	estado = Required(int, size = 8, default = 1)

class Menu(db.Entity):
	titulo = Required(str, 255)
	padre = Optional("Menu", reverse="_menus")
	acceso = Optional(Acceso)
	posicion = Required(int, size = 8, default = 0)
	url = Required(str, 500)
	estado = Required(int, size = 8, default = 1)
	##Relaciones
	_menus = Set("Menu", reverse = "padre")

db.generate_mapping(create_tables=True)