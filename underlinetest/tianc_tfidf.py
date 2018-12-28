# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 21:07:18 2017

@author: pleasecallmekaige
"""
#已获取搭配列表中与测试商品最相似的商品
#TODO 根据该商品匹配到搭配列表中的搭配类目对，获取与之搭配的商品和对应类目，并根据这些信息计算与之较为相近的商品
import os
import time


import numpy as np

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer


#current_path = os.path.abspath('.')  #当前文件夹路径H:\tianchi\underline\underlinetest

def m_intersection(a,b):
    """
    取交集
    """
    return list(set(a).intersection(set(b)))


def tfidf(corpus):
    """
    获取语料库中每一个句子的tf-idf值
    :param corpus: 语料库 
    """
    vectorizer = CountVectorizer()
    x = vectorizer.fit_transform(corpus)
    #a = x.toarray()
    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(x)
    return tfidf


def euclidean_metric(vector1,vector2):
    """
    计算欧式距离
    :param vector1:向量1
    :param vector2: 向量2
    """
    '''sqDiffVector = vector1 - vector2
    sqDiffVector = sqDiffVector ** 2
    sqDistance = sqDiffVector.sum()
    distance = sqDistance ** 0.5
    return distance'''
    return np.linalg.norm(vector1 - vector2)  

def European_sparse_matrix(csr_matrix1,csr_matrix2):
    """
    计算稀疏矩阵的欧式距离
    :param csr_matrix1:单行稀疏矩阵1
    :param csr_matrix2: 单行稀疏矩阵2
    """ 
    local = np.unique(np.concatenate((csr_matrix1.indices,csr_matrix2.indices)))
    vector1 = csr_matrix1[:,local].toarray()
    vector2 = csr_matrix2[:,local].toarray()
    return euclidean_metric(vector1,vector2)
    

def testitems(): 
    '''读取测试商品'''
    with open('H:/tianchi/underline/underlinetest_set.csv', "r") as f:
        test_items = []
        for line in f:
            arr = line.replace("\n","").split(" ")
            test_items.append((arr[0]))
    return test_items


def classification():
    """
    获取每个item的类目
    """
    f = open("H:/tianchi/underline/data/dim_items.txt", "r")
    label = {}
    for line in f:
        arr = line.replace("\n","").split(" ")
        label[arr[0]] = arr[1]
    return label


def infomation():
    """
    获取每一个item的标题
    :return:
    """
    f = open("H:/tianchi/underline/data/dim_items.txt", "r")
    info = {}
    for line in f:
        arr = line.replace("\n","").split(" ")
        info[arr[0]] = arr[2]
    return info

def get_allitem():
    """
    获取每一个item
    :return:
    """
    f = open("H:/tianchi/underline/data/dim_items.txt", "r")
    items = []
    for line in f:
        arr = line.replace("\n","").split(" ")
        items.append(arr[0])
    return items 



if __name__ == "__main__":
    test_items = testitems()
    all_items = get_allitem()
    
    
    
    
    
    
    
    
    
    
