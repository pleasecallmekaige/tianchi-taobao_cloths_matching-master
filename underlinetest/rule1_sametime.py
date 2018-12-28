# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 19:32:28 2017

@author: pleasecallmekaige
"""
import os
from collections import Counter
import time
import profile

import pandas as pd

import tianc_tfidf as tff

current_path = os.path.abspath('.')

'''class MagicDict(dict):
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value'''

def get_sameday(user_bought_history,test_item):
    buyer_List = (user_bought_history.user_id[user_bought_history.item_id == test_item].values)
    buyer_date = (user_bought_history.create_at[user_bought_history.item_id == test_item].values) 
    buy = list(set(zip(buyer_List,buyer_date)))
    item_list = []
    for i in range(len(buyer_List)):
        sameitem = user_bought_history.item_id[(user_bought_history.user_id == buy[i][0]) & (user_bought_history.create_at == buy[i][1])].values
        sameitem = list(set(sameitem))
        if len(sameitem)>1:
            sameitem.remove(test_item)
            item_list.extend(sameitem)
    return  item_list

def get_text(test_items,i,user_bought_history,item2labels_dict,test2matchlab_dict):
    item_list = get_sameday(user_bought_history,test_items[i])
    count = Counter(item_list)
    out_items  = sorted(count.items(), key = lambda s: s[1], reverse=True)
    text1 = ''
    text2 = ''
    text1 += str(test_items[i]) + ' '
    text2 += str(test_items[i]) + ' '
    matchlab = test2matchlab_dict[test_items[i]]
    for item in out_items:
        if item2labels_dict[str(item[0])] in matchlab: #看类目是否搭配
            text1 += str(item[0]) + ','
            text2 += str(item[1]) + ','
    text1 = text1[:-1] + '\n'
    text2 = text2[:-1] + '\n'
    return text1,text2


        

def main():
    user_bought_history = pd.read_table(current_path + '/../data/user_bought_history.txt',sep = '\s+' , names = ['user_id','item_id','create_at']) 
    test_items = pd.read_table(current_path + '/../underlinetest_set.csv', names = ['test_items_id'])
    
    
    test_items = list(test_items['test_items_id'])
    
    item2labels_dict = tff.classification()  # 获取每个item的类目
    
    with open(current_path + '/test_items2matchlabels.csv', "r") as f:
        test2matchlab_dict = {}
        for line in f:
            arr = line.replace("\n","").split(" ")
            test2matchlab_dict[int(arr[0])] = arr[1].split(",")
        
    text1 = ''
    text2 = ''
    '''with open(current_patch + '/rule1_data/同一天被同一用户购买的商品.csv', "w") as f:
        f.write(text1)
    with open(current_patch + '/rule1_data/共同购买数.csv', "w") as f:
        f.write(text2)'''
        
    start = time.clock()
    for i in range(4000,6500): #len(test_items)
        t1,t2 = get_text(test_items,i,user_bought_history,item2labels_dict,test2matchlab_dict)
        text1 += t1
        text2 += t2
        if (i%50)==0:
            print(i)
    with open(current_path + '/rule1_data/同一天被同一用户购买的商品.csv', "a") as f:
        f.write(text1)
    with open(current_path + '/rule1_data/共同购买数.csv', "a") as f:
        f.write(text2)        
    elapsed = (time.clock() - start)
    print("Time used:",elapsed)


if __name__ == '__main__':
    #profile.run("main()")
    main()

