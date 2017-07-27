'''
    Author: Juntaran
    Email:  Jacinthmail@gmail.com
    Date:   2017/7/25 14:02
'''
# !/usr/bin/env python3
# coding=utf-8

def get_cidr(ip):
    # 把ip处理，返回 ip  /8  /16  /24 的格式
    ipdic = ip.split(".")
    cidr1 = ipdic[0] + '.0.0.0/8'
    cidr2 = ipdic[0] + '.' + ipdic[1] + '.0.0/16'
    cidr3 = ipdic[0] + '.' + ipdic[1] + '.' + ipdic[2] + '.0/24'
    cidr_dict = [ip, cidr1, cidr2, cidr3]
    # print(cidr_dict)
    return cidr_dict

# get_cidr('192.168.1.1')