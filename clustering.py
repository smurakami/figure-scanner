# -*- coding: utf-8 -*-
import json
import numpy as np
import cv2
import matplotlib.pyplot as plt
import glob
import os
from scipy.cluster.hierarchy import linkage, dendrogram, leaves_list, fcluster
from IPython import embed
import ipdb

#取り急ぎjsonsのtwinkleフォルダ直下で回しました
def main():
    #jsonファイルのファイル名取得
    dirname = 'jsons/twinkle/JPN'
    file_list = glob.glob(os.path.join(dirname, '*.json'))

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


    print "全体の長さ（データの点の数）"
    print len(angle)

    #角度のリストを分割↓のzipのところの数字が○個ずつで分割することを決めています。
    angle_sublist = zip(*[iter(angle)]*50)
    print "サブリストの数"
    print len(angle_sublist)

    mat_size = len(angle_sublist)

    #####################
    #ここからクラスタリング#
    #####################

    #分割でできた角度の推移データの数だけ、ゼロ行列を作っておきます
    dis_mat = np.zeros((mat_size,mat_size))

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
    for x in range(0,mat_size):
        for y in range(0,mat_size):
            dis_mat[x,y] = dtw(angle_sublist[x],angle_sublist[y])

    #距離行列見てみます、対角成分は0です。
    print "距離行列"
    print dis_mat

    #クラスタリング実行
    result = linkage(dis_mat, method = 'average')

    dendrogram(result, p = 20, truncate_mode='lastp')
    plt.show()


    #一定距離で区切ってフラットクラスタリング（△*result[mat_size -2][2]の△の値で深さを調整）
    flat_result = fcluster(result,0.7*result[mat_size -2][2], 'distance')
    flat_result_list = flat_result.tolist()

    ipdb.set_trace()

    angle_sublist = np.array(angle_sublist)
    # 各クラスタの配列を集める
    vertex_for_figure = [angle_sublist[flat_result == l].tolist() for l in np.unique(flat_result)]

    # represent_index = []

    # for s in range(1,max(flat_result_list)+1):
    #     represent_index.append(flat_result_list.index(s))

    # vertex_for_figure = []

    # for t in represent_index:
    #     vertex_for_figure.append(angle_sublist[t])

    with open('clusters/twinkle.json', 'w') as f: json.dump(vertex_for_figure,f, sort_keys=True, indent=4)

main()
