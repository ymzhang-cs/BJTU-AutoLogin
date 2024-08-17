# BJTU-AutoLogin
北京交通大学校园网自动登录脚本

## 简介

本项目旨在帮助用户自动登录北京交通大学的校园网。支持以下功能：

- 个人电脑开机自动登录
- 服务器命令行界面下登录

该脚本支持 Windows 和 Unix 系统，用户可以根据自己的需求选择合适的版本。

> [!IMPORTANT]
> 由于脚本中需要明文存储上网密码，请在使用时注意保护个人隐私和安全。

## 原理

通过解析校园网登录时的数据包，核心操作是向以下网址发送 GET 请求：

```
https://login.bjtu.edu.cn:802/eportal/portal/login?
callback=dr1003
&login_method=1
&user_account=你的学号
&user_password=你的上网密码
&wlan_user_ip=你的内网IP
&wlan_user_ipv6=
&wlan_user_mac=本机MAC地址
&wlan_ac_ip=
&wlan_ac_name=
&jsVersion=上网系统js版本
&terminal_type=1
&lang=zh-cn
&v=猜测为随机数
&lang=zh
```

本项目的脚本会自动补全内网IP、本机MAC地址和上网系统js版本信息，以便在这些信息过期时无需手动更新。

## Windows

1. 下载脚本 `bjtu_login.ps1`

2. 打开脚本并在提示注释处的引号内填写你的学号和上网密码

3. 右键脚本并选择“使用 PowerShell 运行”，或者创建任务计划来自动执行

### 创建任务计划

你可以参考这篇博客：https://www.cnblogs.com/Arisf/p/16186145.html

**注意事项**

1. 在“程序或脚本”栏中填写 `bjtu_login.ps1` 的文件路径

2. SSID名称应为'web.wlan.bjtu'
   
    在编辑XML时，请在`</select>`前添加以下代码：

    ```xml
    [EventData[Data[@Name='SSID']='web.wlan.bjtu']]
    ```

    完成编辑后，XML 代码应与下方代码一致：

    ```xml
    <QueryList>
    <Query Id="0" Path="Microsoft-Windows-WLAN-AutoConfig/Operational">
        <Select Path="Microsoft-Windows-WLAN-AutoConfig/Operational">*[System[Provider[@Name='Microsoft-Windows-WLAN-AutoConfig'] and (EventID=8001)]][EventData[Data[@Name='SSID']='web.wlan.bjtu']]</Select>
    </Query>
    </QueryList>
    ```

    你也可以直接复制这段代码。

## Linux / macOS

1. 下载脚本 `bjtu_login.sh`

2. 打开脚本并在提示注释处的引号内填写你的学号和上网密码

3. 赋予脚本执行权限：`chmod +x bjtu_login.sh`

4. 在命令行中执行：`./bjtu_login.sh`


## FAQ

### 无法打开校园网登录页面

如通过 `http://10.10.42.3/` 与 `https://login.bjtu.edu.cn/` 都无法正常显示校园网登录页面，可能是网络配置存在问题。

请按以下步骤逐一排查，并在每完成一步后重新尝试打开登录页面：

1. 退出代理软件

2. 将 DNS 设置为自动分配
   
   打开“设置”，`网络和 Internet` - `WLAN` - `web.wlan.bjtu 属性`，找到“DNS 服务器分配”，设置为“自动(DHCP)”。

### 已登录校园网，但仍无法上网，注销时出现错误

一般是因为 MAC 地址绑定错误，属于系统 BUG。可以通过设置随机 MAC 地址解决。

操作步骤：打开“设置”，`网络和 Internet` - `WLAN` - `web.wlan.bjtu 属性`，找到“随机硬件地址”，设置为“开”或“每天更改”。

### 正确配置了任务计划，但连接校园网时未自动登录

请检查是否启用了代理软件，并配置了开机自启，可能导致无法访问校园网登录页面。

解决方案 1：将 `10.0.0.0/8` 网段配置为 DIRECT 直连模式。

解决方案 2：取消代理软件的开机自启设置，并在校园网登录的任务计划中添加启动代理软件的步骤。

## 许可证与免责声明

请勿在使用过程中违反法律法规与北京交通大学网络管理相关规定。

本项目按“现状”提供，作者不对使用本脚本所产生的任何后果负责。使用本脚本的风险由用户自行承担。

详细的责任限制和许可条件请参阅 [MIT License](LICENSE) 文件。
