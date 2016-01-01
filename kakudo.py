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


#取り急ぎjsonsのtwinkleフォルダ直下で回しました
def main():
    shape_list = [
        ['clutter', 'gochagocha']
    ]
    for shape in shape_list:
        cul_Kakudo(shape)


def cul_Kakudo(shape):
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

    #とりあえずhatayamaさんので試してみましょう。
    f = open(file_list[4])
    data = json.load(f)
    angle = data["angle"]

    point_num = len(angle)

    print "頂点数",
    print point_num

    #角の数
    def kado_num(x): 
        #直角　= π/2ラジアン = 3.14/2 = 1.57
        return math.fabs(x) >= 1.57

    print "角の数" ,
    print len(filter(kado_num,angle)) 

    #丸さ
    def maru_num(x): 
        return math.fabs(x) < 1.57 and math.fabs(x) > 0.1745

    print "丸率",
    print float(len(filter(maru_num,angle))) / float(point_num)


    #真っ直ぐさ
    def massugu_num(x):
        #直線 = 10度以内とする　= 0.1745
        return math.fabs(x) <= 0.1745

    print "真っ直ぐ率",
    print float(len(filter(massugu_num,angle))) / float(point_num)

    plt.plot(angle)
    plt.show()


main()
