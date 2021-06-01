# USAGE
# python mask_rcnn.py --mask-rcnn mask-rcnn-coco --image images/example_01.jpg
# python mask_rcnn.py --mask-rcnn mask-rcnn-coco --image images/example_03.jpg --visualize 1

# import the necessary packages
import glob

import numpy as np
import argparse
import random
import time
import cv2
import os

from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import cv2
from scipy.ndimage.measurements import label

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to input image")
ap.add_argument("-m", "--mask-rcnn", required=True, help="base path to mask-rcnn directory")
ap.add_argument("-v", "--visualize", type=int, default=0, help="whether or not we are going to visualize each instance")
ap.add_argument("-c", "--confidence", type=float, default=0.5, help="minimum probability to filter weak detections")
ap.add_argument("-t", "--threshold", type=float, default=0.3, help="minimum threshold for pixel-wise mask segmentation")
ap.add_argument("-a", "--att", required=True, type=float, default=0, help="h of attacking color")
ap.add_argument("-d", "--def", required=True, type=float, default=0, help="h od defending color")
args = vars(ap.parse_args())

# load the COCO class labels our Mask R-CNN was trained on
labelsPath = os.path.sep.join([args["mask_rcnn"], "object_detection_classes_coco.txt"])
LABELS = open(labelsPath).read().strip().split("\n")

# load the set of colors that will be used when visualizing a given instance segmentation
# colorsPath = os.path.sep.join([args["mask_rcnn"], "colors.txt"])
# COLORS = open(colorsPath).read().strip().split("\n")
attColor = args["att"]
defColor = args["def"]

# derive the paths to the Mask R-CNN weights and model configuration
weightsPath = os.path.sep.join([args["mask_rcnn"], "frozen_inference_graph_coco.pb"])
configPath = os.path.sep.join([args["mask_rcnn"], "mask_rcnn_inception_v2_coco_2018_01_28.pbtxt"])

# load our Mask R-CNN trained on the COCO dataset (90 classes) from disk
print("[INFO] loading Mask R-CNN from disk...")
net = cv2.dnn.readNetFromTensorflow(weightsPath, configPath)


def find_connected_components(mask):
    structure = np.ones((3, 3), dtype=np.int)
    labeled, ncomponents = label(mask, structure)
    best = 0
    for i in range(1, ncomponents + 1):
        count = np.count_nonzero(labeled == i)
        if count > best:
            best = count
    return best


def get_hue_closest_color_to_input(colors, color_to_search=(222, 184, 135)):
    best = -1
    best_color = None
    for color in colors:
        mse = abs(np.sum(color) * np.sum(color) - np.sum(color_to_search) * np.sum(color_to_search))
        best = (best, mse)[best > mse or best < 0]
        if (best == mse):
            best_color = color
    (r, g, b) = best_color
    court_color_nd = np.uint8([[[r, g, b]]])
    hsv_court = cv2.cvtColor(court_color_nd, cv2.COLOR_RGB2HSV)
    hue_court = hsv_court[0][0][0]
    return hue_court


def get_dominant_colors_for_court(img, k=3):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    (h, w, _) = img.shape
    # plt.imshow(img)
    # plt.show()
    img = img.reshape((img.shape[0] * img.shape[1], img.shape[2]))
    clt = KMeans(n_clusters=k)  # "pick out" the K-means tool from our collection of algorithms
    clt.fit(img)  # apply the model to our data, the image
    # print(clt.labels_)
    label_indx = np.arange(0, len(np.unique(clt.labels_)) + 1)
    (hist, _) = np.histogram(clt.labels_, bins=label_indx)
    hist = hist.astype('float')
    hist /= hist.sum()
    hist_bar = np.zeros((50, 300, 3), dtype="uint8")
    startX = 0
    res = []
    for (percent, color) in zip(hist, clt.cluster_centers_):
        endX = startX + (percent * 300)  # to match grid
        cv2.rectangle(hist_bar, (int(startX), 0), (int(endX), 50),
                      color.astype("uint8").tolist(), -1)
        res.append(color)
        startX = endX
    # plt.imshow(hist_bar)
    # plt.show()
    return res


def mask_player(img, color, tol=10):
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    tub = (color - tol) / 2
    tlb = (color + tol) / 2
    if tub < 1:
        tub = 1
    if tlb > 179:
        tlb = 179
    upper_bound = np.array([tub, 0, 0], np.uint8)
    lower_bound = np.array([tlb, 255, 255], np.uint8)

    mask = cv2.inRange(hsv_img, upper_bound, lower_bound)

    # # Bitwise-AND mask and original image
    # res = cv2.bitwise_and(img, img, mask=mask)

    # Show original image
    # plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    # plt.title('Original Image')
    # plt.show()

    # Show masked image
    # plt.imshow(mask)
    # plt.title('Mask')
    # plt.show()

    return mask


# load our input image and grab its spatial dimensions
directory = args["image"]
images_path = glob.glob(directory + "\*.jpg")
court_color = None
for img_path in images_path:
    output_path = img_path[:-4]
    os.mkdir(output_path)
    image = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
    (H, W) = image.shape[:2]
    print("[INFO] image size: {}x{} pixels".format(W, H))
    if court_color is None:
        dominant_colors = get_dominant_colors_for_court(image, 3)
        court_color = get_hue_closest_color_to_input(dominant_colors)
        # attColor = get_hue_closest_color_to_input(dominant_colors, )
        print(court_color)

    # construct a blob from the input image and then perform a forward
    # pass of the Mask R-CNN, giving us (1) the bounding box coordinates
    # of the objects in the image along with (2) the pixel-wise segmentation
    # for each specific object
    blob = cv2.dnn.blobFromImage(image, swapRB=True, crop=False)
    net.setInput(blob)

    start = time.time()
    (boxes, masks) = net.forward(["detection_out_final", "detection_masks"])
    end = time.time()

    # show timing information and volume information on Mask R-CNN
    print("[INFO] Mask R-CNN took {:.6f} seconds".format(end - start))
    print("[INFO] boxes shape: {}".format(boxes.shape))
    print("[INFO] boxes size: {}".format(boxes.size))
    print("[INFO] masks shape: {}".format(masks.shape))

    # loop over the number of detected objects
    for i in range(0, boxes.shape[2]):

        # extract the class ID of the detection along with the confidence
        # (i.e., probability) associated with the prediction
        classID = int(boxes[0, 0, i, 1])
        confidence = boxes[0, 0, i, 2]

        # filter out weak predictions by ensuring the detected probability
        # is greater than the minimum probability
        if confidence > args["confidence"]:
            # clone our original image so we can draw on it
            # clone = image.copy()

            # scale the bounding box coordinates back relative to the
            # size of the image and then compute the width and the height
            # of the bounding box
            box = boxes[0, 0, i, 3:7] * np.array([W, H, W, H])
            (startX, startY, endX, endY) = box.astype("int")
            boxW = endX - startX
            boxH = endY - startY

            # extract the pixel-wise segmentation for the object, resize
            # the mask such that it's the same dimensions of the bounding
            # box, and then finally threshold to create a *binary* mask
            mask = masks[i, classID]
            mask = cv2.resize(mask, (boxW, boxH), interpolation=cv2.INTER_NEAREST)
            mask = (mask > args["threshold"])

            # extract the ROI of the image
            roi = image[startY:endY, startX:endX]

            # check to see if are going to visualize how to extract the masked region itself
            if args["visualize"] > 0:
                # convert the mask from a boolean to an integer mask with
                # to values: 0 or 255, then apply the mask
                visMask = (mask * 255).astype("uint8")
                instance = cv2.bitwise_and(roi, roi, mask=visMask)
                (h, w, _) = instance.shape
                if w * 3 / 2 > h:
                    continue

                # show the extracted ROI, the mask, along with the segmented instance
                # cv2.imshow("ROI", roi)
                # cv2.imshow("Mask", visMask)
                # cv2.imshow("Segmented", instance)

                # write the segmented image to disk
                cv2.imwrite(output_path + "\\segmented{}.png".format(i), instance)
                instance = instance[int(h / 4):int(2 * h / 3), ]
                att_mask = mask_player(instance, attColor)
                def_mask = mask_player(instance, defColor)
                court_mask = mask_player(instance, court_color, 5)

                att_mask -= cv2.bitwise_and(court_mask, att_mask)
                def_mask -= cv2.bitwise_and(court_mask, def_mask)
                att_comp = find_connected_components(att_mask)
                def_comp = find_connected_components(def_mask)

                fig = plt.figure(figsize=(5, 5))
                fig.add_subplot(1, 3, 1)
                plt.imshow(cv2.cvtColor(instance, cv2.COLOR_BGR2RGB))
                plt.title('OG')
                fig.add_subplot(1, 3, 2)
                plt.imshow(att_mask)
                plt.title('AMask')
                fig.add_subplot(1, 3, 3)
                plt.imshow(def_mask)
                plt.title('DMask')
                plt.show()

                (h, w, _) = instance.shape

                if attColor < 70:
                    if (att_comp < h * w * 5 / 100):
                        att_comp = 0
                print(def_comp, h * w * 5 / 100)
                if defColor < 70:
                    if (def_comp < h * w * 5 / 100):
                        def_comp = 0

                print(att_comp, def_comp)

                res = 2
                if 0 < def_comp > att_comp:
                    res = 1
                elif att_comp > 0:
                    res = 0

                f = open(output_path + "\\segmented{}.txt".format(i), "w")
                toWrite = str(startX + (endX - startX) / 2) + " " + str(endY) + "\n" + str(res)
                f.write(toWrite)
                f.close()

        # now, extract *only* the masked region of the ROI by passing in the boolean mask array as our slice condition
        # roi = roi[mask]
        #
        # # Red will be used to visualize this particular instance segmentation
        # # then create a transparent overlay by blending the randomly selected color with the ROI
        # blended = ((0.4 * RED_COLOR) + (0.6 * roi)).astype("uint8")
        #
        # # store the blended ROI in the original image
        # image[startY:endY, startX:endX][mask] = blended

        # draw the bounding box of the instance on the image
        # cv2.rectangle(image, (startX, startY), (endX, endY), (255,255,255), 2)

        # draw the predicted label and associated probability of the instance segmentation on the image
        # text = "{}: {:.4f}".format("Person", confidence)
        # cv2.putText(image, text, (startX, startY - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)

        # show the output image
        # cv2.imshow("Output", image)
        # cv2.waitKey(0)
#
# cv2.imshow('out', image)
# cv2.waitKey(0)
# cv2.imwrite("output/result.jpg", image)
