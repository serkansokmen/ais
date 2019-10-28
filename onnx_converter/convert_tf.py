import onnx
import onnxmltools
import onnxruntime
import keras2onnx
import numpy as np
import tensorflow as tf

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.inception_v3 import preprocess_input

model_name = 'pneumonia_v0.0.1.hd5'
model_path = f'onnx_converter/models/{model_name}'

onnx_model_name = 'pneumonia_v0.0.1.onnx'
onnx_model_path = f'onnx_converter/models/{onnx_model_name}'

# image preprocessing
img_path = 'onnx_converter/val/NORMAL2-IM-1427-0001.jpeg'
# person1946_bacteria_4874.jpeg
img_size = 150
img = image.load_img(img_path, target_size=(img_size, img_size))
x = image.img_to_array(img)
x = np.expand_dims(x, axis=0)
x = preprocess_input(x)


# load keras model
model = load_model(model_path)

# convert to onnx model
onnx_model = keras2onnx.convert_keras(model, model.name)
onnx.save_model(onnx_model, onnx_model_path)

# runtime prediction
# content = onnx_model.SerializeToString()
# sess = onnxruntime.InferenceSession(content)
# x = x if isinstance(x, list) else [x]
# feed = dict([(input.name, x[n]) for n, input in enumerate(sess.get_inputs())])
# pred_onnx = sess.run(None, feed)
