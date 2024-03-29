import pymysql
import subprocess
import io
from base64 import encodebytes
from PIL import Image


def running_smart_speed_system(filename):
	""" Check if the smart speed system is running
	
	Args:
		filename: File to be checked
		
	Returns:
		True if running, otherwise False
	"""
	list_process = subprocess.Popen(["ps", "aux"],
						stdout=subprocess.PIPE, text=True)
	grep_process = subprocess.Popen(["grep", filename],
					stdin=list_process.stdout,
					stdout=subprocess.PIPE, text=True)
	
	output, error = grep_process.communicate()
	
	if error:
		return False
	else:
		return f"python {filename}" in output
		
def connect_to_database(host, user, password, database=None):
	""" Connect to mysql Database
	
	Args:
		host: Host where the database is hosted
		user: Username log in as
		password: User's Password
		database: Database to use, None to not use a specific one
		
	Return:
		Connection Object
	"""
	return pymysql.connect(host=host, user=user, password=password,
						   database=database)
						   
def get_database_configurations(app):
	""" Get the database configuration i.e host, user,
		password, database, table
		
	Args:
		app: An instance of the app
		
	Returns:
		A dictionary containing database info
	"""
	host = app.config.get("MY_SQL_HOST")
	user = app.config.get("MY_SQL_USER")
	password = app.config.get("MY_SQL_PASSWORD")
	database = app.config.get("MY_SQL_DATABASE")
	table = app.config.get("MY_SQL_TABLE")
	
	return {"host": host, "user": user, "passwd": password,
			"db": database, "table": table}
	
	
def get_response_image(filename):
	""" Convert the image to byte array
	
	Args:
		filename: Name of the image file to convert to a byte arraty
		
	Returns:
		Encoded Byte array
	"""
	pil_image = Image.open(filename, mode='r')
	bytes_arr = io.BytesIO()
	pil_image.save(bytes_arr, format="PNG")
	encoded_img = encodebytes(bytes_arr.getvalue()).decode("ascii")
	
	return encoded_img
