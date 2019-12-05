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

#具体登录设备并执行命令逻辑
def execcmd(dip,duser,dpwd,cinfo):
    dlogininfo = {
        'host': dip,
        'username': duser,
        'password': dpwd,
        'device_type': 'hp_comware'  # hp_comware 为H3C设备支持类型；
    }
    netConn = ConnectHandler(**dlogininfo)
    output = netConn.send_command(cinfo)
    return output

#读取设备列表，以及需要执行的命令，并调用文件操作函数
def checkConf():
    for dinfo in deviceInfo.devicelist:
        dinfolist=dinfo.split()
        dname=dinfolist[0]  #设备名称
        dip=dinfolist[1]    #设备ip
        duser=dinfolist[2]  #设备用户名
        dpwd=dinfolist[3]   #设备密码
        fileInfo=resultDir+nowday+"-"+dname+".txt"
        fileopt(fileInfo,"Check Time:"+nowday)
        for cinfo in cmdInfo.cmdlist:
            des="#\n<"+dname+">"+cinfo+'\n##'
            fileopt(fileInfo,des)
            output = execcmd(dip,duser,dpwd,cinfo)
            fileopt(fileInfo,output)

def pxls():
    pass

checkConf()
pxls

