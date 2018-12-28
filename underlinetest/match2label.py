# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 21:56:15 2017

@author: pleasecallmekaige
"""
import time
import os
from collections import Counter

import tianc_tfidf as tff

current_path = os.path.abspath('.')


def get_Package2Category_match_dict(item2labels_dict):
    Package2Category_match_dict = {}  # 套餐对应类目搭配的字典
    with open(current_path + "/../data/dim_fashion_matchsets.txt", "r") as f:
        for line in f:
            arr = line.replace("\n","").split(" ")
            pairs = arr[1].split(";")
            p = []
            for pair in pairs:
                item = pair.split(",")[0]
                p.append(item2labels_dict[item])
            Package2Category_match_dict[arr[0]] = p
    return Package2Category_match_dict


item2labels_dict = tff.classification()  # 获取每个item的类目
Package2Category_match_dict = get_Package2Category_match_dict(item2labels_dict)     # 套餐对应类目搭配的字典  
all_labels = sorted(set(item2labels_dict.values()))

test_items = tff.testitems()  # 获取测试商品
#label2labels_dict = item2labels_dict(test_items[0])
#allitems = tff.get_allitem()   

test_items2matchlabels_dict = {}

len_test = len(test_items) #测试商品的个数

start = time.clock()

Category_list = [] 
Package_list = [] 

text = ''
count_text = ''
for num in range(len_test):
    label = item2labels_dict[test_items[num]]
    for k,v in Package2Category_match_dict.items():
        if label in v:
            v.remove(label)
            Category_list.extend(v)
            #Package_list.append(k)
    count = Counter(Category_list)
    out_labels  = sorted(count.items(), key = lambda s: s[1], reverse=True)
        
    #print(test_items[num] +'labels'+item2labels_dict[test_items[num]] + ':',Category_list)
    test_items2matchlabels_dict[test_items[num]] = Category_list

    text = text + test_items[num] + ' '
    count_text = count_text + test_items[num] + ' '
    for j in range(len(out_labels)):
        text = text + out_labels[j][0] + ','
        count_text = count_text + str(out_labels[j][1]) + ','
    text = text[:-1] + '\n'
    count_text = count_text[:-1] + '\n'
    print(num)
    
with open(current_path + '/label_match/test_items2matchlabels_xx.csv', "w") as f:
    f.write(text)

with open(current_path + '/label_match/test_items2matchlabels_count.csv', "w") as f:
    f.write(count_text)
    
elapsed = (time.clock() - start)
print("Time used:",elapsed)