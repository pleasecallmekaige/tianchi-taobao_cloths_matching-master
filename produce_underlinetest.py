# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 15:16:32 2017

@author: lenovo
"""
import os
import random

current_patch = os.path.abspath('.')

def m_intersection(a,b):
    """
    取交集
    """
    return list(set(a).intersection(set(b)))


def get_two_listanddict():
    with open(current_patch + "/data/dim_fashion_matchsets.txt", "r") as f:
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



def get_three_list(all_itemsinfashionmatchsets_list,Package2item_match_dict):
    random_num = random.sample(range(len(all_itemsinfashionmatchsets_list)), 6500)  #共60000个
    underline_testset = [] #线下测试商品集
    for i in random_num:
        underline_testset.append(all_itemsinfashionmatchsets_list[i])
    #underline_testset 线下测试商品集   
    underline_answer_Package = [] #测试套餐，用于生成测试集答案
    underline_train_Package = [] #剔除测试套餐后的训练套餐
    for p,s in Package2item_match_dict.items():
        intersection = m_intersection(s,underline_testset)
        if len(intersection) != 0:
            underline_answer_Package.append(p)
        else:
            underline_train_Package.append(p)
    return underline_testset,underline_answer_Package,underline_train_Package



#---------------------------start------------------------------------------------

all_itemsinfashionmatchsets_list,Package2item_match_dict = get_two_listanddict()
#all_itemsinfashionmatchsets_list #dim_fashion_matchsets中的所有商品列表
#Package2item_match_dict # 套餐对应商品搭配的字典
underline_testset,underline_answer_Package,underline_train_Package = get_three_list(all_itemsinfashionmatchsets_list,Package2item_match_dict)
#underline_testset #线下测试商品集
#underline_answer_Package  #测试套餐id，用于生成测试集答案
#underline_train_Package #剔除测试套餐后的训练套餐id
with open(current_patch + "/data/dim_fashion_matchsets.txt", "r") as f:
    underline_answerset_text = '' #要写入的线下用于生成答案的套餐 str
    underline_trainset_text = ''  #要写入的线下用于训练的套餐 str
    for line in f:
        arr = line.replace("\n","").split(" ")
        if arr[0] in underline_answer_Package:
            underline_answerset_text += line
        else:
            underline_trainset_text += line
   
#underline_answerset_text #要写入的线下用于生成答案的套餐 str
#underline_trainset_text #要写入的线下用于训练的套餐 str

with open(current_patch + "/测试套餐（用于生成线下测试对应的答案）.csv", "w") as f:
    f.write(underline_answerset_text)

with open(current_patch + "/训练套餐.csv", "w") as f:
    f.write(underline_trainset_text)  
    
with open(current_patch + "/underlinetest_set.csv", "w") as f:
    text = ''
    for i in range(len(underline_testset)):
        text += underline_testset[i] + '\n'
    f.write(text)
    
#------------------------------生成线下测试答案---------------------------------
with open(current_patch + "/测试套餐（用于生成线下测试对应的答案）.csv", "r") as f:
    test_Package2item_match_dict = {} #线下用于生成答案测试套餐的字典
    query_dict = {} #
    for line in f:
        arr = line.replace("\n","").split(" ")
        pairs = arr[1].split(";")
        tmp_list = []
        tmp_list1 = []
        for pair in pairs:
            item = pair.split(",")
            tmp_list.append(item)
            tmp_list1.extend(item)  
        test_Package2item_match_dict[arr[0]] = tmp_list
        query_dict[arr[0]] = tmp_list1 
                  
#test_Package2item_match_dict #线下用于生成答案测试套餐的字典 
answer_text = '' 
for item in underline_testset:
    answer_text += item + ' '
    for p,s in query_dict.items():
        if item in s:
            answer = test_Package2item_match_dict[p]
            for i in range(len(answer)):
                if item not in answer[i]:
                    for j in range(len(answer[i])):
                        answer_text += answer[i][j] + ','
    answer_text = answer_text[:-1] + '\n'

with open(current_patch + "/answer.csv", "w") as f:
    f.write(answer_text)
    
    
    
    
    