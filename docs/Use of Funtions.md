<h1 align="center">音·创 Musicreater</h1>

<p align="center">
<img width="128" height="128" src="https://s1.ax1x.com/2022/05/06/Ouhghj.md.png" >
</p>


# Instructions for Using Demo(s)

*This is a tutorial for using the demo(s) of this library, not the Development Guide. If you want to see so, please read Below*

## Under Windows

0. Install Python 3.6+

	First of all, you need to install the runtime environment of this library, *Python*. And a Installation Pack maybe the best choice:

	> [Downloading Python 64-bit](https://www.python.org/ftp/python/3.8.10/python-3.8.10-amd64.exe)
	> [Downloading Python 32-bit](https://www.python.org/ftp/python/3.8.10/python-3.8.10.exe)

	While installing, it's better to check `Add Python 3.X to PATH`(just as the screenshot showed below), otherwise it needs to be set manually which may cause some time wasting

	<img src=https://foruda.gitee.com/images/1662736520757331846/e38efb81_9911226.png>

	If you are new to Python or not very familiar to Computer Programming, and having the disk space in your PC's System Partition (usually C:) of 150 MB, you can directly choose *Install Now*.

	However, if you want to do it like a pro, choosing *Customize Installation*, it's a necessary to be sure to check `pip` and `py launcher` will be installed on your computer(see screenshot below). The two options is required for the next step of installing the requirements.

	<img src=https://foruda.gitee.com/images/1662736621235871190/2ac3d98f_9911226.png>

	After the installation, you can enter in your terminal(CMD/PowerShell/Bash/etc): "python" to ensure whether the installation was successful. If it was, your terminal will show things like below:

	<img src=https://foruda.gitee.com/images/1659972669907359295/cmd.png>


1. Installing Requirements

	It's better to open your terminal(CMD/PowerShell/Bash/etc) under Administrator Mode.

	For example, if you want to use CMD in Administrator Mode, you can search `cmd` in the *Start Menu*, right click it and *Run as Administrator*

	<img src="https://foruda.gitee.com/images/1662736878650993886/62487dd8_9911226.png">

	Okay, after that, please enter in your terminal:

	`pip install mido`

	`pip install brotli`

	If successful you will see something like below:

	<img src="https://foruda.gitee.com/images/1662737676719454287/f61a70f7_9911226.png">



2. Download This Package and Demo(s)

	- If you using Git, you can use the following commands to clone this lib:

	`git clone -b pkgver https://gitee.com/EillesWan/Musicreater.git`

	- If Git is not installed, you can download the zip package from the code page(from [GitHub](https://github.com/EillesWan/Musicreater.git) or [Gitee](https://gitee.com/EillesWan/Musicreater.git)). Or you are a Chinese fan having a QQ account, you can [Join the QQ Group 861684859](https://jq.qq.com/?_wv=1027&k=hpeRxrYr) and get it from our GroupFiles.

	<img src=" https://foruda.gitee.com/images/1659972440341216712/下载.png" >


2. Start Using Demo(s)

	Open your terminal in the directory of this, taking CMD, for example, just enter the directory and enter `cmd` in the path box:

	<img src=https://foruda.gitee.com/images/1659974437388532868/输入.png>
	<img src=https://foruda.gitee.com/images/1659974754378201859/输入c.png>

	And enter one of the commands below by choosing what you need:

	`python demo_convert.py`

	`python demo_convert_bdx_byDelay.py`


### Addition for Error(s) Using or Installing

1. Environment Error of Microsoft Visual C++ Redistributable

	If you meet this condition as the screenshot shows:

	<img src=https://foruda.gitee.com/images/1659972789779764953/bug.jpeg>

	Your MSVC Environment may be not installed, and you can download and install
	> [Here of 64-Bit VCREDIST](https://aka.ms/vs/17/release/vc_redist.x64.exe)
	> [Here of 32-Bit VCREDIST](https://aka.ms/vs/17/release/vc_redist.x86.exe)

	Thank our groupmate *Mono* again for helping finding this problem.

2. More Info for Parameters of Our Demo Program(s)

	<img src=https://foruda.gitee.com/images/1659974810147043475/运行.png>

	|Input Prompt|English Translation|Description|
	|----------------|----------------|-------|
	|请输入MIDI文件路径|Midi File Path|Path of a .mid file or a directory. While directory entered, our demo will convert all midi(s) in the directory|
	|请输入输出路径|Output Path|Where files converted in|
	|是否重置计分板|Whether Reset Scoreboard Automatically|Can only be 1 or 0(Recommanded 1)|
	|*进度条[注]|Progressbar|Whether to enable Progressbar and customize progressbar style. Type 0 or False to disable, 1 or True to use default style, or type using format taught in follow the Instructions below to customize one you like|
	|请输入计分板名称|Scoreboard Name|*Only not byDelay* The name of scoreboard that player using|
	|请输入音量|Volume|Only decimal in [0,1],(Recommanded 1)|
	|请输入速度倍率|Speed Multiplying Factor|Maybe you want to play it faster(＞1) or slower(＞0 ＜1)?|
	|请输入玩家选择器|Player Selector|Full Selector including `@x`. E.g: Play for players tagged `Holo`, enter `@a[tag=Holo]` on this parameter|




# Instructions for **Customize Progress Bar**

We have supported the function of making progress bar in *Minecraft*'s music player. And also the method of customize them. So the following instructions are about the parameters of the Progress Bar Customizition.

A Progress Bar, of course, is composed of **changeless** parts and **changable** parts. And the changable parts include texts or *images*(these images are made up of texts, or we can say, character paintings 😁). That is, for *Minecraft*, a changable image in a progress bar is just the "bar" part(which is like a stripe).

We use a string to describe the style of progress bar you need, and it includes many **identifier**s to replace the changable parts.

There are the identifiers:

| Identifier   | Changable Part                                       |
|--------------|------------------------------------------------------|
| `%%N`        | Music name(file name which is imported into program) |
| `%%s`        | Value of scoreboard of now                           |
| `%^s`        | Max value of scoreboard                              |
| `%%t`        | Current playback time                                |
| `%^t`        | Total music time                                     |
| `%%%`        | Current playback progress                            |
| `_`          | To be replaced by the *Bar* part of the progress bar |

The `_` is a placeholder to identifying the *bar* part, yeah, just the changable image.

This is an example of **style description string**, and this is also the default style of *Musicreater*'s progress bar.

`▶ %%N [ %%s/%^s %%% __________ %%t|%^t]`

This is a progress bar with only one line, but it is possible if you want to give a multiline parameter into the style description string.

But the string above is only for style identification, but we also need to identifying the changable image's image(just what the bar's look).

A "bar", simply, included 2 parts: *Have Been Played* & *Not Been Played*. So we use a tuple to pass the parameter. It's under a simple format: `(str: played, str: not)`. For example, the default parameter is below:

`('§e=§r', '§7=§r')`

So it's time to combine what I said in one parameter now!

This is a default definder parameter:

`('▶ %%N [ %%s/%^s %%% __________ %%t|%^t]',('§e=§r', '§7=§r'))`

*Tip: To avoid errors, please not to use the identifiers as the other part of your style.*
