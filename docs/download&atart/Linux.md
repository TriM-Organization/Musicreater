
##  运行环境安装

### 检验Python运行环境

0.	一般的Linux发行版都有安装Python环境，我们只需要保证其版本即可，理论上 ≥Python3.6 都可以运行我们的库

	我们可以使用

	```bash
	python -V
	```

	来查看 Python 版本，如下
	
	<img src=https://foruda.gitee.com/images/1665120915821957090/429561fd_9911226.png>

1.	*非必要环节*：回退版本

	如果你跟作者一样，觉得 Python 3.10+ 太难用很烦人的话，那真是皆大欢喜，让我们一起来回退版本吧！

	-	pacman 包管理器（多用于Arch Linux上）

		1.	让我们先来把 python3 加入忽略升级的列表中，使用`vim`修改`/etc/pacman.conf`，在`IgnorePkg`后加上`python3`

			```bash
			sudo vim /etc/pacman.conf
			```

			<img src=https://foruda.gitee.com/images/1665124611490335193/5e99ca26_9911226.png>

		2.	然后我们开始从[Arch Achieve](https://archive.archlinux.org/packages/)上找Python的版本列表。（*这里说明一下，在Arch中，Python默认指的是Python3，而与其他某些Linux发行版中Python默认指代Python2不同，所以在Arch Achieve中也是如此。*）我这里找到的是[Python3.8.6](https://archive.archlinux.org/packages/p/python/python-3.8.6-1-x86_64.pkg.tar.zst)，于是我们用`pacman`把她下载下来并安装：

			```bash
			sudo pacman -U https://archive.archlinux.org/packages/p/python/python-3.8.6-1-x86_64.pkg.tar.zst
			```

			<img src=https://foruda.gitee.com/images/1665126362769399903/ea4b9598_9911226.png>

		3.	完美！
	
	-	其他包管理器

		暂无

### 检查并安装pip包管理器依赖

1.	我们在安装依赖库之前，应该确认一下，Python自带的包管理器pip是否安装到位：

	```bash
	python -m pip				# 确认pip是否安装
	# 当这个命令输入后有长段提示出现则为已经安装

	# 如果返回如下，那么则pip尚未安装
	/usr/bin/python: No module named pip
	# 可以使用如下命令来安装pip
	sudo pacman -S python-pip
	# 安装完成后记得验证
	python -m pip


	# 如果还是失败，那么就需要用其他工具安装pip：
	wget https://bootstrap.pypa.io/get-pip.py
	sudo python get-pip.py
	# 安装完成后一定要验证！！！
	python -m pip
	```

2.	确认完成之后，我们来安装一下依赖库：
	
	```bash
	pip install mido -i https://mirrors.aliyun.com/pypi/simple/
	pip install brotli -i https://mirrors.aliyun.com/pypi/simple/
	```

3.	安装成功后可能会见到类似下图的提示：

	<img src="https://foruda.gitee.com/images/1662737676719454287/f61a70f7_9911226.png">


## 本代码库的下载与使用

1. 使用Git下载本库及其示例代码

	```bash
	git clone -b pkgver https://gitee.com/EillesWan/Musicreater.git MSCTpkgver
	```

	当上述命令执行成功，你会在执行此命令的所在位置发现一个名为 `MSCTpkgver` 的文件夹，其中包含的正是我们心心念念下载的本程序和示例代码。
	而我们要运行的也正是示例代码，因此，赶快进入下载到的文件夹：

	```bash
	cd MSCTpkgver
	```

1. 开始使用

	在目录下打开终端，执行以下命令以运行演示程序：

	```bash
	python magicDemo.py
	```

