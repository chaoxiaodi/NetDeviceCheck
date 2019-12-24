NetDeviceCheck

# 项目说明
用到的模块<br />
os<br />
time<br />
netmiko<br />
xlwt<br />
<br />

通过python netmiko模块实现H3C网络设备巡检<br />
分析输出的信息并进行可视化输出<br />
cmdInfo 包含所有需要在设备执行的命令列表(建议把命令补全)<br />
deviceInfo.py 包含所有需要巡检的网络设备信息<br />

|设备名称 | 设备IP | 用户名 | 密码 |
|---------|------------|------|---------|
|'sw0013 |192.168.1.13 |admin |12345678'|
<br />
ps：设备需要开启SSH登录并允许列表里的用户登录<br />

# 版本记录
## v0.1 201912
完成设备登录实现<br />
完成对设备命令返回结果收集并输出文件<br />

## v0.2 201912
修改登录并执行命令逻辑；加快程序运行速度；
完成对设备命令进行的分析结果

# 运行结果截图

![ndcrunpng](https://github.com/chaoxiaodi/NetDeviceCheck/blob/master/ndc-result.png) <br />


PS：如果各位有想增加分析的内容可以提一下 
