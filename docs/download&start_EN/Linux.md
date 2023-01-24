
## Install Runtime Environment

### Install and Verify Python Runtime

0.	Common Linux Distributions do include a Python Runtime Environment, what we should do is only to check whether it is a satisfied version to our program. If the version ≥Python3.6, theoretically our program can be run.

	We can type:

	```bash
	python -V
	```

	To check the Python version, as the follows
	
	<img src=https://foruda.gitee.com/images/1665120915821957090/429561fd_9911226.png>

1.	**Not Necessary**

	If you want to change a Python version just as what I want to do, it is such a great fantastic action! Let do as the follows:

	- pacman Package Manager（In Arch Linux Mostly）

		1.	Let's write python3 into the ingore list of updating. Via `vim` to edit `/etc/pacman.conf`, add `python3` after `IgnorePkg`.

			```bash
			sudo vim /etc/pacman.conf
			```

			<img src=https://foruda.gitee.com/images/1665124611490335193/5e99ca26_9911226.png>

		2.	Then we can search for python releases in [Arch Achieve](https://archive.archlinux.org/packages/).（*HERE, under Arch, Python refers to Python3 defaultly, while some other Linux releases using Python2 as default. So dose Arch Achieve.*）What I find here is [Python3.8.6](https://archive.archlinux.org/packages/p/python/python-3.8.6-1-x86_64.pkg.tar.zst), so let's download she via `pacman`:

			```bash
			sudo pacman -U https://archive.archlinux.org/packages/p/python/python-3.8.6-1-x86_64.pkg.tar.zst
			```

			<img src=https://foruda.gitee.com/images/1665126362769399903/ea4b9598_9911226.png>

		3.	Perfect!
	
	- Other Package Manager

		None yet.

###	Install and Verify pip Package Manager

1.	Before installing, it is to be checked, wheather Python's pip is OK:

	```bash
	python -m pip				# To check is pip installed
	# If a long tip occured, it is OK
	
	# If returned as this, then not.
	/usr/bin/python: No module named pip
	# We can install pip via:
	sudo pacman -S python-pip
	# Verfy, remember.
	python -m pip


	# If you did but failed, we should use other methods to install pip:
	wget https://bootstrap.pypa.io/get-pip.py
	sudo python get-pip.py
	# Verfy, must.
	python -m pip
	```

2.	After checking, let's install the dependences.
	
	```bash
	pip install mido -i
	pip install brotli -i
	```

3.	See the tips below as successfully installed：

	<img src="https://foruda.gitee.com/images/1662737676719454287/f61a70f7_9911226.png">


## Download this lib's sources code and Using its demos.

1.	Download via Git

	```bash
	git clone -b pkgver https://github.com/TriM-Organization/Musicreater.git MSCTpkgver
	```

	If succeed, a directory named `MSCTpkgver` well be found in the path you run this command, and inside it is the source code and demo(s) we wantted to download.
	What we want to use is the demo(s) so enter the folder via:

	```bash
	cd MSCTpkgver
	```

1.	Starting Using Demo(s)

	Via

	```bash
	python magicDemo.py
	```
