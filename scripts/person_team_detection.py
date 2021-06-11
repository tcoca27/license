import glob

import numpy as np
import time
import os

from sklearn.cluster import KMeans
from constants import *
import cv2
from scipy.ndimage.measurements import label

# TODO: better define these
color_bounds = {'red': [[128, 0, 0], [255, 80, 80]], 'blue': [[0, 0, 128], [80, 120, 255]],
                'dark_blue': [[0, 0, 55], [60, 90, 128]], 'purple': [[0, 0, 55], [75, 100, 128]],
                'white': [[150, 150, 150], [255, 255, 255]], 'green': [[0, 128, 0], [160, 255, 160]],
                'black': [[1, 1, 1], [64, 64, 64]], 'yellow': [[120, 120, 0], [255, 255, 180]],
                'gray': [[64, 64, 64], [150, 150, 150]]
                }

labelsPath = labels_path_mask
LABELS = open(labelsPath).read().strip().split("\n")

weightsPath = weights_path_mask
configPath = config_path_mask

# print("[INFO] loading Mask R-CNN from disk...")
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


def mask_player(img, color):
    if color == 'yellow':
        return mask_court(img, 60)
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    lower_bound = np.array(color_bounds[color][0], np.uint8)
    upper_bound = np.array(color_bounds[color][1], np.uint8)

    mask = cv2.inRange(rgb_img, lower_bound, upper_bound)

    return mask


def mask_court(img, color, tol=10):
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

    return mask


def person_detection_team_classification(name, attColor, defColor, resFlag=False):
    images_path = glob.glob(processing_folder + '\\' + name + "\*.jpg")
    if resFlag:
        res_pth = results_folder + '\\' + name + '\\teams'
        try:
            os.mkdir(res_pth)
        except:
            pass
        images_path = glob.glob(results_folder + '\\' + name + '\\frames' + "\*.jpg")
    court_color = None
    for img_path in images_path:
        output_path = img_path[:-4]
        if resFlag:
            output_path = results_folder + '\\' + name + '\\teams\\' + img_path.split('\\')[-1][:-4]
        try:
            os.mkdir(output_path)
        except:
            pass
        image = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
        (H, W) = image.shape[:2]
        # print("[INFO] image size: {}x{} pixels".format(W, H))
        if court_color is None:
            dominant_colors = get_dominant_colors_for_court(image, 3)
            court_color = get_hue_closest_color_to_input(dominant_colors)
            # print(court_color)

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
        # print("[INFO] Mask R-CNN took {:.6f} seconds".format(end - start))
        # print("[INFO] boxes shape: {}".format(boxes.shape))
        # print("[INFO] boxes size: {}".format(boxes.size))
        # print("[INFO] masks shape: {}".format(masks.shape))

        # loop over the number of detected objects
        for i in range(0, boxes.shape[2]):

            # extract the class ID of the detection along with the confidence
            # (i.e., probability) associated with the prediction
            classID = int(boxes[0, 0, i, 1])
            confidence = boxes[0, 0, i, 2]

            # filter out weak predictions by ensuring the detected probability
            # is greater than the minimum probability
            if confidence > 0.2:
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
                mask = (mask > 0.3)

                # extract the ROI of the image
                roi = image[startY:endY, startX:endX]

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
                court_mask = mask_court(instance, court_color, 10)

                att_mask -= cv2.bitwise_and(court_mask, att_mask)
                def_mask -= cv2.bitwise_and(court_mask, def_mask)
                att_comp = cv2.countNonZero(att_mask)
                def_comp = cv2.countNonZero(def_mask)

                # if res:
                #     try:
                #         os.mkdir(results_folder + '\\' + name)
                #     except:
                #         print('Directory already exists')
                #
                #     try:
                #         os.mkdir(results_folder + '\\' + name + '\\person_team')
                #     except:
                #         print('Directory already exists')
                #     numpy_horizontal_concat = np.concatenate((instance, cv2.cvtColor(att_mask, cv2.COLOR_GRAY2BGR), cv2.cvtColor(def_mask, cv2.COLOR_GRAY2BGR)), axis=1)
                #     cv2.imwrite(results_folder + '\\' + name + '\\person_team' + '\\' + 'team.jpg', numpy_horizontal_concat)
                #     first = False

                (h, w, _) = instance.shape

                # if attColor < 70:
                if (att_comp < h * w * 5 / 100):
                    att_comp = 0
                # print(def_comp, h * w * 5 / 100)
                # if defColor < 70:
                if (def_comp < h * w * 5 / 100):
                    def_comp = 0

                # print(att_comp, def_comp)

                res = 2
                if 0 < def_comp > att_comp:
                    res = 1
                elif att_comp > 0:
                    res = 0

                # print(res)

                f = open(output_path + "\\segmented{}.txt".format(i), "w")
                toWrite = str(startX + (endX - startX) / 2) + " " + str(endY) + "\n" + str(res)
                f.write(toWrite)
                f.close()

            # now, extract *only* the masked region of the ROI by passing in the boolean mask array as our slice condition
            try:
                roi = roi[mask]
                #
                # # Red will be used to visualize this particular instance segmentation
                # # then create a transparent overlay by blending the randomly selected color with the ROI
                blended = ((0.4 * np.array([255, 0, 0])) + (0.6 * roi)).astype("uint8")
                #
                # # store the blended ROI in the original image
                image[startY:endY, startX:endX][mask] = blended

                # draw the bounding box of the instance on the image
                cv2.rectangle(image, (startX, startY), (endX, endY), (255, 255, 255), 2)

                # draw the predicted label and associated probability of the instance segmentation on the image
                text = "{}: {:.4f}".format("Person", confidence)
                cv2.putText(image, text, (startX, startY - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

                # show the output image
                # cv2.imshow("Output", image)
                # cv2.waitKey(0)
            except:
                pass

        if resFlag:
            cv2.imwrite(output_path + '\\' + 'detected.jpg', image)
