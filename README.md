# Firewall Rule Assist

对 yaml 格式的防火墙配置文件进行解析  
可以快速通过以下命令查找 集群/IP 之间关系  

Usage:
    -s: search ip in conf, conf can set *
    -c: cluster conn ip
    -t: test ip1 conn ip2
Example:
    python bin\main.py -s 10.10.10.10 10.10.10.20 conf\test\test.conf
    python bin\main.py -c from|to FAL_SERVER DB_MONITER conf\test\test.conf
    python bin\main.py -t 1|2|3|4 src to dst conf\test\test.conf