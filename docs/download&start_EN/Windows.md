## Install Runtime Environment

### Install Python 3.6+

1.	First of all, you need to install the runtime environment of this library, *Python*. And a Installation Pack maybe the best choice:

	> [Downloading Python 64-bit](https://www.python.org/ftp/python/3.8.10/python-3.8.10-amd64.exe)
	> [Downloading Python 32-bit](https://www.python.org/ftp/python/3.8.10/python-3.8.10.exe)

2.	While installing, it's best to check `Add Python 3.X to PATH`(just as the screenshot showed below), otherwise it needs to be set manually which may cause some time wasting.

	<img src=https://foruda.gitee.com/images/1662736520757331846/e38efb81_9911226.png>

	-	If you are new to Python or not very familiar to Computer Programming, and having the disk space in your PC's System Partition (usually C:) of 150 *MB*, you can directly choose *Install Now*.

3.	However, if you want to do it like a pro, choosing *Customize Installation*, it's necessary to be sure to check `pip` and `py launcher` will be installed on your computer(see screenshot below). The two options is required for the next step of installing the requirements.

	<img src=https://foruda.gitee.com/images/1662736621235871190/2ac3d98f_9911226.png>

4.	After the installation, you can enter in your *Terminal*(CMD/PowerShell/Bash/etc): `python` to ensure whether the installation was successful. If it was, your terminal will show things like below:

	<img src=https://foruda.gitee.com/images/1659972669907359295/cmd.png>


### Installing Requirements

1.	It's better to open your *Terminal*(CMD/PowerShell/Bash/etc) under Administrator Mode.

	For example, if you want to use CMD in Administrator Mode, you can search `cmd` in the *Start Menu*, right click it and *Run as Administrator*

	<img src="https://foruda.gitee.com/images/1662736878650993886/62487dd8_9911226.png">

2.	Okay, after that, please enter in your Terminal:

	```bash
	pip install mido
	pip install brotli
	```

3.	If successful you will see something like below:

	<img src="https://foruda.gitee.com/images/1662737676719454287/f61a70f7_9911226.png">


## Downloading & Using of this tool

1. Download This Package and Demo(s)

	-	If you use Git, you can clone this lib via the following commands:

	```bash
	git clone -b pkgver https://github.com/TriM-Organization/Musicreater.git
	```

	-	If Git is not installed, you can download the zip package from the code page(from [GitHub](https://github.com/TriM-Organization/Musicreater.git) or [Gitee](https://gitee.com/TriM-Organization/Musicreater.git)). Or you are a Chinese fan having a QQ account, you can [Join the QQ Group 861684859](https://jq.qq.com/?_wv=1027&k=hpeRxrYr) and get it from our GroupFiles.

	<img src="https://foruda.gitee.com/images/1669540786443169766/fabf0acd_9911226.png">

	But it should be noticed that you're clear instructed to choose the branch "pkgver" first instead of downloading it directly from the "master" branch, the master branch is now under developing and has no practical use.


2. Start Using Demo(s)

	You can directly double click `magicDemo.py` to run the demo, or follow instructions below using Terminal APP to run it.

	Open your terminal in the directory of this, taking CMD, for example, just enter the directory and enter `cmd` in the path box:

	<img src=https://foruda.gitee.com/images/1659974437388532868/输入.png>
	<img src=https://foruda.gitee.com/images/1659974754378201859/输入c.png>

	And enter the commands below:

	```bash
	python ./magicDemo.py	
	```


## Addition for Error(s) Using or Installing

1. Environment Error of Microsoft Visual C++ Redistributable

	If you meet this condition as the screenshot shows:

	<img src=https://foruda.gitee.com/images/1659972789779764953/bug.jpeg>

	Your MSVC Environment may be not installed, and you can download and install
	> [Here of 64-Bit VCREDIST](https://aka.ms/vs/17/release/vc_redist.x64.exe)
	> [Here of 32-Bit VCREDIST](https://aka.ms/vs/17/release/vc_redist.x86.exe)
	or follow [this page](https://learn.microsoft.com/en-gb/cpp/windows/latest-supported-vc-redist)'s instructions.

	Thanks to our groupmate *Mono* for helping us finding this problem.

