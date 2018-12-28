# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 14:09:18 2017

@author: lenovo
"""
import os
import numpy as np
import tianc_tfidf as tff
import time

current_path = os.path.abspath('.')

def m_intersection(a,b):
    """
    取交集
    """
    return list(set(a).intersection(set(b)))

'''test = tff.testitems()
item2labels_dict = tff.classification()  # 获取每个item的类目
all_items = tff.get_allitem() # 所有的商品
item2infos_dict = tff.infomation()  # 获取每一个item的标题'''
'''with open(current_path + '/../tfidf_data/top800xx.csv', "r") as f:
    top800xx = {}
    for line in f:
        arr = line.replace('\n','').split(' ')
        try:
            top800xx[arr[0]] = arr[1].split(',')
        except IndexError:
            top800xx[arr[0]] = []
            
            
with open(current_path + '/../tfidf_data/similar.csv', "r") as f:
    similar = {}
    for line in f:
        arr = line.replace('\n','').split(' ')
        try:
            pair = arr[1].split(',')
            p = []
            for i in range(len(pair)):
                p.append(float(pair[i]))
                similar[arr[0]] = p
        except IndexError:
            similar[arr[0]] = []
            
with open(current_path + '/../rule1_data/同一天被同一用户购买的商品.csv', "r") as f:
    sameday = {}
    for line in f:
        arr = line.replace('\n','').split(' ')
        try:
            sameday[arr[0]] = arr[1].split(',')
        except IndexError:
            sameday[arr[0]] = []
            
            
with open(current_path + '/../rule1_data/共同购买数.csv', "r") as f:
    sameday_buynum = {}
    for line in f:
        arr = line.replace('\n','').split(' ')
        try:
            pair = arr[1].split(',')
            p = []
            for i in range(len(pair)):
                p.append(int(pair[i]))
                sameday_buynum[arr[0]] = p
        except IndexError:
            sameday_buynum[arr[0]] = []'''
            
b=[]
for i in sameday_buynum.values():
    b.extend(i)           
bgm = sum(b)/len(b)  #  1.2523654960438746
denominator = bgm*1
         
Matching_degree = {}

w1=0.5
w2=1-w1

start = time.clock()

text = ''
for i in range(0,6500):
    rule1_items = sameday[test[i]]
    rule1_nums = sameday_buynum[test[i]]
    tfidf_items = top800xx[test[i]]
    tfidf_nums = similar[test[i]]
    
    intersection = m_intersection(rule1_items,tfidf_items)
    
    matching_degree = []
    for j in range(len(rule1_items)):
        if rule1_items[j] not in intersection:
            matching_degree.append((rule1_items[j],w1*rule1_nums[j]/denominator))
    #Matching_degree[test[i]] = matching_degree
    
    for j in range(len(tfidf_items)):
        if tfidf_items[j] not in intersection:
            matching_degree.append((tfidf_items[j],(1-tfidf_nums[j]/2)*w2)) #将标准化的欧式距离转化为cosine余弦相似度
    for k in intersection:
        i1 = rule1_items.index(k)
        i2 = tfidf_items.index(k)
        matching_degree.append((k,(1-tfidf_nums[i2]/2)*w2 + w1*rule1_nums[i1]/denominator))
        
    matching_degree = sorted(matching_degree, key = lambda s: s[1], reverse=True)    
    
    text += test[i] + ' '
    for item in matching_degree[0:200]:
        text += item[0] + ','
    text = text[:-1] + '\n'
    
with open(current_path + '/my_answer.csv', "w") as f:
    f.write(text)
    
elapsed = (time.clock() - start)
print("Time used:",elapsed)



