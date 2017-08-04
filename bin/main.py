'''
    Author: Juntaran
    Email:  Jacinthmail@gmail.com
    Date:   2017/7/25 13:45
'''
# !/usr/bin/env python3
# coding=utf-8

import sys
import yaml

from get_cidr import *
from get_keys import *
from file import *



############################################################################
'''
    searchIP() 输入IP和配置文件，查找该 IP 所在集群
    searchCluster() 输入集群和配置文件，查找该集群IP
'''

def searchCluster(cluster, file):

    with open(file) as cf:
        data = yaml.load(cf)

    for key in data['ZONE']:
        for i in data['ZONE'][key]:
            if i == cluster:
                print('    ' + key + ':')
                print('      ', i + ':')
                print('        ', data['ZONE'][key][i])

def searchIP(ip, file):

    with open(file) as cf:
        data = yaml.load(cf)
        ip_cidr = get_cidr(ip)
        # print(ip_cidr)
    for i in range(len(ip_cidr)):
        global route
        route = ['ZONE']
        data_range_ip(ip_cidr[i], data['ZONE'])
    # print(route)

def data_range_ip(ip, data):

    if len(route) == 0:
        return

    if isinstance(data, dict):  # 使用isinstance检测数据类型，如果是dict类型
        for key in data:
            value = data[key]
            # print("%s : %s" % (key, value))
            if data[key] != None:
                route.append(key)
            data_range_ip(ip, value)
        route.pop()

    if isinstance(data, list):  # 如果是list类型
        check = 0
        for i in range(len(data)):
            if (data[i] == ip):
                # print("get!")
                # print("data_list:", data)
                check = 1
                route.append(data)
                print('    ', route)
                # 弹出刚写入的数据
                route.pop()
                route.pop()
                return
        if check == 0:
            route.pop()

############################################################################







############################################################################
'''
    getClusterIp() 输入集群，输出对应的IP
    getIpCluster() 输入IP，返回所在集群
'''

def getClusterIp(cluster, zone):
    ret = []
    for key in zone:
        for key2 in zone[key]:
            if key2 == cluster:
                print('        ', zone[key][key2])
                ret.append(zone[key][key2])
    # print('getClusterIP RET: ', ret)
    return ret

# 获取ip所在的集群
def getIpCluster(ip, file):
    ip_cidr = get_cidr(ip)
    cluster_ret = []
    for i in ip_cidr:
        for key1 in file:
            for key2 in file[key1]:
                if i in file[key1][key2]:
                    cluster_ret.append(key2)
    return cluster_ret

############################################################################



############################################################################
'''
    clusterConn1() 输入集群和配置文件，查找该集群能访问的IP
    clusterConn2() 输入集群和配置文件，查找能访问该集群的IP
'''

def  clusterConn1(cluster, file):
    if cluster == None:
        return []
    with open(file) as cf:
        data = yaml.load(cf)
        return data_range_cluster(cluster, data['RULE'], data['ZONE'], 0)

def clusterConn2(cluster, file):
    if cluster == None:
        return []
    with open(file) as cf:
        data = yaml.load(cf)
        return data_range_cluster(cluster, data['RULE'], data['ZONE'], 1)

def data_range_cluster(cluster, data, zone, judge):
    ret = []
    if isinstance(data, list):  # 如果是list类型
        if judge == 0:
            print(cluster, ' can connect these:')
            for i in range(len(data)):
                for key in data[i]:
                    for o in range(len(data[i][key]['from'])):
                        if data[i][key]['from'][o] == '@' + cluster:
                            for j in range(len(data[i][key]['to'])):
                                print('    ' + data[i][key]['to'][j].strip('@'))
                                ret.append(data[i][key]['to'][j].strip('@'))
                                ret.append(getClusterIp(data[i][key]['to'][j].strip('@'), zone))
        elif judge == 1:
            print(cluster, ' can connected by these:')
            for i in range(len(data)):
                for key in data[i]:
                    for o in range(len(data[i][key]['tp'])):
                        if data[i][key]['to'][o] == '@' + cluster:
                            for j in range(len(data[i][key]['from'])):
                                print('    ' + data[i][key]['from'][j].strip('@'))
                                ret.append(data[i][key]['from'][j].strip('@'))
                                ret.append(getClusterIp(data[i][key]['from'][j].strip('@'), zone))

    # print('data_range_cluster ret: ', ret)
    return ret

############################################################################







############################################################################
'''
    ClusterToCluster()
    ClusterToIp()
    IpToIp()
    IpToCluster()
'''

# 判断集群访问集群
def ClusterToCluster(clusterFrom, clusterTo, file):

    if clusterFrom == clusterTo:
        return True

    with open(file) as cf:
        data = yaml.load(cf)

    print('From', clusterFrom, 'To', clusterTo, ':')
    print('    ', clusterFrom, ':')
    getClusterIp(clusterFrom, data['ZONE'])
    print('    ', clusterTo, ':')
    getClusterIp(clusterTo, data['ZONE'])

    target = clusterConn1(clusterFrom, file)
    for i in range(len(target)):
        if i % 2 == 0 and target[i] == clusterTo:
            print('True')
            return True

    print('False')
    return False


# 判断集群访问IP
def ClusterToIp(clusterFrom, ipTo, file):

    with open(file) as cf:
        data = yaml.load(cf)

    print('From', clusterFrom, 'To', ipTo, ':')
    print('    ', clusterFrom, ':')
    ipFrom = getClusterIp(clusterFrom, data['ZONE'])

    # 判断目的ip是否在源集群中
    for i in range(len(ipFrom[0])):
        if ipFrom[0][i] == ipTo:
            print("dstIp in srcCluster, True")
            return True

    # 获取目的ip所在的集群
    clusterTo = getIpCluster(ipTo, data['ZONE'])
    print(clusterTo)

    check = False
    for i in clusterTo:
        if ClusterToCluster(clusterFrom, i, file) == True:
            check = True

    print(check)
    return check


# 判断IP访问集群
def IpToCluster(ipFrom, clusterTo, file):

    with open(file) as cf:
        data = yaml.load(cf)

    print('From', ipFrom, 'To', clusterTo, ':')
    print('    ', clusterTo, ':')
    ipTo = getClusterIp(clusterTo, data['ZONE'])

    # 判断源ip是否在目的集群中
    for i in range(len(ipTo[0])):
        if ipTo[0][i] == ipFrom:
            print("srcIp in dstCluster, True")
            return True

    # 获取源ip所在的集群
    clusterFrom = getIpCluster(ipFrom, data['ZONE'])
    print(clusterFrom)

    check = False
    for i in clusterFrom:
        if ClusterToCluster(i, clusterTo, file) == True:
            check = True

    print(check)
    return check


# 判断IP访问IP
def IpToIp(ipFrom, ipTo, file):

    with open(file) as cf:
        data = yaml.load(cf)

    print('From', ipFrom, 'To', ipTo, ':')

    # 获取源ip所在的集群
    clusterFrom = getIpCluster(ipFrom, data['ZONE'])
    print(clusterFrom)

    # 获取目的ip所在的集群
    clusterTo = getIpCluster(ipTo, data['ZONE'])
    print(clusterTo)

    check = False
    for i in clusterFrom:
        for j in clusterTo:
            if ClusterToCluster(i, j, file) == True:
                check = True

    print(check)
    return check

############################################################################



############################################################################
'''
    getAppInfo() 根据服务查看它的信息，包括集群访问关系、协议、src&dst port
'''

def getAppInfo(APP, file):

    with open(file) as cf:
        data = yaml.load(cf)

    judge = 0

    for i in data['RULE']:
        for key in i:
            for j in i[key]['applications']:
                if j == APP:
                    print('APP :', j)
                    print('    From:', i[key]['from'])
                    print('    To  :', i[key]['to'])
                    if data['APPLICATION'][APP] != None :
                        print('    protocol:', data['APPLICATION'][APP]['protocol'])
                        print('    src-port:', data['APPLICATION'][APP]['source-port'])
                        print('    dst-port:', data['APPLICATION'][APP]['destination-port'])
                    judge = 1
    if judge == 0:
        print('Error: APPLICATION not search!')

############################################################################



############################################################################
'''
    getClusterApp() 根据集群查看它对应的服务，并列出服务的信息
'''

def getClusterAppInfo(APP, data):
    print(APP + ':')
    judge = 0
    for i in data['RULE']:
        for key in i:
            for j in i[key]['applications']:
                if j == APP:
                    print('    APP :', j)
                    print('      From:', i[key]['from'])
                    print('      To  :', i[key]['to'])
                    if data['APPLICATION'][APP] != None :
                        print('      protocol:', data['APPLICATION'][APP]['protocol'])
                        print('      src-port:', data['APPLICATION'][APP]['source-port'])
                        print('      dst-port:', data['APPLICATION'][APP]['destination-port'])
                    judge = 1
    if judge == 0:
        print('Error: APPLICATION not search!')



def getClusterApp(cluster, file, direct):

    ret = []
    print(cluster, ":")
    with open(file) as cf:
        data = yaml.load(cf)

    for i in data['RULE']:
        for key in i:
            for j in i[key][direct]:
                if j == '@' + cluster:
                    for v in i[key]['applications']:
                        ret.append(v)
    ret = list(set(ret))
    print('  ', ret)
    for value in ret:
        getClusterAppInfo(value, data)


############################################################################










############################################################################
'''
    errorExample() 当参数错误时的提示
'''
def errorExample():
    print("Usage:\n    "
          "-s ip: search ip in conf, conf can set all\n    "
          "-s cluster: search cluster in conf, conf can set all\n    "
          "-c -i: cluster ip\n    "
          "-c -a: cluster application\n    "
          "-t: test ip1 conn ip2\n    "
          "-a: show application info\n")
    print("Example:\n"
          "    python bin\main.py -s ip IP1 IP2 IP3... conf\\test\\test.yaml\n"
          "    python bin\main.py -s cluster CLUSTER1 CLUSTER2... conf\\test\\test.yaml\n"
          "    python bin\main.py -c -i from|to CLUSTER1 CLUSTER2... conf\\test\\test.yaml\n"
          "    python bin\main.py -c -a from|to CLUSTER1 CLUSTER2... conf\\test\\test.yaml\n"
          "    python bin\main.py -t 1|2|3|4 SRC_IP/CLUSTER to DST_IP/CLUSTER conf\\test\\test.yaml\n"
          "    python bin\main.py -a APPLICAITON conf\\test\\test.yaml\n")
    return

############################################################################





if __name__ == '__main__':
    
    if len(sys.argv) < 3:
        if len(sys.argv) > 1 and sys.argv[1] == '-t':
            print("Choose:\n cluster to cluster | cluster to ip | ip to cluster | ip to ip")
            print("1        2        3        4, then enter the src to dst and conf")
            quit()
        errorExample()
        quit()

    if (sys.argv[1] != '-s' and sys.argv[1] != '-c' and sys.argv[1] != '-t' and sys.argv[1] != '-a'):
        errorExample()
        quit()

    elif sys.argv[1] == '-s' and sys.argv[2] == 'ip':
        if len(sys.argv) < 5:
            print("Enter ip and conf")
            quit()
        for i in range(3, len(sys.argv)-1):
            print('\n', sys.argv[i])
            if sys.argv[len(sys.argv) - 1] == 'all':
                filename = ListFile()
                for j in filename:
                    print('  file: ', j)
                    searchIP(sys.argv[i], j)
            else:
                searchIP(sys.argv[i], sys.argv[len(sys.argv)-1])
        quit()

    elif sys.argv[1] == '-s' and sys.argv[2] == 'cluster':
        if len(sys.argv) < 5:
            print("Enter cluster and conf")
            quit()
        for i in range(3, len(sys.argv)-1):
            print('\n', sys.argv[i])
            if sys.argv[len(sys.argv) - 1] == 'all':
                filename = ListFile()
                for j in filename:
                    print('  file: ', j)
                    searchCluster(sys.argv[i], j)
            else:
                searchCluster(sys.argv[i], sys.argv[len(sys.argv)-1])
        quit()

    elif sys.argv[1] == '-c' and sys.argv[2] == '-i':
        if len(sys.argv) < 6:
            print("Enter direct, cluster and conf")
            quit()
        if sys.argv[3] == 'from':
            for i in range(4, len(sys.argv)-1):
                clusterConn1(sys.argv[i], sys.argv[len(sys.argv)-1])
            quit()
        if sys.argv[3] == 'to':
            for i in range(4, len(sys.argv)-1):
                clusterConn2(sys.argv[i], sys.argv[len(sys.argv)-1])
        quit()

    elif sys.argv[1] == '-c' and sys.argv[2] == '-a':
        if len(sys.argv) < 6:
            print("Enter direct cluster and conf")
            quit()
        for i in range(4, len(sys.argv) - 1):
            getClusterApp(sys.argv[i], sys.argv[len(sys.argv) - 1], sys.argv[3])
        quit()

    elif sys.argv[1] == '-t':
        # 四种情况： cluster to cluster / cluster to ip / ip to cluster / ip to ip
        if len(sys.argv) != 7:
            print("Choose cluster to cluster | cluster to ip | ip to cluster | ip to ip")
            print("1    2    3    4, then enter the src to dst and conf")
            quit()
        if sys.argv[2] == '1':
            ClusterToCluster(sys.argv[3], sys.argv[5], sys.argv[len(sys.argv)-1])
        if sys.argv[2] == '2':
            ClusterToIp(sys.argv[3], sys.argv[5], sys.argv[len(sys.argv) - 1])
        if sys.argv[2] == '3':
            IpToCluster(sys.argv[3], sys.argv[5], sys.argv[len(sys.argv) - 1])
        if sys.argv[2] == '4':
            IpToIp(sys.argv[3], sys.argv[5], sys.argv[len(sys.argv) - 1])

    elif sys.argv[1] == '-a':
        if len(sys.argv) != 4:
            errorExample()
            quit()
        getAppInfo(sys.argv[2], sys.argv[3])

    else:
        errorExample()