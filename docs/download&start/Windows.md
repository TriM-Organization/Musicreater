## 一、运行环境安装

### （一）安装 Python3.6+

1.	首先需要下载Python的安装包，最好是 *Python3.8*，因为作者就用的是这个版本

	> [下载64位Python安装包](https://www.python.org/ftp/python/3.8.10/python-3.8.10-amd64.exe)
	> [下载32位Python安装包](https://www.python.org/ftp/python/3.8.10/python-3.8.10.exe)

2.	在安装时，最好需要勾选 `Add Python 3.X to PATH`，如下图所示，当然，如果您对自己非常自信，您也可以手动设置此项目：

	<img src=https://foruda.gitee.com/images/1662736520757331846/e38efb81_9911226.png>

	-   若您对Python一知半解或者不怎么了解、并对自己的系统盘（通常是C盘）有大约150*兆字节*(MB)的信心的话，您可以在安装时直接选择*快速安装*(Install Now)

3.	若您选择了*自定义安装*(Customize Installation)，请务必勾选 `pip` 和 `py launcher` 便于后续安装依赖，如下图：

	<img src=https://foruda.gitee.com/images/1662736621235871190/2ac3d98f_9911226.png>

4.	安装结束之后可以在*终端*(命令行/PowerShell/Bash/etc)中输入：`python` 试试是否安装成功，成功安装之后，在终端中输入python会显示诸如如下图片的提示：

	<img src=https://foruda.gitee.com/images/1659972669907359295/cmd.png>


### （二）安装依赖

1.	请以管理员模式打开您的*终端*(命令行/PowerShell/Bash/etc)

	例如，命令行，可以如此打开：在*视窗开始菜单*(Windows开始)中搜索 `cmd`, 并以管理员身份运行

	<img src="https://foruda.gitee.com/images/1662736878650993886/62487dd8_9911226.png">
	
2.	打开了终端之后，请在终端中输入以下指令

	```bash
	pip install mido -i https://mirrors.aliyun.com/pypi/simple/
	pip install brotli -i https://mirrors.aliyun.com/pypi/simple/
	```

3.	安装成功后您可能会见到类似下图的提示：

	<img src="https://foruda.gitee.com/images/1662737676719454287/f61a70f7_9911226.png">

## 二、本工具的下载与使用

0. 下载本代码库以及演示程序

	-	若您使用git，请直接克隆本仓库：

		```bash
		git clone -b pkgver https://gitee.com/TriM-Organization/Musicreater.git
		```

	-	若您不使用git，可以在[*码云*(Gitee)](https://gitee.com/TriM-Organization/Musicreater.git)或[*GitHub*](https://github.com/TriM-Organization/Musicreater.git)下载zip包，或者[加入QQ群聊861684859](https://jq.qq.com/?_wv=1027&k=hpeRxrYr)，在群文件中获取。

		<img src="https://foruda.gitee.com/images/1669540786443169766/fabf0acd_9911226.png">

		值得注意的是，这张图上有1、2两个数字，虽然是手写的，但确实是数字，表示着要进行的步骤。希望眼尖得能找出我的口头禅的你们能够发现这两个用鼠标手写的数字并在安装时认真地执行。我认为这并不算十分的难，移动鼠标并单击大约消耗不了多少卡路里，不过我没有进行精确的计算，我也不是十分的清楚这个活动对于一个常人来讲有多难，但我怀疑它不难。


1. 开始使用

	您可以直接双击 `magicDemo.py` 以运行演示程序，或者按照以下步骤使用终端应用运行。

	在目录下打开终端。
	
	例如：打开命令行：请进入到目录下，在文件资源管理器的地址框内输入`cmd`：

	<img src=https://foruda.gitee.com/images/1659974437388532868/输入.png>
	<img src=https://foruda.gitee.com/images/1659974754378201859/输入c.png>

	使用以下指令：

	```bash
	python ./magicDemo.py	
	```

## 三、安装时错误的补充说明

1. Microsoft Visual C++ Redistributable 环境出错

	如果你遇到了类似以下这种情况：

	<img src=https://foruda.gitee.com/images/1659972789779764953/bug.jpeg>
	
	请下载最新的VCREDIST安装包，可以参照[这个网页](https://docs.microsoft.com/zh-CN/cpp/windows/latest-supported-vc-redist)的说明，也可以在这直接选择你需要的安装包下载：
	> [下载64位VCREDIST安装包](https://aka.ms/vs/17/release/vc_redist.x64.exe)
	> [下载32位VCREDIST安装包](https://aka.ms/vs/17/release/vc_redist.x86.exe)

	感谢群友*Mono*帮我们发现这个问题。