# 音·创 Musicreater

### 介绍
音·创 Musicreater 是由金羿(*W-YI*)开发的一款 **《我的世界：基岩版》** 音乐生成辅助软件

欢迎加群：861684859

### 作者

金羿 (Eilles)：主要作者，开发了音·创主体，及其前身“函数音乐生成器”、“世界音创”。

bgArray “诸葛亮与八卦阵”：修复bug，改进代码美观度，增加新功能，更改数据格式等。

### 软件架构

软件采用 *Python* 作为第一语言，目前还没有使用其他语言辅助。使用 *Tkinter* 为图形库。

支持 Windows7+ 以及各个支持 Python3.8 的 Linux

***各位开发人员注意！！！多语言支持请使用`READABLETEXT`常量输出文字！！！如需补充，请在简体中文的语言文件(zhCN.py)中补充！！！***


### 安装教程

正在到来。

### 从源代码运行教程

#### Windows7+

0.  [Gitee下载（需要登陆）](https://gitee.com/EillesWan/Musicreater/repository/archive/master.zip)
    [Github下载（慢）](https://github.com/EillesWan/Musicreater/archive/refs/heads/master.zip)本程序源代码
1.  安装Python 3.8.10 
    [下载64位Python安装包](https://www.python.org/ftp/python/3.8.10/python-3.8.10-amd64.exe)
    [下载32位Python安装包](https://www.python.org/ftp/python/3.8.10/python-3.8.10.exe)
2.  以管理员身份运行 补全库.py :
    -   点击 “开始” 菜单，搜索 `命令提示符`
    -   右键点击 `命令提示符` 左键点击 “以管理员身份运行”
    -   将 “补全库.py” 拖拽入开启的窗口，按下回车
3.  等待安装完成后，双击运行 Musicreater.py

#### Linux

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


### 诸葛亮与八卦阵的说明（不必要）

1. 首先！这里的提示是给想使用多音色资源包的人的，如果你想用就请下载 [神羽资源包（神羽自己的链接）](https://pan.baidu.com/s/11uoq5zwN7c3rX-98DqVpJg)提取码:ek3t
2. 下载到你自己电脑上某个位置，可以不放置于本项目下。音色资源包较大，可以选取只下载：
    `神羽资源包_乐器、音源的资源包\羽音缭绕-midiout_25.0` 这个文件夹，再嫌麻烦的话，也可以只下载其中的：
    `神羽资源包_乐器\音源的资源包\羽音缭绕-midiout_25.0\mcpack(国际版推荐)格式_25.0` 或者：
    `神羽资源包_乐器\音源的资源包\羽音缭绕-midiout_25.0\zip格式_25.0`
4. 接下来就是关键了：在*音创*中绑定资源包
    首先，先打开 *音创*->帮助与疑问->\[神羽资源包位置选择\]：选择文件夹... 这时候，会跳出选择框
    关键来了，选择：***您下载的`羽音缭绕-midiout_25.0`文件夹，或者`mcpack(国际版推荐)格式_25.0`或`zip格式_25.0`的上级目录***
    举个例子：我的文件路径是这样的：
    `L:\shenyu\音源的资源包\羽音缭绕-midiout_25.0`这里面有：`神羽资源包_25.0_使用方法.xls`、
    `mcpack(国际版推荐)格式_25.0`、`zip格式_25.0`两个文件夹和一个.xls文件，而你在音创中
    也应该选择这个文件夹：**L:\shenyu\音源的资源包\羽音缭绕-midiout_25.0**
6. 如果你想使用音色资源包来制作函数，那么解析时你应该用 *音创*->编辑->从midi导入音轨且用新方法解析，
    然后再使用 *音创*->函数（包）->下面的四个新函数

### 致谢

1.  感谢由 [Fuckcraft](https://github.com/fuckcraft) “鸣凤鸽子”等 带来的我的世界websocket服务器功能
2.  感谢 昀梦\<QQ1515399885\> 找出指令生成错误bug并指正
3.  感谢由 Charlie_Ping “查理平” 带来的bdx转换功能
4.  感谢由 CMA_2401PT 带来的 BDXWorkShop 供本程序对于bdx操作的指导
5.  感谢由 Miracle Plume “神羽” \<QQshenyu40403\>带来的羽音缭绕基岩版音色资源包
6.  感谢 Arthur Morgan 对本程序的排错提出了最大的支持
7.  感谢广大群友为此程序提供的测试等支持
8.  若您对我们有所贡献但您的名字没有显示在此列表中，请联系我！


### 作者\<*金羿*\>(W-YI)联系方式

1.  QQ       2647547478
2.  电邮      EillesWan2006@163.com W-YI_DoctorYI@outlook.com EillesWan@outlook.com
3.  微信      WYI_DoctorYI

### 作者\<*诸葛亮与八卦阵*\>(bgArray) 联系方式

1.  QQ       4740437765