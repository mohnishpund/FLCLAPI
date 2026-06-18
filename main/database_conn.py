from app import app
import oracledb


app.config['ORACLE_HOST'] = 'localhost'
app.config['ORACLE_PORT'] = '1521'
app.config['ORACLE_USER'] = 'table_jan24'
app.config['ORACLE_PASSWORD'] = '123'
app.config['ORACLE_SERVICE'] = 'xe'

# create a function 

def get_db_connection():
	try:
		# make dsn
		dsn = oracledb.makedsn(app.config['ORACLE_HOST'],
			app.config['ORACLE_PORT'], service_name = app.config['ORACLE_SERVICE']
			)
		connection = oracledb.connect(user=app.config['ORACLE_USER'], password=app.config['ORACLE_PASSWORD'], dsn=dsn)


		return connection

	except oracledb.Error as error:
		# If anything goes wrong, this block catches it safely
		print(f"Failed to connect to the database: {error}")
		# Return None so your routes know the connection failed
		return None