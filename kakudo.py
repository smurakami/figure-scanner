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
    def kado_fil(x): 
        #直角　= π/2ラジアン = 3.14/2 = 1.57
        return math.fabs(x) >= 1.57

    kado_num = len(filter(kado_fil,angle)) 

    print "角の数" ,
    print kado_num

    #丸さ
    def maru_fil(x): 
        return math.fabs(x) < 1.57 and math.fabs(x) > 0.1745

    maru_rate = float(len(filter(maru_fil,angle))) / float(point_num)
    print "丸率",
    print maru_rate


    #真っ直ぐさ
    def massugu_fil(x):
        #直線 = 10度以内とする　= 0.1745
        return math.fabs(x) <= 0.1745

    massugu_rate = float(len(filter(massugu_fil,angle))) / float(point_num)
    print "真っ直ぐ率",
    print massugu_rate

    plt.plot(angle)
    plt.show()


main()
