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

#fegure_features.json = [形][ファイルの順番][角の数,丸率、直線率] の形で格納してます
def main():
    shape_list = [
        ['clutter', 'gochagocha'],
        ['murmur', 'sarasara'],
        ['twinkle', 'kirakira'],
    ]

    for_save_list = []

    for shape in shape_list:
        features = cal_Features(shape)
        for_save_list.append(features)

    with open('figure_features.json','w')as f:
        json.dump(for_save_list, f, sort_keys=True, indent=4)


def cal_Features(shape):
    print 'shape:', shape

    shape_en, shape_jp = shape
    dirname_en = 'jsons/%s/*' % shape_en
    file_list_en = glob.glob(os.path.join(dirname_en, '*.json'))

    shape_jp, shape_jp = shape
    dirname_jp = 'jsons/%s/*' % shape_jp
    file_list_jp = glob.glob(os.path.join(dirname_jp, '*.json'))

    file_list = file_list_en + file_list_jp

    ################
    #データリスト作り#️
    ################
    shape_num = len(file_list)

    # features_list = [角の数,丸率、直線率]
    features_list = []

    #角の数
    def kado_fil(x): 
        #直角　= π/2ラジアン = 3.14/2 = 1.57
        return math.fabs(x) >= 1.57
    
    #丸率
    def maru_fil(x): 
        return math.fabs(x) < 1.57 and math.fabs(x) > 0.1745

    #真っ直ぐさ
    def massugu_fil(x):
        #直線 = 10度以内とする　= 0.1745
        return math.fabs(x) <= 0.1745


    for i in range(shape_num):
        f = open(file_list[i])
        data = json.load(f)
        angle = data["angle"]

        #頂点数
        point_num = len(angle)

        #角数
        kado_num = len(filter(kado_fil,angle)) 
        #丸率
        maru_rate = float(len(filter(maru_fil,angle))) / float(point_num)
        #直線率
        massugu_rate = float(len(filter(massugu_fil,angle))) / float(point_num)

        #データ格納
        
        features_list_for_append = [kado_num, maru_rate, massugu_rate]
        features_list.append(features_list_for_append)

    return features_list 


main()
