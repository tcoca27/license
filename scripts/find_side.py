import glob
import sys
from collections import defaultdict

import numpy as np
import cv2

def angle(line):
    x1, y1, x2, y2 = line[0]
    angle = np.arctan2(y2 - y1, x2 - x1)
    return angle % (2 * np.pi)

def get_mean_angle(lines):
    angles = [angle(line) % np.pi for line in lines]
    return np.mean(angles, axis=0)

def segment_by_angle_kmeans(lines, k=2, **kwargs):
    default_criteria_type = cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER
    criteria = kwargs.get("criteria", (default_criteria_type, 10, 1.0))
    flags = kwargs.get("flags", cv2.KMEANS_RANDOM_CENTERS)
    attempts = kwargs.get("attempts", 10)

    # returns angles in [0, π)
    angles = [angle(line) % np.pi for line in lines]
    # stretch angles to the full range and map to coords
    pts = np.array(
        [[[np.cos(2 * angle), np.sin(2 * angle)]] for angle in angles], dtype=np.float32
    )
    # run kmeans on unit coordinates of the angle
    labels, centers = cv2.kmeans(pts, k, None, criteria, attempts, flags)[1:]
    labels = labels.reshape(-1)  # transpose to row vec

    # segment lines based on their kmeans label
    segmented = defaultdict(list)
    for i, line in zip(range(len(lines)), lines):
        segmented[labels[i]].append(line)
    segmented = list(segmented.values())
    return segmented

frame_path = str(sys.argv[1])
images_path = glob.glob(frame_path + "\*.jpg")
side = 'left'
for im_path in images_path[:1]:
    img = cv2.imread(im_path)
    line_image = np.copy(img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    kernel = np.ones((4, 4), np.uint8)
    gray = cv2.erode(gray, kernel, iterations=1)

    kernel_size = 5
    blur_gray = cv2.GaussianBlur(gray, (kernel_size, kernel_size), 0)

    low_threshold = 100
    high_threshold = 200
    edges = cv2.Canny(blur_gray, low_threshold, high_threshold)

    rho = 1  # distance resolution in pixels of the Hough grid
    theta = np.pi / 180  # angular resolution in radians of the Hough grid
    threshold = 30  # minimum number of votes (intersections in Hough grid cell)
    min_line_length = 100  # minimum number of pixels making up a line
    max_line_gap = 10  # maximum gap in pixels between connectable line segments

    lines = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]), min_line_length, max_line_gap)

    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(line_image, (x1, y1), (x2, y2), (255, 255, 0), 5)

    segmented = segment_by_angle_kmeans(lines)
    if len(segmented[0]) > len(segmented[1]):
        angle_perp = get_mean_angle(segmented[1])
        angle_parallel = get_mean_angle(segmented[0])
    else:
        angle_perp = get_mean_angle(segmented[0])
        angle_parallel = get_mean_angle(segmented[1])

    if angle_perp > angle_parallel:
        print('left')
    else:
        print('right')