from decimal import Decimal
from datetime import datetime, date
from pony.orm import *
from app.core.cdb import cdb

db = cdb()
			
class TipoActividad(db.Entity):
	_table_ = "tipo_actividad"
	titulo = Required(str, 255)
	estatus = Required(int, size = 8, default = 1)
	
	_ingresos = Set("Ingreso")
	_egresos = Set("Egreso")

class Cuenta(db.Entity):
	titulo = Required(str, 255)
	monto = Required(Decimal, 10, 2)
	estatus = Required(int, size = 8, default = 1)

	_ingresos = Set("Ingreso")
	_egresos = Set("Egreso")

class Agrupador(db.Entity):
	titulo = Required(str, 255)
	estatus = Required(int, size = 8, default = 1)
	
	_ingresos = Set("Ingreso")
	_egresos = Set("Egreso")

class Ingreso(db.Entity):	
	tipo_actividad = Required(TipoActividad)
	fecha_referencia = Optional(date, default=datetime.now())
	identificador_documento = Optional(str, 200, default = "")
	observacion = Required(str, 1000)
	monto = Required(Decimal, 10, 2)
	agrupador = Optional("Agrupador")
	cuenta = Required(Cuenta)
	creado = Required(datetime, 0, default = datetime.now())
	usuario = Required(int)
	estatus = Required(int, size = 8, default = 1)
	#
	_traslados = Set('Traslado')

class Egreso(db.Entity):
	tipo_actividad = Required(TipoActividad)
	fecha_referencia = Optional(date, default = datetime.now())
	identificador_documento = Optional(str, 200)
	observacion = Required(str, 1000)
	monto = Required(Decimal, 10, 2)
	agrupador = Optional("Agrupador")
	cuenta = Required(Cuenta)
	creado = Required(datetime, 0, default = datetime.now())
	usuario = Required(int)
	estatus = Required(int, size = 8, default = 1)
	#
	_traslados = Set('Traslado')

class Traslado(db.Entity):
	ingreso = Required(Ingreso)
	egreso = Required(Egreso)
	monto = Required(Decimal, 10,2)
	creado = Required(datetime, 0, default = datetime.now())
	usuario = Required(int)
	observacion = Required(str, 1000)
	estatus = Required(int, size = 8, default = 1)

db.generate_mapping(create_tables=True)
