import glob
import math
import os
import random
import string

import matplotlib.pyplot as plt

from constants import *

import cv2
import numpy as np
from hungarian_algorithm import algorithm


def approx_pixels(i, j, pixels, tol=3):
    for p in pixels:
        if abs(p[0] - i) < tol and abs(p[1] - j) < tol:
            return True
    return False


def detect_color(img):
    pixels_att, pixels_def = [], []
    r, g, b = 0, 255, 0
    rd, gd, bd = 0, 0, 255
    for i in range(len(img)):
        for j in range(len(img[i])):
            pixel = img[i][j]
            if pixel[0] == r and pixel[1] == g and pixel[2] == b:
                if not approx_pixels(i, j, pixels_att):
                    pixels_att.append([i, j])
            if pixel[0] == rd and pixel[1] == gd and pixel[2] == bd:
                if not approx_pixels(i, j, pixels_def):
                    pixels_def.append([i, j])
    return pixels_att, pixels_def


def get_player_pos(players, player):
    return players[int(player)][0]


def get_players_positions(players):
    return [player[0] for player in players.values()]


def get_player_last_detection(players, player):
    return players[player][1]


def set_player_pos(players, player, new_pos):
    players[player][0] = new_pos


def increase_player_last_detection(players, player):
    players[player][1] += 1


def reset_player_last_detection(players, player):
    players[player][1] = 0


def get_name_by_point(players, point):
    for items in players.items():
        if items[1][0] == point:
            return items[0]


twod = cv2.imread("2d.jpg")
twod_c = twod.copy()
# cv2.circle(twod_c, (32, 133), radius=0, color=(0, 255, 0), thickness=10)
# cv2.circle(twod_c, (150, 133), radius=0, color=(0, 255, 0), thickness=10)
# cv2.circle(twod_c, (150, 227), radius=0, color=(0, 255, 0), thickness=10)
# cv2.circle(twod_c, (32, 227), radius=0, color=(0, 255, 0), thickness=10)
#
# plt.imshow(cv2.cvtColor(twod_c, cv2.COLOR_BGR2RGB))
# plt.title('HL')
# plt.show()


def check_inbounds(p):
    if p[1] < 20 or p[1] > 605 or p[0] < 30 or p[0] > 330:
        return False
    return True

def find_closest(point, points):
    if len(points) == 0 or point is None:
        return None
    min_dist = math.sqrt(math.pow((point[0] - points[0][0]), 2) + math.pow((point[1] - points[0][1]), 2))
    min_point = points[0]
    for p in points:
        d = math.sqrt(math.pow((point[0] - p[0]), 2) + math.pow((point[1] - p[1]), 2))
        if d < min_dist:
            min_dist = d
            min_point = p
    return min_point

def euclidean_distance(point1, point2):
    return math.sqrt(math.pow((point1[0] - point2[0]), 2) + math.pow((point1[1] - point2[1]), 2))


def points_are_close(curr, prev, tol = 20):
    return abs(curr[0] - prev[0]) < tol and abs(curr[1] - prev[1]) < tol


def get_unguarded_attacker(res):
    if len(res) == 0:
        return None, None
    max_dist = 0
    best_att = res[0][0][1][-1:]
    for r in res:
        if r[1] > max_dist:
            max_dist = r[1]
            best_att = r[0][1][-1:]
    return best_att, max_dist

def hoop_dist_attackers(attack, hoop_pos):
    res = {}
    for att in list(attack):
        dist = euclidean_distance(get_player_pos(attack, att), hoop_pos)
        res[att] = dist
    return res


def remove_far_attackers(res, att_dist):
    result = []
    for att in res:
        name = int(att[0][1][-1:])
        if name in list(att_dist):
            if att_dist[name] < 160:
                result.append(att)
    return result

def remove_smallest_confidence(players):
    min = 300
    min_conf = list(players)[0]
    for player in list(players):
        conf = players[player][2]
        if conf < min:
            min = conf
            min_conf = player
    players.pop(min_conf)


def hung_alg(attack, defence, hoop_pos):
    att_dist = hoop_dist_attackers(attack, hoop_pos)
    while len(attack) - len(defence) > 1:
        remove_smallest_confidence(attack)

    while len(attack) - len(defence) < -1:
        remove_smallest_confidence(defence)
    #compute match ups
    G = {}
    for dif in defence.items():
        res = {}
        for att in attack.items():
            res['a' + str(att[0])] = int(euclidean_distance(dif[1][0], att[1][0]))
        G['d' + str(dif[0])] = res
    res = algorithm.find_matching(G, matching_type='min', return_type='list')
    res = remove_far_attackers(res, att_dist)
    return get_unguarded_attacker(res)


def homography(frame_path, side):
    try:
        os.mkdir(results_folder + '\\' + frame_path)
    except:
        print('Directory already exists')

    try:
        os.mkdir(results_folder + '\\' + frame_path + '\\homography')
    except:
        print('Directory already exists')
    prev_att = {}
    prev_def = {}
    lu, ru, rd, ld = 0, 0, 0, 0
    pts_dst_left = np.array([[32, 133], [150, 133], [150, 227], [32, 227]])
    pts_dst_right = np.array([[475, 133], [591, 133], [591, 227], [475, 227]])
    res = []
    img_info = []
    hoop_pos = [180, 555]
    max_dist = 0

    images_path = glob.glob(processing_folder + '\\' + frame_path + "\*.jpg")
    for im_path in images_path:
        im_name = im_path.split('\\')[-1].split('.')[0]
        img = cv2.imread(im_path)
        img_c = img.copy()

        f = open(processing_folder + '\\' + frame_path + '\\' + im_name + '_paint.txt', 'r')
        line = f.readline()
        f.close()
        tokens = line.split(" ")
        if 'None' not in tokens:
            lu = [int(tokens[0][1:-1]), int(tokens[1][:-1])]
            ru = [int(tokens[2][1:-1]), int(tokens[3][:-1])]
            rd = [int(tokens[4][1:-1]), int(tokens[5][:-1])]
            ld = [int(tokens[6][1:-1]), int(tokens[7][:-1])]
        if lu == 0 or ru == 0 or rd == 0 or ld == 0:
            continue
        # print(lu, ru, rd, ld)

        # Four corners of the 3D court in source image (start top-left corner and go clock wise)
        pts_src = np.array([[lu[1], lu[0]], [ru[1], ru[0]], [rd[1], rd[0]], [ld[1], ld[0]]])


        # Calculate Homography
        if(side == 'left'):
            h, status = cv2.findHomography(pts_src, pts_dst_left)
            hoop_pos = [180, 70]
        else:
            h, status = cv2.findHomography(pts_src, pts_dst_right)
            hoop_pos = [180, 555]

        # Warp source image to destination based on homography
        # draw players
        player_positions = glob.glob(processing_folder + '\\' + frame_path + '\\' + im_name + '\*.txt')
        for pp in player_positions:
            f = open(pp, 'r')
            line = f.readline()
            x = int(float(line.split(' ')[0]))
            y = int(float(line.split(' ')[1]))
            team = int(f.readline())
            f.close()
            if team == 0:
                cv2.circle(img, (x, y), radius=1, color=(0, 255, 0), thickness=5)
            elif team == 1:
                cv2.circle(img, (x, y), radius=1, color=(0, 0, 255), thickness=5)

        # plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        # plt.title('HL')
        # plt.show()
        twod_c = twod.copy()
        twod_c2 = twod.copy()

        img_out = cv2.warpPerspective(img, h, (twod.shape[1], twod.shape[0]))
        # plt.imshow(cv2.cvtColor(img_out, cv2.COLOR_BGR2RGB))
        # plt.title('HL')
        # plt.show()
        attack, defence = detect_color(img_out)
        curr_att = []
        curr_def = []
        for att in attack:
            if check_inbounds(att):
                cv2.circle(twod_c, (att[1], att[0]), radius=1, color=(0, 255, 0), thickness=10)
                if not approx_pixels(att[0], att[1], curr_att, 10):
                    curr_att.append(att)
        for d in defence:
            if check_inbounds(d):
                cv2.circle(twod_c, (d[1], d[0]), radius=1, color=(0, 0, 255), thickness=10)
                if not approx_pixels(d[0], d[1], curr_def, 10):
                    curr_def.append(d)

        if len(prev_att) == 0 and len(prev_def) == 0:
            for i in range(len(curr_att)):
                prev_att[i] = [curr_att[i], 0, 1]
            for i in range(len(curr_def)):
                prev_def[i] = [curr_def[i], 0, 1]
        else:
            res_att = {}
            # players found in consecutive frames
            cc = curr_att.copy()
            for att in cc:
                prev = find_closest(att, get_players_positions(prev_att))
                curr = find_closest(prev, curr_att)
                if curr == att:
                    name = get_name_by_point(prev_att, prev)
                    #if matched points are close then we excanhge old point for new and grow its confidence meter
                    if points_are_close(curr, prev, 60):
                        curr_att.remove(curr)
                        prev_val = prev_att.pop(name)
                        res_att[name] = [curr, 0, prev_val[2] + 1]
                    #if not close, we exchange only if confience is low
                    elif prev_att[name][2] < 10:
                        curr_att.remove(curr)
                        prev_val = prev_att.pop(name)
                        res_att[name] = [curr, 0, 0]
            # previous players not found in next frame
            added_from_prev = []
            for att in prev_att.items():
                if len(res_att) < 5:
                    res_att[att[0]] = [att[1][0], att[1][1] + 1, att[1][2]]
                    added_from_prev.append(att[0])
            # remove players not found in 10 previous frames
            for key in list(res_att):
                if get_player_last_detection(res_att, key) > 5:
                    res_att.pop(key)
                    added_from_prev.remove(key)

            # new players not found in last frame
            for att in curr_att:
                pos = get_players_positions(res_att)
                for name in added_from_prev:
                    if points_are_close(att, get_player_pos(res_att, name), 15):
                        continue
                if len(res_att) < 5:
                    res_att[np.max(list(res_att)) + 1] = [att, 0, 1]

            prev_att = res_att

            new_att_pos = get_players_positions(res_att)
            for att in new_att_pos:
                cv2.circle(twod_c2, (att[1], att[0]), radius=1, color=(0, 255, 0), thickness=10)

            res_def = {}
            # players found in consecutive frames
            cc = curr_def.copy()
            for dif in cc:
                prev = find_closest(dif, get_players_positions(prev_def))
                curr = find_closest(prev, curr_def)
                if curr == dif:
                    name = get_name_by_point(prev_def, prev)
                    #if matched points are close then we excanhge old point for new and grow its confidence meter
                    if points_are_close(curr, prev, 60):
                        curr_def.remove(curr)
                        prev_val = prev_def.pop(name)
                        res_def[name] = [curr, 0, prev_val[2] + 1]
                    #if not close, we exchange only if confience is low
                    elif prev_def[name][2] < 10:
                        curr_def.remove(curr)
                        prev_val = prev_def.pop(name)
                        res_def[name] = [curr, 0, 0]
            # previous players not found in next frame
            added_from_prev = []
            for dif in prev_def.items():
                if len(res_def) < 5:
                    res_def[dif[0]] = [dif[1][0], dif[1][1] + 1, dif[1][2]]
                    added_from_prev.append(dif[0])
            # remove players not found in 10 previous frames
            for key in list(res_def):
                if get_player_last_detection(res_def, key) > 5:
                    res_def.pop(key)
                    added_from_prev.remove(key)

            # new players not found in last frame
            for dif in curr_def:
                #check if they were added from prev frame
                pos = get_players_positions(res_def)
                for name in added_from_prev:
                    if points_are_close(dif, get_player_pos(res_def, name), 15):
                        continue
                #add if not already in and number of players is smaller than 5
                if len(res_def) == 0:
                    res_def[0] = [dif, 0, 1]
                elif len(res_def) < 5:
                    res_def[np.max(list(res_def)) + 1] = [dif, 0, 1]

            prev_def = res_def

            new_def_pos = get_players_positions(res_def)
            for dif in new_def_pos:
                cv2.circle(twod_c2, (dif[1], dif[0]), radius=1, color=(0, 0, 255), thickness=10)

            best_att, max_d = hung_alg(res_att, res_def, hoop_pos)

            if best_att is None or max_d is None:
                continue

            pos = get_player_pos(res_att, best_att)
            cv2.circle(twod_c2, (pos[1], pos[0]), radius=1, color=(255, 0, 0), thickness=10)

            if(max_d > max_dist):
                final_td = twod_c2.copy()
                res.append([final_td, im_name, pts_src])
                max_dist = max_d
                final_td_c = final_td.copy()
                cv2.imwrite(results_folder + '\\' + frame_path + '\\homography' + '\\' + 'result.jpg', final_td_c)
                cv2.circle(final_td_c, (pos[1], pos[0]), radius=1, color=(0, 255, 0), thickness=10)
                cv2.imwrite(results_folder + '\\' + frame_path + '\\homography' + '\\' + 'homography.jpg', final_td_c)
                # plt.imshow(cv2.cvtColor(final_td, cv2.COLOR_BGR2RGB))
                # plt.title('Detected')
                # plt.show()
        print(im_name)

        # cv2.circle(img_out, (42, 188), radius=0, color=(0, 255, 0), thickness=10)
        # cv2.circle(img_out, (42, 276), radius=0, color=(0, 255, 0), thickness=10)
        # cv2.circle(img_out, (182, 188), radius=0, color=(0, 255, 0), thickness=10)
        # cv2.circle(img_out, (182, 276), radius=0, color=(0, 255, 0), thickness=10)

        # fig = plt.figure(figsize=(15, 15))
        # fig.add_subplot(1, 3, 1)
        # plt.imshow(cv2.cvtColor(img_c, cv2.COLOR_BGR2RGB))
        # plt.title('OG')
        # fig.add_subplot(1, 3, 2)
        # plt.imshow(cv2.cvtColor(twod_c, cv2.COLOR_BGR2RGB))
        # plt.title('Detected')
        # fig.add_subplot(1, 3, 3)
        # plt.imshow(cv2.cvtColor(twod_c2, cv2.COLOR_BGR2RGB))
        # plt.title('Detected')
        # plt.show()


    def colorize_detection(img_out, im):
        r, g, b = 255, 0, 0
        for i in range(len(img_out)):
            for j in range(len(img_out[i])):
                pixel = img_out[i][j]
                if pixel[0] == r and pixel[1] == g and pixel[2] == b:
                    im[i][j] = [255, 0, 0]

    def return_to_3d(twod, image_name, pts_src):
        im = cv2.imread(processing_folder + '\\' + frame_path + '\\' + image_name + '.jpg')

        if (side == 'left'):
            h, status = cv2.findHomography(pts_dst_left, pts_src)
        else:
            h, status = cv2.findHomography(pts_dst_right, pts_src)
            # hoop_pos = [180, 555]

        img_out = cv2.warpPerspective(twod, h, (im.shape[1], im.shape[0]))
        colorize_detection(img_out, im)
        # plt.imshow(cv2.cvtColor(im, cv2.COLOR_BGR2RGB))
        # plt.title('Detected')
        # plt.show()
        letters = string.ascii_lowercase
        res_name = ''.join(random.choice(letters) for i in range(10))
        cv2.imwrite(results_folder + '\\' + frame_path + '\\' + res_name + '.jpg', im)
        print(results_folder + '\\' + frame_path + '\\' + res_name + '.jpg')
        return res_name


    save_results = []
    try:
        os.mkdir(results_folder + '\\' + frame_path)
    except:
        print('Directory already exists')
    res1 = res[-5:]
    if len(res1) > 1:
        res1 = res1[1:]
    for imgs in res1:
        save_results.append(return_to_3d(imgs[0], imgs[1], imgs[2]) + '.jpg')
        # fig = plt.figure(figsize=(15, 15))
        # fig.add_subplot(1, 3, 1)
        # plt.imshow(cv2.cvtColor(imgs[0], cv2.COLOR_BGR2RGB))
        # plt.title('Detected')
        # fig.add_subplot(1, 3, 2)
        # im = cv2.imread(processing_folder + '\\' + frame_path + '\\' + imgs[1] + '.jpg')
        # plt.imshow(cv2.cvtColor(im, cv2.COLOR_BGR2RGB))
        # plt.title('OG')
        # plt.show()

    return save_results
