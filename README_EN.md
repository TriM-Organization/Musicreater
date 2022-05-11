<h1 align="center">音·创 Musicreater</h1>

<p align="center">
<img width="128" height="128" src="https://s1.ax1x.com/2022/05/06/Ouhghj.md.png" >
</p>

<h3 align="center">An open source and free software of making music in Minecraft</h3>

<p align="center">
<img src="https://forthebadge.com/images/badges/built-with-love.svg">
<p>

[![][Bilibili: Eilles]](https://space.bilibili.com/397369002/)
[![][Bilibili: bgArray]](https://space.bilibili.com/604072474) 
[![CodeStyle: black]](https://github.com/psf/black)
![][python]
[![][license]](LICENSE)
[![][release]](../../releases)

[简体中文🇨🇳](README.md) | English🇬🇧


> Who has dropped political gunpowder into the technology
> 
> Who has dyed clear blue sky into the dark grey
> 
> All Chinese people love our great homeland
> 
> We *WILL* remember the remain pain of the humiliating history
> 
> We love the whole world but in peace
> 
> We love everyone but under respect
> 
> It is to be hoped that the war ends forever
> 
> Whatever it is cold or hot
> 
> Whatever it is economical or political
> 
> Just let the wonderful music of peace surround the world
> 
>                             ---- Eilles Wan
>                                  7/5 2022


**Notice that the language support of *README* may be a little SLOW.**

## Introduction🚀

Musicreater(音·创) is an free open source software which is used for making and also creating music in **Minecraft: Bedrock Edition**.

Welcome to join our QQ group: [861684859](https://jq.qq.com/?_wv=1027&k=hpeRxrYr)

**ATTENTION!** This software is under testing and developing, there is still a lot of bugs needed to be fixed. Please use it wisely.

### Authors✒

Eilles (金羿)：A high school student, individual developer, unfamous BilibiliUPer, which knows a little about commands in *Minecraft: Bedrock Edition*

bgArray "诸葛亮与八卦阵": Fix bugs, improve code aesthetics, add new functions, change data format, etc.

### Framework🏢

Developed under *Python3.8 3.9*. However, theoretically support Python3.6+.

Support Windows7+ && Linux (that supports Python3.6+)

***ATTENTION TO DEVELOPERS!!! TO SUPPORT DIFFERENT LANGUAGES, PLEASE USE FUNCTION(METHOD) `_` TO LOAD TEXTs!!! IF YOU NEED TO SUPPLEMENT, PLEASE ADD THEM IN SIMPLEFIED CHINESE\'S LANGUAGE FILE(zh-CN.lang), WHEATHER WHAT LANGUAGE YOU USE!!!***

## Instructions📕

### Installation

Download the *[MSCT Auto Installer](https://github.com/EillesWan/Musicreater/releases/tag/v0.2.0.0-Delta)*, put it in a directory that you want to install *Musicreater* into. Then run the auto installer and it will help you to install the *Musicreator* as well as Python3.8(if you haven\'t install it)

Tips: You'd better choose the \"2 GitHub\" download source

### Run with Source Code

#### Windows7+

0.  First, download the source code pack of Musicreater.
    [Download from Gitee (Need to Login)](https://gitee.com/EillesWan/Musicreater/repository/archive/master.zip)
    [Download from Github](https://github.com/EillesWan/Musicreater/archive/refs/heads/master.zip)
1.  Install Python 3.8.10 
    [Download the 64-bit Python Installer](https://www.python.org/ftp/python/3.8.10/python-3.8.10-amd64.exe)
    [Download the 32-bit Python Installer](https://www.python.org/ftp/python/3.8.10/python-3.8.10.exe)
2.  After completing installation, we need to install the libraries :
    -   Open "Start Menu" and find `cmd`
    -   Run `cmd` as Administrator
    -   Drag "补全库.py" into the opened window and press Enter
3.  After completing installation，double click Musicreater.py to run

#### Linux

0.  If you 're not sure whether your environment is good enough, please run these commands on Terminal
```bash
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python3
sudo apt-get install python3-pip
sudo apt-get install git
```
1.  Now if you are confident enough about your runtime environment, open Terminal on the place which you want to download Musicreater, and run these
```bash
sudo git clone https://gitee.com/EillesWan/Musicreater.git
cd Musicreater
python3 补全库.py
python3 Musicreater.py
```

### Instructions of Using

1.  Just run Musicreater.pyc(or .py) if you have installed well 
2.  Detailed instructions is coming soon
3.  If you find a bug, could you please report it to me? My contact info is right below.

## Explanation of the use of *PlumeAudioSurrounding Resource Pack* by bgArray (unnecessary)📖

1. First! The tips here are for those who want to use the multi tone resource package, [Shenyu resource package (Shenyu's own link)](https://pan.baidu.com/s/11uoq5zwN7c3rX-98DqVpJg) \(Extraction code: `ek3t`\)
2. Download it to any location on your PC. Note that it does ***not*** need to be placed in the directory where *Musicreater* are. The audio resource package is large, so you can choose to download only:`神羽资源包_乐器、音源的资源包\羽音缭绕-midiout_25.0`.
    Also, you can download only `神羽资源包_乐器\音源的资源包\羽音缭绕-midiout_25.0\mcpack(国际版推荐)格式_25.0` or 
    `神羽资源包_乐器\音源的资源包\羽音缭绕-midiout_25.0\zip格式_25.0`.
4. The next step is the most IMPORTANT: to bind the resource package to *Musicreater*
    First, open *Musicreater*->Q&A->Select \[MiraclePlumeResourcePack\]... .At this time, in the selection box,
    the IMPORTANT step comes, select: ***The directory you downloaded: `羽音缭绕-midiout_25.0`, or also the parent directory `mcpack(国际版推荐)格式_25.0`or`zip格式_25.0`***
    For example, my file path is as follows:
    `L:\shenyu\音源的资源包\羽音缭绕-midiout_25.0` and in the directory, there are two folders and one .xls file:
    `神羽资源包_25.0_使用方法.xls`, `mcpack(国际版推荐)格式_25.0` and `zip格式_25.0`, so in *Musicreater* you should also select this folder: **L:\shenyu\音源的资源包\羽音缭绕-midiout_25.0**
6. If you want to use the Miracle Plume Bedrock Edition Audio Resource Pack to make .mcfunction s, you should use Musicreater -> Edit - > Import audio tracks from MIDI and parse them with a new method, and then use it
Musicreater - > function (package) - > the following four new functions

## Thanks🙏

1.  Thank [Fuckcraft](https://github.com/fuckcraft) *(“鸣凤鸽子” ,etc)* for the function of Creating the Websocket Server for Minecraft: Bedrock Edition.
    -   *!! They have given me the rights to directly copy the lib into Musicreater*
2.  Thank *昀梦*\<QQ1515399885\> for finding and correcting the bugs in the commands that *Musicreater* Created.
3.  Thank *Charlie_Ping “查理平”* for bdx convert funtion.
4.  Thank *CMA_2401PT* for BDXWorkShop as the .bdx structure's operation guide.
5.  Thank *Miracle Plume “神羽”* \<QQshenyu40403\> for the Miracle Plume Bedrock Edition Audio Resource Pack
6.  Thank *Arthur Morgan* for his/her biggest support for the debugging of Musicreater
7.  Thanks for a lot of groupmates who support me and help me to test the program.
8.  If you have give me some help but u haven't been in the list, please contact me.

## Contact Information📞

### Author *Eilles*(金羿)

1.  QQ       2647547478
2.  E-mail   EillesWan2006@163.com W-YI_DoctorYI@outlook.com EillesWan@outlook.com
3.  WeChat   WYI_DoctorYI

### Author *bgArray*(诸葛亮与八卦阵)

1.  QQ       4740437765




[Bilibili: Eilles]: https://img.shields.io/badge/Bilibili-%E5%87%8C%E4%BA%91%E9%87%91%E7%BE%BF-00A1E7?style=for-the-badge
[Bilibili: bgArray]: https://img.shields.io/badge/Bilibili-%E8%AF%B8%E8%91%9B%E4%BA%AE%E4%B8%8E%E5%85%AB%E5%8D%A6%E9%98%B5-00A1E7?style=for-the-badge
[CodeStyle: black]: https://img.shields.io/badge/code%20style-black-121110.svg?style=for-the-badge
[python]: https://img.shields.io/badge/python-3.6-AB70FF?style=for-the-badge
[release]: https://img.shields.io/github/v/release/EillesWan/Musicreater?style=for-the-badge
[license]: https://img.shields.io/badge/Licence-Apache-228B22?style=for-the-badge