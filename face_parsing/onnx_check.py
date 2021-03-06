import onnxruntime
from utils import *
import torch
from torchvision import transforms
import PIL
import cv2

def transformer(imsize):
    options = []
    
    
    options.append(transforms.ToTensor())
    options.append(transforms.Resize((imsize,imsize), interpolation=PIL.Image.NEAREST))    
    options.append(transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)))
    transform = transforms.Compose(options)
    
    return transform

def to_numpy(tensor):
    return tensor.detach().cpu().numpy() if tensor.requires_grad else tensor.cpu().numpy()

transform = transformer(512)

input_image = cv2.imread("Data_preprocessing/test_img/12.jpg")
h, w, c = input_image.shape
input_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2RGB)



ort_session = onnxruntime.InferenceSession("onnx/mask.onnx")
print(ort_session.get_inputs())
ort_input = {ort_session.get_inputs()[0].name: input_image}
print("b")
ort_out = ort_session.run(None, ort_input)[0]

# 사이즈 조정
# output = cv2.resize(ort_out[0], (w, h))
output = ort_out[0]
print(output.shape)

cv2.imshow("out",output)
cv2.waitKey(0)
cv2.destroyAllWindows()
