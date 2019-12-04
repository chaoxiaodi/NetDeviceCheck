#!/usr/bin/env python
from netmiko import Netmiko
from getpass import getpass
from netmiko import ConnectHandler
import os
import time
import deviceInfo
import cmdInfo

#定义时间作为配置文件输出信息
nowday=time.strftime("%Y-%m-%d-%H%M%S")
#定义文件输出目录
resultDir = os.path.abspath('.') + '\outputFile\\'
#文件操作函数，把对设备的操作输出到文件逻辑实现
def fileopt(fname,cmdresult = ""):
    fo = open(fname,"a+")
    fo.write(cmdresult)
    fo.write("\n")
    fo.close()

#读取设备列表，以及需要执行的命令，并调用文件操作函数
def checkConf():
    for dinfo in deviceInfo.devicelist:
        dinfolist=dinfo.split()
        dname=dinfolist[0]
        dip=dinfolist[1]
        duser=dinfolist[2]
        dpwd=dinfolist[3]
        fileInfo=resultDir+nowday+"-"+dname+".txt"
        fileopt(fileInfo)
        for cinfo in cmdInfo.cmdlist:
            cmd=cinfo
            dlogininfo ={
                'host': dip,
                'username': duser,
                'password': dpwd,
                'device_type': 'hp_comware' #hp_comware 为H3C设备支持类型；
            }
            netConn = ConnectHandler(**dlogininfo)
            output = netConn.send_command(cinfo)
            fileopt(fileInfo,output)

checkConf()

