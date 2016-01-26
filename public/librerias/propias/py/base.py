import mysql.connector
from mysql.connector import errorcode
'''importo el driver de mysql y tambien la libreria para manejar los errores'''



class DataBase:
	'''Clase que servira para administrar las conecciones'''
	CONFIG = {
	  'user': 'root',
	  'password': 'S01u)i0n73)n0dis@',
	  'host': '127.0.0.1',
	  'database': 'genesispy',
	  'raise_on_warnings': True,
	  'charset': 'utf8'
	}
	txt_insert = 'INSERT INTO {0} ({1}) VALUES({2})'
	txt_update = 'UPDATE {0} SET {1} WHERE {2}'
	txt_delete = 'DELETE FROM  {0} WHERE {1}'
	txt_select = 'SELECT {0} FROM {1} WHERE {2}'
	error = ''
	def __init__(self,table):
		'''Inicializa la aplicacion solicitando la tabla para la que servira la coneccion y los encabezados 
		para generar el string de insert'''	
		self.table = table
		
		
	def connect(self):
		'''Se realiza la coneccion, si existe error lo muestra en caso contrario no indica nada'''
		try:
			self.connection = mysql.connector.connect(**self.CONFIG)
		except mysql.connector.Error as err:
			if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
				self.error +="Something is wrong with your user name or password"
			elif err.errno == errorcode.ER_BAD_DB_ERROR:
				self.error += "Database does not exist"
			else:
				self.error += err
		else:
			pass
	def generate_string_insert(self, attributes):
		'''Crea los encabezados y la estructura que pide el insert para ingresar los valores recibe los attributes 
		que en si son los encabezados de la tabla de la que se habla'''
		encabezado, valores = '', ''
		for punter in attributes:
			encabezado += punter+', '
			if(attributes[punter]['val']!=''):
				valores += "'"+str(attributes[punter]['val'])+"', "
			else:
				valores += 'NULL, '
		encabezado, valores = encabezado[:-2], valores[:-2]
		txt_insert = self.txt_insert.format(self.table,encabezado,valores)
		return txt_insert
	def generate_string_update(self, attributes):
		'''crea el string necesario para realizar la actualizacion a la base de datos, toma como referencia el string de update'''
		valores = ''
		restriction = ''
		for punter in attributes:
			if punter != 'id':
				if attributes[punter]['val'] != '':
					valores += punter+" = '"+str(attributes[punter]['val'])+"', "
		restriction += "id = '"+attributes['id']+"'"
		valores = valores[:-2]
		txt_update = self.txt_update.format(self.table, valores, restriction)
		return txt_update
	def generate_string_delete(self, attributes):
		'''crea el string necesario para realizar la eliminacion a la base de datos, toma como referencia el string de delete'''
		restriction = ''
		restriction += "id = '"+str(attributes['id'])+"'"
		
		txt_delete = self.txt_delete.format(self.table, valores)
		return txt_delete
	def generate_string_select(self, attributes, seleccion= None):
		encabezados = ''
		restriction = ''
		objetos = []
		tablas = self.table+', '
		if type(seleccion) is not list and seleccion is not None:
			seleccion = eval(seleccion)

		for punter in seleccion:
			if '.' in punter:
				punter = punter.split('.')
				encabezados += punter[0]+'.'+punter[1]+', '
				objetos.append(punter[0])
				tablas += punter[0]+', '
			else:
				encabezados += self.table+'.'+punter+', '
		'''else:
			if '.' in seleccion:
				punter = punter.split('.')
				encabezados += punter[0]+'.'+punter[1]+', '
				objetos.append(punter[0])
				tablas += punter[0]+', '
			else:

				encabezados += self.table+'.'+eval(seleccion)+', '
		'''
		for punter in attributes:
			if attributes[punter]['val'] != "":
				restriction += self.table+'.'+punter+" = '"+str(attributes[punter]['val'])+"' AND "
			if encabezados == '':
				encabezados += self.table+'.'+punter+', '
		for tabla_foranea in objetos:
			restriction += self.table+'.'+tabla_foranea+" = "+tabla_foranea+".id AND "

		restriction = restriction[:-4]
		encabezados = encabezados[:-2]
		tablas = tablas[:-2]
		txt_select = self.txt_select.format(encabezados,tablas,restriction)
		return txt_select
	def insert(self,data):
		'''Realiza la accion de insertar en la base de datos crea un cursor para saber el ultimo id y errores
		Si existe un error lo coloca en los errores de este objeto y retorna None, para que sea consultado por 
		el objeto invocador. Si existe lastid lo devuelve de lo contrario devuelve Ok'''
		self.start_transaction()
		txt_insert = self.generate_string_insert(data)
		self.cursor = self.connection.cursor()
		try:
			self.cursor.execute(txt_insert)
		except mysql.connector.Error as err:
			self.error = str(err)+txt_insert
			return None
		else:
			if(self.cursor.lastrowid):
				answer = self.cursor.lastrowid
			else:
				answer = "Ok"
			self.connection.commit()
			self.end_transaction()
			return answer
	def update(self,data):
		'''Realiza la accion de insertar en la base de datos crea un cursor para saber el ultimo id y errores
		Si existe un error lo coloca en los errores de este objeto y retorna None, para que sea consultado por 
		el objeto invocador. Si existe lastid lo devuelve de lo contrario devuelve Ok'''
		self.start_transaction()
		txt_update = self.generate_string_update(data)
		self.cursor = self.connection.cursor()
		try:
			self.cursor.execute(txt_update)
		except mysql.connector.Error as err:
			self.error = str(err)+txt_update
			return None
		else:
			answer = "Ok"
			self.connection.commit()
			self.end_transaction()
			return answer
	def delete(self,data):
		'''Realiza la accion de insertar en la base de datos crea un cursor para saber el ultimo id y errores
		Si existe un error lo coloca en los errores de este objeto y retorna None, para que sea consultado por 
		el objeto invocador. Si existe lastid lo devuelve de lo contrario devuelve Ok'''
		self.start_transaction()
		txt_update = self.generate_string_delete(data)
		self.cursor = self.connection.cursor()
		try:
			self.cursor.execute(txt_delete)
		except mysql.connector.Error as err:
			self.error = str(err)+txt_delete
			return None
		else:
			answer = "Ok"
			self.connection.commit()
			self.end_transaction()
			return answer

	def find(self,data, seleccion = None):
		'''Realiza la accion de insertar en la base de datos crea un cursor para saber el ultimo id y errores
		Si existe un error lo coloca en los errores de este objeto y retorna None, para que sea consultado por 
		el objeto invocador. Si existe lastid lo devuelve de lo contrario devuelve Ok'''
		self.start_transaction()
		if seleccion != None:
			txt_select = self.generate_string_select(data, seleccion)
		else:
			txt_select = self.generate_string_select(data)
		
		self.cursor = self.connection.cursor()
		try:
			self.cursor.execute(txt_select)
		except mysql.connector.Error as err:
			self.error = str(err)+txt_select
			return None
		else:
			answer = self.cursor
			return answer


	def end_transaction(self):
		'''Realiza la desconeccion de este objeto, elimina la connection y cursor existente actual'''	
		self.cursor.close()
		self.connection.close()
	def start_transaction(self):
		self.connect()
	def confirm_transaction(self):
		connection.commit()
		if connection.error != "":
			return "Erro: "+connection.error
	def rollbak_transaction(self):
		connection.rollback()
	def restrictions(dic_restriction):
		output = "WHERE "
		for restriction in dic_restriction:
			output += " "+restriction[0]+" "
			output += restriction[1]+" "
			output += restriction[2]+" "
			if restriction[3] == ".":
				output += restriction[3]
			elif restriction[3] == "":
				output += "NULL";
			else:
				output += "'"+restriction[3]+"'";
		return output
	def select(selection, restriction, tables):
		connet()
		sql = "SELECT "
		for column in selection:
			sql += column+", "
		sql = sql[0:-2]+" FROM"
		for table in tables:
			sql += table+", "
		sql = sql[0:-2]
		if len(restriction) > 0:
			restrictions(restriction)
		result = cursor.execute
		if connection.error:
			print(connection.error)
		else:
			for line in result:
				print (line['id'])