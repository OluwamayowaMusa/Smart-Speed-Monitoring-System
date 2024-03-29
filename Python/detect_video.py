import cv2
import numpy as np
from helpers import prepare_interpreter, process_image, load_labels
from helpers import generate_colors, add_label, get_tensor_output

# Declare Parameters
VIDEO_PATH = "veh2.mp4"
LABEL_PATH = "labelmap.txt"
MODEL = "efficientdet_lite0.tflite"
NUM_THREADS = 4
THRESHOLD = 0.3

# Get interpreter info
interpreter_info = prepare_interpreter(MODEL, NUM_THREADS)
interpreter = interpreter_info["Interpreter"]

labels = load_labels(LABEL_PATH)
colors = generate_colors(len(labels))

# Load Video
video = cv2.VideoCapture(VIDEO_PATH)
count = 0
while True:
	status, frame = video.read()
	
	# If the read operation fails
	if status is False:
		print("Read operation failed")
		exit(1)
		
	count += 1 
	if count % 3 != 0:
		continue
		
	input_data, image = process_image(frame, interpreter_info["input_dim"])
	
	# Allocate Tensors
	interpreter.set_tensor(interpreter_info["tensors_index"]["input_tensor_index"], input_data)
	interpreter.invoke()
	
	# Get boxes, classes, scores
	boxes, classes, scores = get_tensor_output(interpreter_info)
	
	for box, class_, score in zip(boxes, classes[:5], scores[:5]):
		if score < THRESHOLD:
			continue
		
		color = [int(i) for i in colors[int(class_)]]
		add_label(image, box, labels[int(class_)], score, color)
		cv2.imshow("Input", image)
		print(f"{score} {labels[int(class_)]}")
	
	if cv2.waitKey(1) == ord('q'):
		break


video.release()
cv2.destroyAllWindows()
print("All Good")
