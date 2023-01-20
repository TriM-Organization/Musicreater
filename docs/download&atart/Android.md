##	使用前的准备工作

###	安装终端工具

这里我们选用 **Termux** 作为我们的终端工具来安装，这是一个强大的终端模拟器，旨在安卓环境下模拟Linux的软件包环境。

1.	下载

	下载可以通过 [GitHub源](https://github.com/termux/termux-app/releases) 或者 [F-Droid源](https://f-droid.org/en/packages/com.termux/) ，个人建议选择 F-Droid 源，因为在国内可以访问得到，而 GitHub 源就看运气。

2.	安装

	下载*APK*包后直接安装，安装后打开可以看到一个类似这样的界面：

	<img height="512" src="https://foruda.gitee.com/images/1665933025120627254/a0479618_9911226.jpeg">

3.	完成
    
	恭喜你，你已经获得了一个极客般流畅地操作你手机的终端工具。

###	安装运行环境

1.	换源

	接下来，我们就要来准备安装一下 **Python** 运行环境了，这是运行 **Python** 源代码必要的。

	首先，我估计你等不了多久，急得要死，所以我们要让下载速度稍微快一点，先来换个源。在 **Termux** 中，输入以下指令：

	```bash
	echo "deb https://mirror.mwt.me/termux/main stable main" > /data/data/com.termux/files/usr/etc/apt/sources.list
	```

	*感谢 天如<QQ 3291691454>为我们带来的简单换源方法。*
    
	-	*非必要步骤*：手动编辑换源
    
		如果你闲着没事，非要要手动编辑个文档来换源，那用啥？用普通的编辑器肯定可以，于是我们就让他更普通一点，用**nano**吧！

		在 **Termux** 中，输入以下指令：

		```bash
		export EDITOR=nano
		apt edit-sources
		```
		
		那么请把看到的如左下图的界面变为右下图吧：

		<table><tr>
		<td><img src="https://foruda.gitee.com/images/1665933104313107707/41108f03_9911226.jpeg"> </td>
		<td><img src="https://foruda.gitee.com/images/1665933122534781330/3887a901_9911226.jpeg"></td>
		</tr></table>

		- 图片中的文件，最后应该加入的两行为：
		
			```bash
			deb https://mirrors.ustc.edu.cn/termux/apt/termux-main/ stable main
			deb https://mirrors.tuna.tsinghua.edu.cn/termux/apt/termux-main/ stable main
			```

		然后键入 `Ctrl`+`S`，再键入 `Ctrl`+`X`，退出`nano`。

	在换源之后，你可能会见到类似的提示：

	```bash
	Your '/data/data/com.termux/files/usr/etc/apt/sources.list' file changed. Please run 'apt-get update'.
	```

	那就遵循它的指引，输入：

	```bash
	apt-get update
	```

	Alright.
	
2.	安装 **Python**

	```bash
	apt-get install python3
	```

	如果遇到提示问是否继续，那就输入`Y`表示是，如左下图，安装成功后，图若右下。

	<table><tr>
	<td><img src="https://foruda.gitee.com/images/1665933181440420034/7f0fb5fd_9911226.jpeg"></td>
	<td><img src="https://foruda.gitee.com/images/1665933238339972260/a9f06f4f_9911226.jpeg"></td>
	</tr></table>

	接下来，我们来试一试 **Python** 是不是安装成了吧，输入

	```bash
	python3 -V
	```

	如果输出了形如 `Python 3.X.X` 的提示，则完成。

3.	安装依赖库
	
	```bash
	# 首先换源
	pip config set global.index-url http://mirrors.aliyun.com/pypi/simple/
	# 然后安装
	pip install mido
	pip install brotli
	```

	- 如果出现以下情况，真是死了鬼的，我们要来再搞个设置：

		<img height="512" src="https://foruda.gitee.com/images/1665933289612919459/b87b7804_9911226.jpeg">

		我们来修改收信任的源设置：

		```bash
		pip config set global.trusted-host mirrors.aliyun.com/
		```

		之后再来安装即可

		```bash
		pip install mido
		pip install brotli
		```

	安装成功后您可能会见到类似下图的提示：

	<img src="https://foruda.gitee.com/images/1662737676719454287/f61a70f7_9911226.png">

###	安装下载工具

既然已经有了运行环境，那么我们就需要下载下我们的**音·创库版示例代码**工具，我非常推崇**Git**这种方便快捷好用还能下载仓库的代码管理器，这个世界上你也找不到第二个，所以我们来安装一下：

```bash
pkg install git
```

安装完成后记得测试一下：

<img height="512" src="https://foruda.gitee.com/images/1665933331269483373/9374c85d_9911226.jpeg">

## 本代码库的下载与演示程序的使用

1. 使用Git下载本库及其示例代码

	```bash
	git clone -b pkgver https://gitee.com/EillesWan/Musicreater.git MSCTpkgver
	```

	当上述命令执行成功，你会在执行此命令的所在位置发现一个名为 `MSCTpkgver` 的文件夹，其中包含的正是我们心心念念下载的本程序和示例代码。
	而我们要运行的也正是示例代码，因此，赶快进入下载到的文件夹：

	```bash
	cd MSCTpkgver
	```

1. 开始使用演示程序

	依照你的需要，执行以下命令以运行库的演示程序：

	```bash
	python magicDemo.py
	```

	运行成功了，哦耶！

	<img height="512" src="https://foruda.gitee.com/images/1665933366784631363/db9f80f6_9911226.jpeg">

