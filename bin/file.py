
'''
    Author: Juntaran
    Email:  Jacinthmail@gmail.com
    Date:   2017/7/27 13:56
'''
# !/usr/bin/env python3
# coding=utf-8

import os, sys

def getListFiles(path):
    ret = []
    for root, dirs, files in os.walk(path):
        for filespath in files:
            ret.append(os.path.join(root,filespath))
    return ret

def ListFile():
    filename = []
    ret = getListFiles("conf")
    for each in ret:
        if 'test' in each:
            continue
        filename.append(each)
    return filename