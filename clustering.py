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
#import ipdb


#取り急ぎjsonsのtwinkleフォルダ直下で回しました
def main():
    shape_list = [
        ['clutter', 'gochagocha'],
        ['murmur', 'sarasara'],
        ['twinkle', 'kirakira'],
    ]
    for shape in shape_list:
        clusterShape(shape)


def clusterShape(shape):
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

    #角度のリストを生成（各人のデータを繋げて長いリストにします。）
    f = open(file_list[0])
    data = json.load(f)
    angle = data["angle"]

    for i in file_list[1:]:
        f2 = open(i)
        data2 = json.load(f2)
        angle_for_append = data2["angle"]
        angle.extend(angle_for_append)

    print "全体の長さ（データの点の数）",
    print len(angle)

    #角度のリストを分割↓のzipのところの数字が○個ずつで分割することを決めています。
    angle_sublist = zip(*[iter(angle)]*50)
    print "サブリストの数",
    print len(angle_sublist)

    mat_size = len(angle_sublist)

    #####################
    #ここからクラスタリング#
    #####################

    #分割でできた角度の推移データの数だけ、ゼロ行列を作っておきます
    dis_mat = np.zeros((mat_size, mat_size))

    #距離ベクトルの獲得DTW計算
    def dtw(vec1, vec2):
        import numpy as np
        d = np.zeros([len(vec1)+1, len(vec2)+1])
        d[:] = np.inf
        d[0, 0] = 0
        for i in range(1, d.shape[0]):
            for j in range(1, d.shape[1]):
                cost = abs(vec1[i-1]-vec2[j-1])
                d[i, j] = cost + min(d[i-1, j], d[i, j-1], d[i-1, j-1])
        return d[-1][-1]

    #距離行列作成
    print 'mat_size:', mat_size
    for x in range(mat_size):
        print x,
        sys.stdout.flush()
        for y in range(0, x + 1):
            dist = dtw(angle_sublist[x], angle_sublist[y])
            dis_mat[x, y] = dist
            dis_mat[y, x] = dist



    #距離行列見てみます、対角成分は0です。
    print "距離行列",
    print dis_mat

    #クラスタリング実行
    result = linkage(dis_mat, method='average')

    # dendrogram(result, p=20, truncate_mode='lastp')
    # plt.show()

    #########################################################
    #クラスタの上位からクラスタ要素数10以下のものを選んでいくどーん！#
    #########################################################
    #フラットクラスタリングで切りまくって階層を上からサーチしていきます。
    angle_sublist = np.array(angle_sublist)
    #index溜め込み用のセット
    number_pool = []
    number_pool = set(number_pool)
    #クラスタのリスト
    cluster_vertex = []
    #最終出力する３次元配列のリスト
    figure_vertex_list = []

    for x in range(9, 0, -1):
        flat_result = fcluster(
            result, x * 0.1 * result[mat_size - 2][2], 'distance')
        #一定の値で階層クラスタリングを切って、各クラスタを探索
        for y in np.unique(flat_result):
            #各クラスタの要素数が10以下の場合
            if len(np.where(flat_result == y)[0]) <= 10 and len(np.where(flat_result == y)[0]) >= 5:
                #そのクラスタがすでに認識したクラスタの要素でない場合
                if len(set(np.where(flat_result == y)[0].tolist()) - number_pool) == len(set(np.where(flat_result == y)[0].tolist())):
                    #全体のリスト（figure_vertex_list）に、クラスタのリスト(cluster_vertex)を追加
                    figure_vertex_list.append(cluster_vertex)
                    #クラスタのリストの要素を空に
                    cluster_vertex = []
                    #追加のindexをsetに保存
                    number_pool = list(number_pool)
                    number_pool.extend(np.where(flat_result == y)[0].tolist())
                    number_pool = set(number_pool)
                    print number_pool
                    print np.where(flat_result == y)
                    #クラスタ内の要素の角度のリストを作ります、それがcluster_vertex
                    for l in np.where(flat_result == y)[0]:
                        ap_V_figure = angle_sublist[l].tolist()
                        cluster_vertex.append(ap_V_figure)

    del figure_vertex_list[0]

    """
    #一定距離で区切ってフラットクラスタリング（△*result[mat_size -2][2]の△の値で深さを調整）
    flat_result = fcluster(result,0.7*result[mat_size -2][2], 'distance')
    flat_result_list = flat_result.tolist()

    angle_sublist = np.array(angle_sublist)
    # 各クラスタの配列を集める
    vertex_for_figure = [angle_sublist[flat_result == l].tolist() for l in np.unique(flat_result)]

    # represent_index = []

    # for s in range(1,max(flat_result_list)+1):
    #     represent_index.append(flat_result_list.index(s))

    # vertex_for_figure = []

    # for t in represent_index:
    #     vertex_for_figure.append(angle_sublist[t])
    """
    with open('clusters/%s_%s.json' % (shape_en, shape_jp), 'w') as f:
        json.dump(figure_vertex_list, f, sort_keys=True, indent=4)

main()
