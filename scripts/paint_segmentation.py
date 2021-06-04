import glob
from collections import defaultdict

from detectron2 import model_zoo
from detectron2.config import get_cfg
from detectron2.engine import DefaultPredictor
import sys

import numpy as np
import cv2
import matplotlib.pyplot as plt

def get_p1(mask, y1):
    h, w, _ = im.shape
    y = int(y1)
    for y in range(y-10, w):
        for i in range(h):
            if (mask[i][y]):
                return (i,y)

def get_p1_left(mask, y1):
    h, w, _ = im.shape
    y = int(y1)
    for y in range(y-10, w):
        for i in range(h-1, 0, -1):
            if (mask[i][y]):
                return (i,y)

def get_p2(mask, x1):
    h, w, _ = im.shape
    x = int(x1)
    for i in range(x-10, h):
        for j in range(w-1, 0, -1):
            if (mask[i][j]):
                return (i,j)

def get_p2_left(mask, x1):
    h, w, _ = im.shape
    x = int(x1)
    for i in range(x-10, h):
        for j in range(w):
            if (mask[i][j]):
                return (i,j)

def get_p3(mask, y2):
    h, w, _ = im.shape
    y = int(y2)
    for y in range(w-1, 0, -1):
        for i in range(h-1, 0, -1):
            if (mask[i][y]):
                return (i,y)

def get_p3_left(mask, y2):
    h, w, _ = im.shape
    y = int(y2)
    for y in range(w-1, y-10, -1):
        for i in range(h):
            if (mask[i][y]):
                return (i,y)

def get_p4(mask, x1):
    h, w, _ = im.shape
    x = int(x1)
    for i in range(x+10, 0, -1):
        for j in range(0, w):
            if (mask[i][j]):
                return (i,j)

def get_p4_left(mask, x1):
    h, w, _ = im.shape
    x = int(x1)
    for i in range(x+10, 0, -1):
        for j in range(w-1, 0, -1):
            if (mask[i][j]):
                return (i,j)

def get_paint_right(mask, x1, y1, x2, y2):
    p1 = get_p1(mask, y1)
    p2 = get_p2(mask,x1)
    p3 = get_p3(mask,y2)
    p4 = get_p4(mask,x2)
    return p1, p2, p3, p4

def get_paint_left(mask, x1, y1, x2, y2):
    p1 = get_p1_left(mask, y1)
    p2 = get_p2_left(mask,x1)
    p3 = get_p3_left(mask,y2)
    p4 = get_p4_left(mask,x2)
    return p2, p3, p4, p1

cfg = get_cfg()
cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5 # Set threshold for this model
cfg.MODEL.WEIGHTS = r'D:\Repos\licenta\script_files\code\model\model_final.pth' # Set path model .pth
cfg.MODEL.ROI_HEADS.NUM_CLASSES = 1
cfg.MODEL.DEVICE = 'cpu'
predictor = DefaultPredictor(cfg)

frame_path = str(sys.argv[1])
side = str(sys.argv[2])
images_path = glob.glob(frame_path + "\*.jpg")
for im_path in images_path:
    im = cv2.imread(im_path)
    outputs = predictor(im)
    y1, x1, y2, x2 = outputs['instances'].pred_boxes.tensor[0]
    mask = outputs['instances'].pred_masks[0]

    if side == 'right':
        left_up, right_up, right_down, left_down = get_paint_right(mask, x1, y1, x2, y2)
    else:
        left_up, right_up, right_down, left_down = get_paint_left(mask, x1, y1, x2, y2)

    f = open(im_path[:-4] + "_paint.txt", "w")
    toWrite = str(left_up) + " " + str(right_up) + " " + str(right_down) + " " + str(left_down)
    f.write(toWrite)
    f.close()

    # plt.imshow(mask)
    # plt.show()
    # cv2.circle(im, (int(left_up[1]), int(left_up[0])), radius=0, color=(0, 255, 0), thickness=20)
    # cv2.circle(im, (int(right_up[1]), int(right_up[0])), radius=0, color=(0, 255, 0), thickness=20)
    # cv2.circle(im, (int(right_down[1]), int(right_down[0])), radius=0, color=(0, 255, 0), thickness=20)
    # cv2.circle(im, (int(left_down[1]), int(left_down[0])), radius=0, color=(0, 255, 0), thickness=20)
    # plt.imshow(cv2.cvtColor(im, cv2.COLOR_BGR2RGB))
    # plt.show()