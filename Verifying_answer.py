# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 22:23:22 2017

@author: lenovo
"""
import os

from math import log

import numpy as np

def testitems(): 
    '''读取测试商品'''
    with open(current_path + '/线下测试集.csv', "r") as f:
        test_items = []
        for line in f:
            arr = line.replace("\n","").split(" ")
            test_items.append((arr[0]))
    return test_items

current_path = os.path.abspath('.')

ap_200 = []
map_200 = 0

test_items = testitems()

with open(current_path + '/answer.csv', "r") as f:
    answer_dict = {}
    for line in f:
        arr = line.replace('\n','').split(' ')
        answer_dict[arr[0]] = arr[1].split(',')
    
with open(current_path + '/underlinetest/Model_fusion/my_answer.csv', "r") as f:
    fm_submissions_dict = {}
    for line in f:
        arr = line.replace('\n','').split(' ')
        try:
            fm_submissions_dict[arr[0]] = arr[1].split(',')
        except IndexError:
            fm_submissions_dict[arr[0]] = []
        
for item in test_items:
    answer = answer_dict[item]
    fm_submissions = fm_submissions_dict[item] 
    P = []
    deta = []
    score = 0
    for k in range(len(fm_submissions)):
        if fm_submissions[k] in answer:
            score += 1
            P.append(score/(k+1))
            deta.append(1)
        else:
            P.append(score/(k+1))
            deta.append(0)
    ap = 0 
    for k in range(len(fm_submissions)):
        if deta[k] == 0:
            ap += 0
        else:
            ap += deta[k]#/( 1 - log(P[k]) ) 
    
    ap_200.append(ap/len(answer))
    
ap_200 = np.array(ap_200)

result = ap_200.sum()/len(test_items)
print(result)