import cv2
import numpy as np
import tflite_runtime.interpreter as tflite
from helpers import load_labels, prepare_interpreter, process_image
from helpers import generate_colors, add_label, get_tensor_output


# Declare Constants
TEST_IMAGE = "image.jpg"
LABEL_PATH = "labelmap.txt"
MODEL = "efficientdet_lite0.tflite"
NUM_THREADS = 4
THRESHOLD = 0.3

# Get interpreter info
interpreter_info = prepare_interpreter(MODEL, NUM_THREADS)

# Process image
image = cv2.imread(TEST_IMAGE)
input_data, image = process_image(image, interpreter_info["input_dim"])

# Allocate tensors
interpreter = interpreter_info["Interpreter"]
interpreter.set_tensor(interpreter_info["tensors_index"]["input_tensor_index"],input_data)
interpreter.invoke()

# Get boxes, classes, scores
boxes, classes, scores = get_tensor_output(interpreter_info)

labels = load_labels(LABEL_PATH)
colors = generate_colors(len(labels))
for box, class_, score in zip(boxes, classes[:5], scores[:5]):
	if score < THRESHOLD:
		continue

	color = [int(i) for i in colors[int(class_)]]
	add_label(image, box, labels[int(class_)], score, color)
	cv2.imshow("Input", image)
	print(f"{score} {labels[int(class_)]}")

cv2.waitKey(0)
cv2.destroyAllWindows()
