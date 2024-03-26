from flask import Flask, make_response, jsonify, request
from utils import running_smart_speed_system, get_database_configurations, connect_to_database, get_response_image


app = Flask(__name__)
app.config.from_pyfile("settings.py")

database_info = get_database_configurations(app)
database_connection = connect_to_database(database_info["host"],
										  database_info["user"],
										  database_info["passwd"],
										  database_info["db"])
database_cursor = database_connection.cursor()


@app.route("/")
def welcome_to_system():
	"""	Welcome to smart speed system
	
	"""
	
	return "Hello from Smart Speed System"

@app.route("/state")
def state_of_system():
	""" Check if Smart Speed System is running
	
	Returns:
		200 - Up and Running
		503 - Not Ruuning
	"""
	smart_speed_system_file = app.config.get("SMART_SPEED_SYSTEM")
	
	if running_smart_speed_system(smart_speed_system_file):
		return make_response(("Success, Up and Running", 200))
	else:
		return make_response(("Offline, Not running", 503))

	
@app.route("/recent")
def recent():
	""" Returns the info of the latest trespasser or the number passed
	
	Returns:
		trespasser info i.e speed, time and picture
	"""
	database_connection.commit()
	number = request.args.get("number")
	if number is None:
		number = 1
		
	statement = f"SELECT speed, trespassed_at FROM {database_info['table']} ORDER BY id DESC LIMIT {number}"
	response = {}
	if database_cursor.execute(statement):
		results = database_cursor.fetchall()
		for index, (speed, date) in enumerate(results):
			filename = f"{app.config.get('IMAGES_PATH')}{date}.jpg"
			encoded_image = get_response_image(filename)
			response[index + 1] = {"speed": speed, "date": date, "ImageBytes": encoded_image}
		return jsonify(response)
		
	database_connection.commit()	
	return make_response(("No image has been saved"), 404)
	
