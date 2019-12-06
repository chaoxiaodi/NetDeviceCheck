#!/usr/bin/env python
from netmiko import Netmiko
from getpass import getpass
from netmiko import ConnectHandler
import os, time, re, string
import deviceInfo, cmdInfo, xlsStyle
import xlwt
from xlwt import *

# 定义时间作为配置文件输出信息
nowday=time.strftime("%Y-%m-%d-%H%M%S")
# 定义文件输出目录信息
resultDir = os.path.abspath('.') + '\outputFile\\'

# 文件操作函数，把对设备的操作输出到文件逻辑实现
def file_opt( fname,cmdresult = "" ):
    fo = open(fname,"a+")
    fo.write(cmdresult)
    fo.write("\n")
    fo.close()

#根据检查的提取的信息生成excel表格
def write_xls(fname, infodct):
    xlsbook = xlwt.Workbook()  # 创建表格
    swcheckres = xlsbook.add_sheet('SWCheckResult', cell_overwrite_ok=True)  # 创建表格的某一分页
    # 设置列宽
    col1 = swcheckres.col(0)  # 设置0、1、2、3列的列宽
    col2 = swcheckres.col(1)
    col3 = swcheckres.col(2)
    col4 = swcheckres.col(3)
    col1.width = 200 * 25
    col2.width = 150 * 25
    col3.width = 120 * 25
    col4.width = 350 * 25
    # 写入表头
    swcheckres.write(0, 0, '设备名称', xlsStyle.sheethead)
    swcheckres.write(0, 1, '管理地址', xlsStyle.sheethead)
    swcheckres.write(0, 2, '检查项', xlsStyle.sheethead)
    swcheckres.write(0, 3, '检查结果', xlsStyle.sheethead)
    #表固定格式
    i = 0
    # 根据字典循环写入excel表格
    for key in infodct.keys():
        # k 具体检查项的数量，后期增加后可以直接修改相乘的数字即可
        k = i * 7
        swcheckres.write_merge(k + 1, k + 7, 0, 0, key, xlsStyle.styledinfo)
        swcheckres.write_merge(k + 1, k + 7, 1, 1, infodct[key]['dip'], xlsStyle.styledinfo)
        swcheckres.write(k + 1, 2, '设备版本', xlsStyle.stylecinfo)
        swcheckres.write(k + 2, 2, '运行时间', xlsStyle.stylecinfo)
        swcheckres.write(k + 3, 2, '设备型号', xlsStyle.stylecinfo)
        swcheckres.write(k + 4, 2, '内存使用率', xlsStyle.stylecinfo)
        swcheckres.write(k + 5, 2, 'CPU使用率', xlsStyle.stylecinfo)
        swcheckres.write(k + 6, 2, '路由表数量', xlsStyle.stylecinfo)
        swcheckres.write(k + 7, 2, 'VLAN数量', xlsStyle.stylecinfo)
        # 写入具体检查信息
        swcheckres.write(k + 1, 3, infodct[key]['dversion'], xlsStyle.stylecinfo)
        swcheckres.write(k + 2, 3, infodct[key]['uptime'], xlsStyle.stylecinfo)
        swcheckres.write(k + 3, 3, infodct[key]['model'], xlsStyle.stylecinfo)
        swcheckres.write(k + 4, 3, infodct[key]['memory'], xlsStyle.stylecinfo)
        swcheckres.write(k + 5, 3, infodct[key]['cpu-usage'], xlsStyle.stylecinfo)
        swcheckres.write(k + 6, 3, infodct[key]['routes'], xlsStyle.stylecinfo)
        swcheckres.write(k + 7, 3, infodct[key]['vlannum'], xlsStyle.stylecinfo)

        # 保存表格
        xlsbook.save(fname)
        # i 判断循环几次要在表里增加几次对应内容
        i += 1

# 获取命令执行结果里的关键参数，并添加到字典，输出表格用
def getmaininfo( dname, dip, cinfo, output, infodct ):
    infodct["dip"] = dip
    if cinfo == 'display version':
        com = re.compile(r'.*Version.*')
        infodct["dversion"] = com.findall(output)[0].split(",")[-2].split(".")[-3].split()[1]
        com = re.compile(r'.*uptime is.*')
        infodct["uptime"] = ''.join(com.findall(output)[0].split()[4:12])
        infodct["model"] = ''.join(com.findall(output)[0].split()[1:2])
    if infodct["dversion"] == '7':
        if cinfo == 'display cpu-usage':
            com = re.compile(r'.*minutes')
            infodct["cpu-usage"] = com.findall(output)[0].split()[0]
        if cinfo == 'display memory':
            com = re.compile(r'Mem.*')
            infodct["memory"] = com.findall(output)[0].split()[7]
        if cinfo == 'display environment':
            com = re.compile(r'.*hotspot.*')
            infodct["temperature"] = com.findall(output)[0].split()[4]
        if cinfo == 'display ip routing-table':
            com = re.compile(r'.*outes.*')
            infodct["routes"] = com.findall(output)[0].split(":")[2]
        if cinfo == 'display vlan':
            com = re.compile(r'.*Total.*')
            infodct["vlannum"] = com.findall(output)[0].split()[2]
    if infodct["dversion"] == '5':
        if cinfo == 'display cpu-usage':
            com = re.compile(r'.*minutes')
            infodct["cpu-usage"] = "5"+com.findall(output)[0].split()[0]
        if cinfo == 'display memory':
            com = re.compile(r'Used Rate.*')
            infodct["memory"] = com.findall(output)[0].split(":")[1]
        if cinfo == 'display environment':
            com = re.compile(r'.*hotspot.*')
            infodct["temperature"] = com.findall(output)[0].split()[4]
        if cinfo == 'display ip routing-table':
            com = re.compile(r'.*Routes.*')
            infodct["routes"] = com.findall(output)[0].split(":")[2]
        if cinfo == 'display vlan':
            com = re.compile(r'.*Total.*')
            infodct["vlannum"] = com.findall(output)[0].split()[1]

    return infodct

# 读取设备列表，以及需要执行的命令，并调用文件操作函数
def checkConf():
    print("设备巡检开始，请稍后···\n巡检结果会保存到outputfile文件夹!")
    # 设备检查结果字典定义
    infodctres = {}
    for dinfo in deviceInfo.devicelist:
        dinfolist = dinfo.split()
        dname = dinfolist[0]  #设备名称
        dip = dinfolist[1]    #设备ip
        duser = dinfolist[2]  #设备用户名
        dpwd = dinfolist[3]   #设备密码
        file_info = resultDir+nowday+"-"+dname+".txt"
        file_opt(file_info, "Check Time:"+nowday)
        # netmiko模块登录信息配置
        dlogininfo = {
            'host': dip,
            'username': duser,
            'password': dpwd,
            'device_type': 'hp_comware'  # hp_comware 为H3C设备支持类型；
        }
        net_conn = ConnectHandler(**dlogininfo)
        # 临时字典定义，接收返回的分析数据
        infodct = {}
        for cinfo in cmdInfo.cmdlist:
            des="#\n<"+dname+">"+cinfo+'\n##'
            # 调用保存命令执行结果的函数
            file_opt(file_info,des)
            output = net_conn.send_command(cinfo)
            # 调用分析命令关键参数函数
            infodct = getmaininfo(dname, dip, cinfo, output, infodct)
            # 调用保存命令执行结果的函数
            file_opt(file_info, output)
        net_conn.disconnect()
        # 更新检查结果字典
        infodctres.update({
            dname : infodct
        })
    # 表格输出文件名定义
    xls_file = resultDir+nowday+'巡检结果.xls'
    write_xls(xls_file, infodctres)
    print("巡检完成！你可以到outputfile文件夹查看结果！")

if __name__ == '__main__':
    checkConf()
