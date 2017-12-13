# Firewall Rule Assist

对 yaml 格式的防火墙配置文件进行解析  
可以快速通过以下命令查找 集群/IP/服务 之间关系  

## Requirement:

- python3  Windows or Linux
- yaml  pip3 install yaml

```
Usage:
    -s ip: search ip in conf, conf can set all
    -s cluster: search cluster in conf, conf can set all
    -c -i: cluster ip
    -c -a: cluster application
    -t: test ip1 conn ip2
    -a: show application info

Example:
    python bin\main.py -s ip 10.10.10.10 10.10.10.20 conf\test\test.conf
    python bin\main.py -s cluster cluster1 cluster2 conf\test\test.conf
    python bin\main.py -c -a from|to FAL_SERVER DB_MONITER conf\test\test.conf
    python bin\main.py -c -i from|to FAL_SERVER DB_MONITER conf\test\test.conf
    python bin\main.py -t 1|2|3|4 src to dst conf\test\test.conf
    python bin\main.py -a APPLICAITON conf\test\test.conf
```
