import cv2
import os
from constants import *


def get_frames_from_video(name, delta_t, res=False):
    video_path = videos_folder + "\\" + name + ".mp4"
    path_to_save = processing_folder + "\\" + name
    path_to_save_res = results_folder + "\\" + name + '\\frames'
    try:
        os.mkdir(path_to_save)
    except:
        print('Directory already exists')

    try:
        os.mkdir(path_to_save_res)
    except:
        print('Directory already exists')

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    save_frame = fps * delta_t
    i = 0
    while (cap.isOpened()):
        ret, frame = cap.read()
        if ret == False:
            break
        if i % save_frame == 0:
            if res:
                cv2.imwrite(path_to_save_res + '/' + video_path.split('\\')[-1][:-4] + str(i).zfill(3) + '.jpg', frame)
            else:
                cv2.imwrite(path_to_save + '/' + video_path.split('\\')[-1][:-4] + str(i).zfill(3) + '.jpg', frame)
        i += 1

    cap.release()
