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

    #正の角
    def p_kado(x, y):
        return x >=  3.14 * ( (y - 20) / 180) and x <=  3.14 * ( y / 180)

    #負の角
    def n_kado(x, y):
        return x <=  -3.14 * ( (y - 20) / 180) and x >=  -3.14 * ( y / 180)



    for i in range(shape_num):
        f = open(file_list[i])
        data = json.load(f)
        angle = data["angle"]

        #頂点数
        point_num = len(angle)

        ###正角のゾーン!!###
        #20度
        p_kado_20 = float(len(filter(lambda x: x >=  3.14 * ( float(20 - 20) / 180) and x <=  3.14 * ( float(20) / 180) ,angle))) / float(point_num)
        
        #40度
        p_kado_40 = float(len(filter(lambda x: x >=  3.14 * ( float(40 - 20) / 180) and x <=  3.14 * ( float(40) / 180) ,angle))) / float(point_num)

        #60度
        p_kado_60 = float(len(filter(lambda x: x >=  3.14 * ( float(60 - 20) / 180) and x <=  3.14 * ( float(60) / 180) ,angle))) / float(point_num)
        
        #80度
        p_kado_80 = float(len(filter(lambda x: x >=  3.14 * ( float(80 - 20) / 180) and x <=  3.14 * ( float(80) / 180) ,angle))) / float(point_num)

        #100度
        p_kado_100 = float(len(filter(lambda x: x >=  3.14 * (float (100 - 20) / 180) and x <=  3.14 * ( float(100) / 180) ,angle))) / float(point_num)
        
        #120度
        p_kado_120 = float(len(filter(lambda x: x >=  3.14 * ( float(120 - 20) / 180) and x <=  3.14 * ( float(120) / 180) ,angle))) / float(point_num)

        #140度
        p_kado_140 = float(len(filter(lambda x: x >=  3.14 * ( float(140 - 20) / 180) and x <=  3.14 * ( float(140) / 180) ,angle))) / float(point_num)
        
        #160度
        p_kado_160 = float(len(filter(lambda x: x >=  3.14 * ( float(160 - 20) / 180) and x <=  3.14 * ( float(160) / 180) ,angle))) / float(point_num)

        #180度
        p_kado_180= float(len(filter(lambda x: x >=  3.14 * ( float(180 - 20) / 180) and x <=  3.14 * ( float(180) / 180) ,angle))) / float(point_num)
        

        ###負角のゾーン!!###
        #20度
        n_kado_20 = float(len(filter(lambda x: x <=  -3.14 * ( float(20 - 20) / 180) and x >=  -3.14 * ( float(20) / 180) ,angle))) / float(point_num)
        
        #40度
        n_kado_40 = float(len(filter(lambda x: x <=  -3.14 * ( float(40 - 20) / 180) and x >=  -3.14 * ( float(40) / 180) ,angle))) / float(point_num)

        #60度
        n_kado_60 = float(len(filter(lambda x: x <=  -3.14 * ( float(60 - 20) / 180) and x >=  -3.14 * ( float(60) / 180) ,angle))) / float(point_num)
        
        #80度
        n_kado_80 = float(len(filter(lambda x: x <=  -3.14 * ( float(80 - 20) / 180) and x >=  -3.14 * ( float(80) / 180) ,angle))) / float(point_num)

        #100度
        n_kado_100 = float(len(filter(lambda x: x <=  -3.14 * ( float(100 - 20) / 180) and x >=  -3.14 * ( float(100) / 180) ,angle))) / float(point_num)
        
        #120度
        n_kado_120 = float(len(filter(lambda x: x <=  -3.14 * (float (120 - 20) / 180) and x >=  -3.14 * ( float(120) / 180) ,angle))) / float(point_num)

        #140度
        n_kado_140 = float(len(filter(lambda x: x <=  -3.14 * ( float(140 - 20) / 180) and x >=  -3.14 * ( float(140) / 180) ,angle))) / float(point_num)
        
        #160度
        n_kado_160 = float(len(filter(lambda x: x <=  -3.14 * ( float(160 - 20) / 180) and x >=  -3.14 * ( float(160) / 180) ,angle))) / float(point_num)

        #180度
        n_kado_180= float(len(filter(lambda x: x <=  -3.14 * ( float(180 - 20) / 180) and x >=  -3.14 * ( float(180) / 180) ,angle))) / float(point_num)
        



        #データ格納
        
        features_list_for_append = [p_kado_20, p_kado_40, p_kado_60, p_kado_80, p_kado_100, p_kado_120, p_kado_140 , p_kado_160, p_kado_180,
                                    n_kado_20, n_kado_40, n_kado_60, n_kado_80, n_kado_100, n_kado_120, n_kado_140 , n_kado_160, n_kado_180]
        features_list.append(features_list_for_append)

    return features_list 


main()
