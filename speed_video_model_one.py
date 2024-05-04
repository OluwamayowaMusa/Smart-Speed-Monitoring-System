import cv2
import time
import numpy as np
from datetime import datetime
from helpers import prepare_interpreter, process_image, load_labels, add_text_to_image
from helpers import calculate_speed_fixed_distance_measure_time, connect_to_database
from helpers import generate_colors, add_label, get_tensor_output, add_id, populate_database
from tracker import Tracker

# Declare Parameters
VIDEO_PATH = "veh2.mp4"
LABEL_PATH = "labelmap.txt"
MODEL = "efficientdet_lite0.tflite"
NUM_THREADS = 4
THRESHOLD = 0.3
LABELS_TO_TRACK = ["car", "motorcycle", "bus", "truck"]
SPEED_LIMIT = 40 # km/hr
PICTURES_PATH = "/home/user/Python/track_history"

# Database Parameters
host = "localhost"
user = "root"
password = "raspberrypi"
database = "smart_speed"
table = "history"

# Text Properties
TEXT_LOCATION = (20, 120)
FONT_STYLE = cv2.FONT_HERSHEY_SIMPLEX
FONT_SIZE = 2
FONT_THICKNESS = 4
FONT_COLOR = [int(i) for i in generate_colors(1)[0]]

# Get interpreter info
interpreter_info = prepare_interpreter(MODEL, NUM_THREADS)
interpreter = interpreter_info["Interpreter"]

labels = load_labels(LABEL_PATH)

colors = generate_colors(len(labels))

# Load Video
video = cv2.VideoCapture(VIDEO_PATH)
count = 0

# Database Connection
database_connection = connect_to_database(host, user, password, database)
cursor = database_connection.cursor()

# Track objects
time_start = time.time()
fps = 0
tracker = Tracker()
while True:
	status, frame = video.read()
	
	# If the read operation fails
	if status is False:
		print("Read operation failed")
		exit(1)
		
#	count += 1 
#	if count % 3 != 0:
#		continue
		
	input_data, image = process_image(frame, interpreter_info["input_dim"])
	
	# Allocate Tensors
	interpreter.set_tensor(interpreter_info["tensors_index"]["input_tensor_index"], input_data)
	interpreter.invoke()
	
	# Get boxes, classes, scores
	boxes, classes, scores = get_tensor_output(interpreter_info)
	
	for box, class_, score in zip(boxes, classes[:5], scores[:5]):
		class_name = labels[int(class_)]
		if score < THRESHOLD or not (class_name in LABELS_TO_TRACK):
			continue
		
		color = [int(i) for i in colors[int(class_)]]
		speed = calculate_speed_fixed_distance_measure_time(image, box, class_name, score, color, tracker)
		if speed > SPEED_LIMIT:
			now = datetime.now().strftime("%d_%m_%y_%H_%M_%S")
			filename = f"{PICTURES_PATH}/picture_{now}.jpg"
			cv2.imwrite(filename, image)
			populate_database(cursor, table, speed, now)
			database_connection.commit()
			print("Saved")
		
		text = f"Gone Down: {len(tracker.gone_down)}"
		add_text_to_image(image, text, TEXT_LOCATION, FONT_STYLE,
						  FONT_SIZE, FONT_COLOR, FONT_THICKNESS)
		
		cv2.imshow("Input", image)
		#print(f"{score} {labels[int(class_)]}")
	
	if cv2.waitKey(1) == ord('q'):
		break
		
	# Calculate Frames Per Second	
	time_end = time.time()
	loop_time = time_end - time_start
	fps = 0.9*fps + 0.1*(1/loop_time)
	time_start = time.time()


video.release()
database_connection.close()
cv2.destroyAllWindows()