# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 21:41:02 2017

@author: lenovo
"""


def read_file(path):
    with open(path, "r") as f:
        f_dict = {}
        for line in f:
            arr = line.replace("\n","").split(" ")
            f_dict[arr[0]] = arr[1].split(",")
            
 