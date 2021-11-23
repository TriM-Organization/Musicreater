# Musicreater

### 介绍
音·创(Musicreater)是由金羿(W-YI)开发的一款《我的世界》基岩版音乐生成辅助软件

欢迎加群：861684859

### 软件架构

软件采用Python作为第一语言，目前还没有使用其他语言辅助。现在的图形库是tkinter，后期将使用BeeWare兼容安卓

现阶段支持Windows7+，Linux(版本嘛，支持Python3.8就好)


### 安装教程

#### Windows7+

0.  [下载](https://gitee.com/EillesWan/Musicreater/repository/archive/master.zip)本程序
1.  安装Python 3.8.10 
    [下载64位安装包](https://www.python.org/ftp/python/3.8.10/python-3.8.10-amd64.exe)
    [下载32位安装包](https://www.python.org/ftp/python/3.8.10/python-3.8.10.exe)
2.  以管理员身份运行 补全库.py :
    -   按下 Ctrl+Shift+Esc 打开任务管理器
    -   点击 "文件" 菜单中的 运行新任务 命令
    -   输入 `cmd` 并框选 "以管理员身份运行" 按下 "确定"
    -   将 "补全库.py" 拖拽入开启的窗口，按下回车
3.  等待安装完成后，双击运行 Musicreater.py

#### Linux (测试版本：Kali 2021.4)

0.  若你没有足够优秀的环境，推荐先在终端敲：
```bash
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python3
sudo apt-get install python3-pip
sudo apt-get install git
```
1.  若你足够自信，该整的都整了，就在你想下载此程序的地方打开终端，敲：
```bash
sudo git clone https://gitee.com/EillesWan/Musicreater.git
cd Musicreater
python3 补全库.py
python3 Musicreater.py
```


### 使用说明

1.  直接运行就好
2.  看得懂简体中文字的不一定全会用
3.  最好要懂一点点英文

### 致谢

1.  感谢由 [Fuckcraft](https://gitee.com/fuckcraft) “鸣凤鸽子”等 带来的我的世界websocket服务器功能
2.  感谢 昀梦＜QQ1515399885＞ 找出指令生成错误bug并指正
3.  感谢由 Charlie_Ping “查理平” 带来的bdx转换功能
4.  感谢广大群友为此程序提供的测试等支持
5.  若您为我找出了错误但您的名字没有显示在此列表中，请联系我！


