import matplotlib.pyplot as plt
import onnx 
import onnxruntime
import numpy as np

# image = plt.imread("recovery/496338_region_1_0.0.png")
image = plt.imread("recovery/11817_l1_on_entire_image.png")
img = image[:,:,0]
a = plt.imread("mnist/img_2.jpg")
a = a/255.0
a = a.astype('float32')

model = "model_sigm_nonrobust.onnx"
session = onnxruntime.InferenceSession(model, None)
input_name = session.get_inputs()[0].name
output_name = session.get_outputs()[0].name
result = session.run([output_name], {input_name: np.reshape(img, (1, 28, 28))})

print(np.argmax(np.array(result).squeeze()))