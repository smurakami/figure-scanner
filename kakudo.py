# -*- coding: utf-8 -*-
import json
import numpy as np
import cv2
import matplotlib.pyplot as plt
import glob
import os
from scipy.cluster.hierarchy import linkage, dendrogram, leaves_list, fcluster
from IPython import embed
import sys
import math
#import ipdb

#fegure_features.json = [形][ファイルの順番][正角の率,負角の率、外側への丸率、内側への丸率、直線率] の形で格納してます
def main():
    onomatpeia_list = [
        'clutter', 'gochagocha',
        'murmur', 'sarasara',
        'twinkle', 'kirakira',
    ]

    for_save_list = []
    dirname_list = []

    for onomatpeia in onomatpeia_list:
        dirname_pattern = 'jsons/%s/*' % onomatpeia
        print dirname_pattern
        for dirname in sorted(glob.glob(dirname_pattern)):
            features, files = cal_Features(dirname)
            dirname_list.append(files)
            for_save_list.append(features)

    with open('figure_features.json', 'w')as f:
        json.dump(for_save_list, f, sort_keys=True, indent=4)
    with open('figure_features_filename.json', 'w')as f:
        json.dump(dirname_list, f, sort_keys=True, indent=4)


def cal_Features(dirname):
    file_list = glob.glob(os.path.join(dirname, '*.json'))

    ################
    #データリスト作り#️
    ################
    shape_num = len(file_list)

    # features_list = [角の数,丸率、直線率]
    features_list = []

    for i in range(shape_num):
        f = open(file_list[i])
        data = json.load(f)
        angle = data["angle"]

        hist, _ = np.histogram(angle, bins=18, range=(-np.pi, np.pi))
        feature = hist / float(hist.sum())
        features_list.append(feature.tolist())

    return features_list, file_list


main()
