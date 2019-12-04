# NetDeviceCheck
network device check
#项目说明
通过python netmiko模块实现H3C网络设备巡检
分析输出的信息并进行可视化输出
cmdInfo 包含所有需要在设备执行的命令
deviceInfo.py 包含所有需要巡检的网络设备信息

ps：设备需要开启SSH登录并允许列表里的用户登录

#···版本记录···
##v0.1 201912
完成设备登录实现
完成对设备命令返回结果收集并输出文件
