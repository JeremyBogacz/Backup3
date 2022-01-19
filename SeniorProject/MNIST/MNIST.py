# Created by Jeremy Bogacz on 11/22/2021

# This program invokes a CNN that classifys hand written
# digits from 0-9. These digits are 28x28 pixels and the 
# program will produce the CNN's prediction and confidence.

# Import packages
import time
start1 = time.time()

import sys

import tflite_runtime.interpreter as tflite
import numpy as np

from PIL import Image
from skimage import transform

# Get start time
start2 = time.time()

# Check for correct amount of arguments
if len(sys.argv) < 2:
    print()
    print("Innvocation: python3 tfModel_1.py filepath")
    print("Example: python3 tfModel_1.py CNN_Numbers/0.png")
    print()
    exit()

# Take in filepath and print it out
filepath = sys.argv[1];
print()
print("File Path: ", filepath)

# Function for processing the image for the network
def load(filename):
    np_image = Image.open(filename)
    np_image = np.array(np_image).astype('float32')/255
    np_image = transform.resize(np_image, (28, 28, 1))
    np_image = np.expand_dims(np_image, axis=0)
    return np_image

# Load in the image from the file
image = load(filepath)

# Load the CNN model
interpreter = tflite.Interpreter(model_path="MNIST.tflite")
interpreter.allocate_tensors()

# Get input and output details from the loaded model
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Set the tensor or input to the model
interpreter.set_tensor(input_details[0]['index'], image)

# Execute the model
interpreter.invoke()

# Get the models output
output_data = interpreter.get_tensor(output_details[0]['index'])

# Get end time
end = time.time()

# Print the output to the screen
print("Model Prediction: ", np.argmax(output_data))
print("Model Confidence: {:02.2f}%".format(np.max(output_data)*100))
print()
print("Execution Time (Before Imports) : {:.2f}".format(end-start1))
print("Execution Time (After Imports) : {:.2f}".format(end-start2))
print()
