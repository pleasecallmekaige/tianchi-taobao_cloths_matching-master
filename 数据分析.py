# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 21:33:02 2017

@author: pleasecallmekaige
"""
import os

import numpy as np

current_patch = os.path.abspath('.')

def kNN_Sparse(local_data_csr, query_data_csr, top_k):
    # calculate the square sum of each vector
    local_data_sq = local_data_csr.multiply(local_data_csr).sum(1)  # 每行有多少个位置不为零
    #matrix([[5],
    #        [6],
    #        [2]], dtype=int64)
    query_data_sq = query_data_csr.multiply(query_data_csr).sum(1)  #

    # calculate the dot
    distance = query_data_csr.dot(local_data_csr.transpose()).todense()  # dot计算点积  transpose稀疏矩阵转置

    # calculate the distance 
    num_query, num_local = distance.shape 
    distance = np.tile(query_data_sq, (1, num_local)) + np.tile(local_data_sq.T, (num_query, 1)) - 2 * distance

    # get the top k
    topK_idx = np.argsort(distance)[:, 0:top_k]
    topK_similarity = np.zeros((num_query, top_k), np.float32)
    for i in range(num_query):
        topK_similarity[i] = distance[i, topK_idx[i]]
    return topK_similarity,topK_idx

def m_intersection(a,b):
    """
    取交集
    """
    return list(set(a).intersection(set(b)))


def get_answer():
    with open(current_patch + "/answer.csv", "r") as f:
        answer_list = [] #dim_fashion_matchsets中的所有商品
        for line in f: #.readlines()[0:5]:
            arr = line.replace("\n","").split(" ")  
            pairs = arr[1].split(",") 
            answer_list.extend(pairs)
    return answer_list

def get_train_itemlist():
    with open(current_patch + "/训练套餐.csv", "r") as f:
        #获取dim_fashion_matchsets中的所有商品
        all_itemsinfashionmatchsets_list = [] #dim_fashion_matchsets中的所有商品
        Package2item_match_dict = {}  # 套餐对应商品搭配的字典
        #Package2Category_match_dict = {}  # 套餐对应类目搭配的字典
        for line in f: #.readlines()[0:5]:
            arr = line.replace("\n","").split(" ")  # arr[0]:商品套餐ID   arr[1]：套餐内的商品
            pairs = arr[1].split(";") #
            tmp_list = []
            for pair in pairs:
                item = pair.split(",")
                all_itemsinfashionmatchsets_list.extend(item)
                tmp_list.extend(item)
            Package2item_match_dict[arr[0]] = tmp_list
        all_itemsinfashionmatchsets_list = list(set(all_itemsinfashionmatchsets_list))
    return all_itemsinfashionmatchsets_list,Package2item_match_dict

answwer = get_answer()

train_itemlist,b = get_train_itemlist()

answwer = list(set(answwer))
train_itemlist = list(set(train_itemlist))

ins = m_intersection(list(set(answwer)),list(set(train_itemlist)))

print('answwer:',len(answwer))

print('train_itemlist:',len(train_itemlist))

print('ins:',len(ins))



