import sys
import cv2
import os

video = str(sys.argv[1])
delta_t = float(sys.argv[2])
path_to_save = str(sys.argv[3])

try:
    os.mkdir(path_to_save)
except:
    print('Directory already exists')

cap = cv2.VideoCapture(video)
fps = cap.get(cv2.CAP_PROP_FPS)
save_frame = fps * delta_t
i = 0
while (cap.isOpened()):
    ret, frame = cap.read()
    if ret == False:
        break
    if i % save_frame == 0:
        cv2.imwrite(path_to_save + '/' + video.split('\\')[-1][:-4] + str(i).zfill(3) + '.jpg', frame)
    i += 1

cap.release()
