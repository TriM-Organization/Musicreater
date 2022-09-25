<h1 align="center">音·创 Musicreater</h1>

<p align="center">
<img width="128" height="128" src="https://s1.ax1x.com/2022/05/06/Ouhghj.md.png" >
</p>

<h3 align="center">一个免费开源的《我的世界：基岩版》音乐编辑制作软件</h3>

<p align="center">
<img src="https://forthebadge.com/images/badges/built-with-love.svg">
<p>


[![][Bilibili: 凌云金羿]](https://space.bilibili.com/397369002/)
[![][Bilibili: 诸葛亮与八卦阵]](https://space.bilibili.com/604072474) 
[![CodeStyle: black]](https://github.com/psf/black)
[![][python]](https://www.python.org/)
[![][license]](LICENSE)
[![][release]](../../releases)


简体中文 | [English](README_EN.md)


## 软件介绍🚀

音·创 Musicreater 是一款免费开源的 **《我的世界：基岩版》** 音乐制作软件

欢迎加群：[861684859](https://jq.qq.com/?_wv=1027&k=hpeRxrYr)

**注意注意注意！！！当前版本正在进行代码重构，详细信息请进入QQ群了解！！**

## 软件作者✒

金羿 Eilles：我的世界基岩版指令师，个人开发者，B站不知名UP主，南昌在校高中生。

诸葛亮与八卦阵 bgArray：我的世界基岩版玩家，喜欢编程和音乐，深圳初二学生。

## 软件架构🏢

软件采用 *Python* 作为第一语言，目前还没有使用其他语言辅助。

支持 Windows7+ 以及各个支持 Python3.6+ 的 Linux

***各位开发人员注意！！！多语言支持请使用函数`_`加载文字！！！如需补充，请在简体中文的语言文件(zh-CN.lang)中补充！！！***

## 使用教程📕

### 安装教程

下载[音·创自动安装器](https://gitee.com/EillesWan/Musicreater/releases/v0.2.0.0-Delta)，将其放在你希望安装音·创的位置，运行后将自动安装。

提示：下载源最好选择\"2 GitHub\"。

### 从源代码运行教程

#### Windows7+

0.  [Gitee下载（需要登陆）](https://gitee.com/EillesWan/Musicreater)
    [Github下载（慢）](https://github.com/EillesWan/Musicreater)本程序源代码
1.  安装Python 3.8.10 
    [下载64位Python安装包](https://www.python.org/ftp/python/3.8.10/python-3.8.10-amd64.exe)
    [下载32位Python安装包](https://www.python.org/ftp/python/3.8.10/python-3.8.10.exe)
2.  以管理员身份运行 作者的自我修养.py :
    -   点击 “开始” 菜单，搜索 `命令提示符`
    -   右键点击 `命令提示符` 左键点击 “以管理员身份运行”
    -   将 “作者的自我修养.py” 拖拽入开启的窗口，按下回车
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
python3 作者的自我修养.py
python3 Musicreater.py
```

### 使用说明

1.  直接运行就好
2.  后期会出详细的使用教程
3.  如果在使用过程中发现了bug拜托请上报给我，详见下方联系方式

## 诸葛亮与八卦阵的关于羽音缭绕资源包应用地说明（不必要）📖

0. ***注意注意！！！这一条说明是供给老版本(Delta 0.1.x)使用的***
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

## 致谢列表🙏

1.  感谢由 [Fuckcraft](https://github.com/fuckcraft) “鸣凤鸽子”等 带来的我的世界websocket服务器功能
2.  感谢 昀梦\<QQ1515399885\> 找出指令生成错误bug并指正
3.  感谢由 Charlie_Ping “查理平” 带来的bdx转换功能
4.  感谢由 CMA_2401PT 带来的 BDXWorkShop 供本程序对于bdx操作的指导
5.  感谢由 神羽 (Miracle Plume) \<QQshenyu40403\>带来的羽音缭绕基岩版音色资源包
6.  感谢 Arthur Morgan 对本程序的排错提出了最大的支持
7.  感谢广大群友为此程序提供的测试等支持
8.  若您对我们有所贡献但您的名字没有显示在此列表中，请联系我！

## 联系我们📞

### 作者\<*金羿*\>(Eilles)联系方式

1.  QQ       2647547478
2.  电邮      EillesWan2006@163.com W-YI_DoctorYI@outlook.com EillesWan@outlook.com
3.  微信      WYI_DoctorYI

### 作者\<*诸葛亮与八卦阵*\>(bgArray) 联系方式

1.  QQ       4740437765

## 待办事项⏲

* - [x] 支持自动安装
* - [ ] 支持多语言
* - [ ] 支持音乐编辑
* - [ ] 窗口优化
* - [ ] 1.支持插件功能
* - [ ] 2.进度条
* - [ ] 3.可以将音乐写入音符盒（红乐）
* - [ ] 4.修改UI界面使之适应当前功能
* - [ ] 5.支持自动给音符盒绑定更多的音色
* - [ ] 6.可以由.schematic文件导入地图，亦可反向处理
* - [ ] 7.制作软件下载器使用户更直观地操作
* - [ ] 8.支持自定义创建websockeet服务器播放音乐
* - [ ] 9.支持使用红石播放音乐
* - [ ] 10.支持采用延时的播放器
* - [ ] 11.支持使用bdx导出结构
* - [ ] 12.支持采用tp的方法播放
* - [ ] 13.支持识别曲谱（简谱）图片解析音乐
* - [ ] 14.支持使用瀑布流的方式播放音乐
* - [ ] 15.支持读入Everyone Piano的曲谱文件（.eop）
* - [ ] 16.支持读入Musescore的通用曲谱文件，即musicXML（.mscz、.mscx）
* - [ ] 17.支持自动搜寻地图目录位置（网易&微软）
* - [ ] 18.支持读入JPword曲谱文件（.jpd）
* - [ ] 19.新的UI设计，以及UI主题文件
* - [ ] 20.以小节为单位做音符播放时间对标



[Bilibili: 凌云金羿]: https://img.shields.io/badge/Bilibili-%E5%87%8C%E4%BA%91%E9%87%91%E7%BE%BF-00A1E7?style=for-the-badge
[Bilibili: 诸葛亮与八卦阵]: https://img.shields.io/badge/Bilibili-%E8%AF%B8%E8%91%9B%E4%BA%AE%E4%B8%8E%E5%85%AB%E5%8D%A6%E9%98%B5-00A1E7?style=for-the-badge
[CodeStyle: black]: https://img.shields.io/badge/code%20style-black-121110.svg?style=for-the-badge
[python]: https://img.shields.io/badge/python-3.6-AB70FF?style=for-the-badge
[release]: https://img.shields.io/github/v/release/EillesWan/Musicreater?style=for-the-badge
[license]: https://img.shields.io/badge/Licence-Apache-228B22?style=for-the-badge
