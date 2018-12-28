# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 21:41:02 2017

@author: lenovo
"""
import os
import numpy as np
import tianc_tfidf as tff

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

def similarity_measure(item1,item2,allitems2list_dict,allitems_itidf_matrix):
    index = []
    index.append(allitems2list_dict[item1]) 
    index.append(allitems2list_dict[item2]) 
    local_item_matrix = allitems_itidf_matrix[index]
    query_item_matrix = allitems_itidf_matrix[index[1]]
    top_k = np.array(2, dtype=np.int32)
    topK_similarity, topK_idx  = kNN_Sparse(local_item_matrix, query_item_matrix, top_k)
    topK_idx = topK_idx.A
    return topK_similarity[0][1]**0.5

with open(current_path + '/../../answer.csv', "r") as f:
    answer_dict = {}
    for line in f:
        arr = line.replace('\n','').split(' ')
        answer_dict[arr[0]] = arr[1].split(',')
        
with open(current_path + '/test_items2matchlabels.csv', "r") as f:
    test2cat_dict = {}
    for line in f:
        arr = line.replace('\n','').split(' ')
        test2cat_dict[arr[0]] = arr[1].split(',')

'''test = tff.testitems()
item2labels_dict = tff.classification()  # 获取每个item的类目
all_items = tff.get_allitem() # 所有的商品
item2infos_dict = tff.infomation()  # 获取每一个item的标题

allitems2list_dict = {} 
for i in range(len(all_items)):
    allitems2list_dict[all_items[i]]=i    
                      
corpus = []  #词袋
for i in all_items:
    corpus.append(item2infos_dict[i])

allitems_itidf_matrix = tff.tfidf(corpus)  # 商品全集建立的词频统计稀疏矩阵'''

'''c=0
d=0
b=0
for i in range(len(test)):
    answer_list = answer_dict[test[i]] #每个测试商品的答案
    cat_list= test2cat_dict[test[i]] #每个测试商品的类目对
    a = 0
    for answer in answer_list:
        try:
            a += cat_list.index(item2labels_dict[answer]) #答案对应的类目
            d += 1
        except ValueError:
            c+=1
            a += 0
            
    b += a/len(answer_list)
print(b/len(test))   
print(c) 
print(d)'''

b=0
for i in range(len(test)):#len(test)
    answer_list = answer_dict[test[i]] #每个测试商品的答案
    cat_list= test2cat_dict[test[i]] #每个测试商品的类目对
    a = 0
    for answer in answer_list:
        a += similarity_measure(test[i],answer,allitems2list_dict,allitems_itidf_matrix)
    b += a/len(answer_list) 
    print(i)
b=b/len(test)      
print(b)       
    
