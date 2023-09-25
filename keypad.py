import torch
import torch.nn as nn
from torchvision import datasets
from torchvision import transforms as T
import torchvision.transforms.functional as F
from torch.utils.data import ConcatDataset,DataLoader
from torchvision.models import densenet201
import os
import numpy as np
import numpy.matlib
from PIL import Image
import cv2
import matplotlib.pyplot as plt

model = None
SIZE = 30
device = 'cuda' if torch.cuda.is_available() else 'cpu'

class ScaledResizePad(object):
    def __init__(self, output_size=SIZE, scale_size=18, fill=0,padding_mode='constant'):
        self.fsize = output_size
        self.dsize = scale_size

        self.fill = 0
        self.padding_mode = padding_mode
#         assert isinstance(min_size, (numbers.Number, str, tuple))
#         assert isinstance(max_size, (numbers.Number, str, tuple))

    def __call__(self, img):
        """
        Args:
            img (PIL Image): Image to be padded.

        Returns:
            PIL Image: Padded image.
        """
        if type(img) == torch.Tensor:
            w,h = img.shape[1:]
        elif type(img) == np.ndarray:
            w,h = img.shape[:2]
        else:
            w,h = img.size
        scale_factor = self.dsize/max(w,h)
        size = int(h*scale_factor),int(w*scale_factor)

        scaled_img = F.resize(img,size)
#         scaled_img = F.resize(img,(20,20))

        return F.pad(scaled_img, get_padding(scaled_img,self.fsize), self.fill, self.padding_mode)

    def __repr__(self):
        return self.__class__.__name__ + '(padding={0}, fill={1}, padding_mode={2})'.\
            format(self.fill, self.padding_mode)

def get_padding(image,output_size = SIZE):
    if type(image) == torch.Tensor or type(image) == np.ndarray:
        w, h = image.shape[1:]
    else:
        w, h = image.size
    h_padding = (output_size - w) / 2
    v_padding = (output_size - h) / 2
    l_pad = h_padding if h_padding % 1 == 0 else h_padding+0.5
    t_pad = v_padding if v_padding % 1 == 0 else v_padding+0.5
    r_pad = h_padding if h_padding % 1 == 0 else h_padding-0.5
    b_pad = v_padding if v_padding % 1 == 0 else v_padding-0.5
    padding = (int(l_pad), int(t_pad), int(r_pad), int(b_pad))
    return padding

def condition(w, h):
    return (w>=5 and w <= 40 and h>=15 and h <= 70 and h/w<5 and w/h<5)

def sort_contours(cnts):
    boundingBoxes=[]
    newContours = []
    for contour in cnts:
        box = cv2.boundingRect(contour)
        x,y,w,h = box
        if condition(w,h):
            boundingBoxes.append(box)
            newContours.append(contour)
    (newContours, boundingboxes) = zip(*sorted(zip(newContours, boundingBoxes),key=lambda b:b[1][1]))
    return newContours,boundingboxes

def get_orientation(bboxes):
    npbox = np.asarray(bboxes)
    xmin,ymin=np.min(npbox[:,:2],axis=0)
    xmax,ymax=np.max(npbox[:,:2]+npbox[:,2:],axis=0)
    return (xmin,ymin), (xmax,ymax)

def predict(image):
    img=cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    transform=T.Compose([T.ToPILImage(),ScaledResizePad(padding_mode='edge',fill=0),T.ToTensor()])
    img=1-transform(img)
    img=img.repeat(1,3,1,1).to(device)
    output=model(img)
    score,predicted=torch.max(output,1)
    return score.item(),predicted.item(), output

def get_grid_location(x,y,tl,br):
    idx_x = int((x-tl[0])/(br[0]-tl[0])*3)
    idx_y = int((y-tl[1])/(br[1]-tl[1])*4)
    number = idx_y*3+idx_x+1
    if number == 11:
        number = 0
    return number


def get_keypad(img_path,conv_str=''):
    global model
    if model is None:
        init()
    full_img = cv2.imread(img_path)
    img = full_img[350:700,10:,:] # 2&3
    result = np.zeros_like(img)

    gray=cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    median = numpy.median(gray)
    edged = cv2.Canny(img, int(0.6 * median), int(1 * median))
    # edged=cv2.Canny(gray,100,200)
    contours,heirarchy = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    contours,boundingboxes=sort_contours(contours)

    print("contours & bboxes generated")

    digits=[]
    scores = []
    original_keys = []
    removal = []
    for i,box in enumerate(boundingboxes):
        x,y,w,h=box
        if condition(w,h):
    #         print(h,w,w/h,h/w)
            number=img[max(y-3,0):y+h+3,max(x-3,0):x+w+3]
            score, digit, raw = predict(number)

            if score < 1:
                removal.append(i)
                continue
            if digit == 0:
                print(digit, raw,h/w)
            if digit == 7 and h/w > 2:
                if raw[0][1].item()>1:
                    digit = 1
                    score = raw[0][1].item()
            if digit == 0 and h/w > 1.2:
                if raw[0][6].item()>2:
                    digit = 6
                    score = raw[0][1].item()

            if str(digit) in conv_str:
                predict_img = cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2) #Plotting bounding box
            # label
            # predict_img = cv2.putText(predict_img, str(digit), (x, y-3), cv2.FONT_HERSHEY_SIMPLEX, 1,(255, 0, 0), 1) #Plotting texts on top of box

            digits.append(digit)
            scores.append(score)

    print("prediction done")
    boundingboxes = [boundingboxes[i] for i in range(len(boundingboxes)) if i not in removal]
    TopLeft,BotRight=get_orientation(boundingboxes)
    for i,box in enumerate(boundingboxes):
        x,y,w,h=box
        original_key = get_grid_location(x,y,TopLeft,BotRight)
        original_keys.append(original_key)
        if str(digits[i]) in conv_str:
            predict_img = cv2.putText(predict_img, str(original_key), (x-7, y-2), cv2.FONT_HERSHEY_SIMPLEX, 0.8,(100, 255, 0), 1) #Plotting texts on top of box

    full_img[350:700,10:,:] = predict_img

    return dict(zip(digits,original_keys)), full_img

def init():
    global model
    print("loading model")
    model=densenet201(pretrained=False)
    classifier_in=model.classifier.in_features
    model.classifier=nn.Linear(classifier_in,10)
    weights=torch.load('MNIST.pth',map_location=device)
    model.load_state_dict(weights)
    model.eval()
    print("Model loaded")


if __name__ == "__main__":
    init()
    # op = cv2.imread('data/machine2_randomised.png')
    # cv2.imshow("contour.png",op)
    # d, img = get_keypad(op)
    # print(d)
    # cv2.imwrite("contour.png",img)
    # cv2.imshow("analysis",img)
