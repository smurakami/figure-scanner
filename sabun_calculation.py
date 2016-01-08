# -*- coding: utf-8 -*-
import json
import numpy as np
import glob
import math
import os

dat = json.load(open("figure_features_jp_en.json"))
dirname = glob.glob('jsons/*/*')

for shape, d in zip(dat, dirname):
    shape = np.array(shape)
    print d, "\t", shape.mean(0)

