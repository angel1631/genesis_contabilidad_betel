from pony.orm import *

def cdb():
	db = Database()
	db.bind('mysql', host = 'localhost', user='root', passwd='S01u)i0n73)n0dis@', db='genesis_contabilidad_betel')
	return db