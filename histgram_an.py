# -*- coding: utf-8 -*-
import json
import numpy as np
import matplotlib.pyplot as plt
import os

f = open('figure_features.json')
data = json.load(f)
data = np.array(data)

gocha_data = data[0]
sara_data = data[1]
kira_data = data[2]

def main():	

	seikaku()
	fukaku()
	seimaru()
	fumaru()
	massugu()



def seikaku():
	gocha_kaku_list = []
	sara_kaku_list = []
	kira_kaku_list = []

	for row in gocha_data:	
		gocha_kaku_list.append(row[0])

	for row in sara_data:	
		sara_kaku_list.append(row[0])

	for row in kira_data:	
		kira_kaku_list.append(row[0])

	plt.subplot(221)
	plt.hist(gocha_kaku_list)
	plt.title("clutter,gochagocha")
	plt.subplot(222)
	plt.hist(sara_kaku_list)
	plt.title("murmur,sarasara")
	plt.subplot(223)
	plt.hist(kira_kaku_list)
	plt.title("twinkle,kirakira")
	plt.suptitle("seikaku")
	plt.show()

def fukaku():
	gocha_kaku_list = []
	sara_kaku_list = []
	kira_kaku_list = []

	for row in gocha_data:	
		gocha_kaku_list.append(row[1])

	for row in sara_data:	
		sara_kaku_list.append(row[1])

	for row in kira_data:	
		kira_kaku_list.append(row[1])

	plt.subplot(221)
	plt.hist(gocha_kaku_list)
	plt.title("clutter,gochagocha")
	plt.subplot(222)
	plt.hist(sara_kaku_list)
	plt.title("murmur,sarasara")
	plt.subplot(223)
	plt.hist(kira_kaku_list)
	plt.title("twinkle,kirakira")
	plt.suptitle("fukaku")
	plt.show()

def seimaru():
	gocha_kaku_list = []
	sara_kaku_list = []
	kira_kaku_list = []

	for row in gocha_data:	
		gocha_kaku_list.append(row[2])

	for row in sara_data:	
		sara_kaku_list.append(row[2])

	for row in kira_data:	
		kira_kaku_list.append(row[2])

	plt.subplot(221)
	plt.hist(gocha_kaku_list)
	plt.title("clutter,gochagocha")
	plt.subplot(222)
	plt.hist(sara_kaku_list)
	plt.title("murmur,sarasara")
	plt.subplot(223)
	plt.hist(kira_kaku_list)
	plt.title("twinkle,kirakira")
	plt.suptitle("seimaru")
	plt.show()

def fumaru():
	gocha_kaku_list = []
	sara_kaku_list = []
	kira_kaku_list = []

	for row in gocha_data:	
		gocha_kaku_list.append(row[3])

	for row in sara_data:	
		sara_kaku_list.append(row[3])

	for row in kira_data:	
		kira_kaku_list.append(row[3])

	plt.subplot(221)
	plt.hist(gocha_kaku_list)
	plt.title("clutter,gochagocha")
	plt.subplot(222)
	plt.hist(sara_kaku_list)
	plt.title("murmur,sarasara")
	plt.subplot(223)
	plt.hist(kira_kaku_list)
	plt.title("twinkle,kirakira")
	plt.suptitle("fumaru")
	plt.show()

def massugu():
	gocha_kaku_list = []
	sara_kaku_list = []
	kira_kaku_list = []

	for row in gocha_data:	
		gocha_kaku_list.append(row[4])

	for row in sara_data:	
		sara_kaku_list.append(row[4])

	for row in kira_data:	
		kira_kaku_list.append(row[4])

	plt.subplot(221)
	plt.hist(gocha_kaku_list)
	plt.title("clutter,gochagocha")
	plt.subplot(222)
	plt.hist(sara_kaku_list)
	plt.title("murmur,sarasara")
	plt.subplot(223)
	plt.hist(kira_kaku_list)
	plt.title("twinkle,kirakira")
	plt.suptitle("massugu")
	plt.show()


main()