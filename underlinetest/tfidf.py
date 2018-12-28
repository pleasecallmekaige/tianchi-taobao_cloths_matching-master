# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 21:06:36 2017

@author: pleasecallmekaige
"""
import profile
import os

import tianc_tfidf as tff
import time
import numpy as np

current_path = os.path.abspath('.')


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
    

def App_mostsimlaritemof_testitems(start,end,test_items,allitems2list_dict,allitems_itidf_matrix,all_items):
    test = test_items[start:end]
    index = []
    for i in range(len(test)):
        index.append(allitems2list_dict[test[i]]) 
    query_item_matrix = allitems_itidf_matrix[index]
    top_k = np.array(10000, dtype=np.int32)
    topK_similarity, topK_idx  = kNN_Sparse(allitems_itidf_matrix, query_item_matrix, top_k)
    topK_idx = topK_idx.A
    match = ''
    similar = ''
    for i in range(len(test)):
        match = match + test[i] + ' '
        similar = similar + test[i] + ' '
        number = 0
        for j in range(1,len(topK_idx[i])):
            if item2labels_dict[all_items[topK_idx[i][j]]] != item2labels_dict[test[i]]:
                match = match + all_items[topK_idx[i][j]] + ','
                similar = similar + str(topK_similarity[i][j]**0.5) + ','
                number += 1
            if number == 800: #取前800个不是同类的商品
                break
        match = match[:-1] + '\n'
        similar = similar[:-1] + '\n'
    with open(current_path + '/tfidf_data/top800xx.csv', "a") as f:
        f.write(match)
    with open(current_path + '/tfidf_data/similar.csv', "a") as f:
        f.write(similar)
    
if __name__=='__main__':    
    print('start....')
    test_items = tff.testitems()  # 待测试商品列表 
    item2labels_dict = tff.classification()  # 获取每个item的类目
    item2infos_dict = tff.infomation()  # 获取每一个item的标题
    
    all_items = tff.get_allitem() # 所有的商品
    
    allitems2list_dict = {} 
    for i in range(len(all_items)):
        allitems2list_dict[all_items[i]]=i
    
    corpus = []  #词袋
    for i in all_items:
        corpus.append(item2infos_dict[i])
    
    allitems_itidf_matrix = tff.tfidf(corpus)  # 商品全集建立的词频统计稀疏矩阵
    
    len_test = len(test_items) #测试商品的个数
    
    start = time.clock()
    with open(current_path + '/tfidf_data/top800xx.csv', "w") as f:
        f.write('')
    with open(current_path + '/tfidf_data/similar.csv', "w") as f:
        f.write('')
        
    sss = 0
    go = 1
    while go:
        eee=sss+50
        if eee>len_test: 
            go = 0
            eee=len_test 
        App_mostsimlaritemof_testitems(sss,eee,test_items,allitems2list_dict,allitems_itidf_matrix,all_items)
        sss+=50
        print(sss)

    elapsed = (time.clock() - start)
    print("Time used:",elapsed)
