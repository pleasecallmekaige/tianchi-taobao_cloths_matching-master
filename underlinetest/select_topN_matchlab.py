# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 22:07:24 2017

@author: pleasecallmekaige
"""
import tianc_tfidf as tff
import time
import os

current_path = os.path.abspath('.')


def get_top800_dict():
    '''
    获取每一个test_item最相似的800个商品
    :return:
    '''
    with open(current_path + '/top800x.csv', "r") as f:
        test_item2simlar = {}
        for line in f:
            arr = line.replace("\n","").split(" ")
            match_items_list = arr[1].split(",")
            test_item2simlar[arr[0]] = match_items_list
    return test_item2simlar
 
    
def get_test_items2matchlabels_dict():
    with open(current_path + '/test_items2matchlabels.csv', "r") as f:
        test_items2matchlabels_dict = {}
        for line in f:
            arr = line.replace("\n","").split(" ")
            match_items_list = arr[1].split(",")
            test_items2matchlabels_dict[arr[0]] = match_items_list
    return test_items2matchlabels_dict

def App_app(start,end,test_item2simlar,test_items2matchlabels_dict,test_items):
    text = ''
    for i in range(start,end):
        match_items_list = test_item2simlar[test_items[i]] 
        match_labels_list = test_items2matchlabels_dict[test_items[i]]
        last_match_list = []
        for item in match_items_list:
            if item2labels_dict[item] in match_labels_list:
                last_match_list.append(item)
        
        num = len(last_match_list)
        if num >200:
            num=200
        last_match_list = last_match_list[0:num]
        
        
        text = text + test_items[i] + ' '
        for j in range(len(last_match_list)):
            text = text + last_match_list[j] + ','
        text = text[:-1] + '\n'
    return text



if __name__ == '__main__':
    test_items = tff.testitems()  # 获取测试商品
    test_items2matchlabels_dict = get_test_items2matchlabels_dict()
    test_item2simlar = get_top800_dict()
    
    item2labels_dict = tff.classification()  # 获取每个item的类目
    
    len_test = len(test_items) #测试商品的个数
                                         
    start = time.clock()
    with open(current_path + '/fm_submissions.csv', "w") as f:
        f.write('')
    sss = 0
    go = 1
    while go:
        eee=sss+100
        if eee>len_test:
            go = 0
            eee=len_test
        text = App_app(sss,eee,test_item2simlar,test_items2matchlabels_dict,test_items)
        with open(current_path + '/fm_submissions.csv', "a") as f:
            f.write(text)
        sss+=100
    
    elapsed = (time.clock() - start)
    print("Time used:",elapsed)
