"""音创系列版本号和版本操作函数"""
# 统计：致命（三级）错误：0个；警告（二级）错误：0个；语法（一级）错误：24个


from msctspt.bugReporter import version
import os

# 以下下两个值请在 msctspt/bugReporter 的version类中修改
VER = version.version
"""当前版本"""

LIBS = version.libraries
"""当前所需库"""


# 判断版本、临时文件与补全库
def compver(ver1, ver2):
    """
    传入不带英文的版本号,特殊情况："10.12.2.6.5">"10.12.2.6"
    :param ver1: 版本号1
    :param ver2: 版本号2
    :return: ver1< = >ver2返回-1/0/1
    """
    list1 = str(ver1).split(".")
    list2 = str(ver2).split(".")
    # 循环次数为短的列表的len
    for i in range(len(list1)) if len(list1) < len(list2) else range(len(list2)):
        if int(list1[i]) == int(list2[i]):
            pass
        elif int(list1[i]) < int(list2[i]):
            return -1
        else:
            return 1
    # 循环结束，哪个列表长哪个版本号高
    if len(list1) == len(list2):
        return 0
    elif len(list1) < len(list2):
        return -1
    else:
        return 1


#
# ————————————————
# 版权声明：上面的函数compver为CSDN博主「基友死得早」的原创文章中的函数，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
# 原文链接：https://blog.csdn.net/tinyjm/article/details/93514261
# ————————————————
#


def InstallLibs(now, LIBS1):
    """比对库信息并安装库"""
    from os import system as run
    for i in LIBS1:
        if i not in now:
            print("安装库：" + i)
            run("python -m pip install " + i + " -i https://pypi.tuna.tsinghua.edu.cn/simple")


def chkver(ver=VER, libs=LIBS):
    """通过文件比对版本信息并安装库"""
    if not os.path.exists(os.getenv('APPDATA') + '\\Musicreater\\msct.ActiveDatas.msct'):
        print("新安装库")
        os.makedirs(os.getenv('APPDATA') + '\\Musicreater\\')
        with open(os.getenv('APPDATA') + '\\Musicreater\\msct.ActiveDatas.msct', 'w') as f:
            f.write(ver[0] + '\n')
            for i in libs:
                f.write(i + '\n')
        InstallLibs([], libs)
    else:
        with open(os.getenv('APPDATA') + '\\Musicreater\\msct.ActiveDatas.msct', 'r') as f:
            v = f.readlines()
        cp = compver(ver[0], v[0])
        if cp != 0:
            InstallLibs(v[1:], libs)
            with open(os.getenv('APPDATA') + '\\Musicreater\\msct.ActiveDatas.msct', 'w') as f:
                f.write(ver[0] + '\n')
                for i in libs:
                    f.write(i + '\n')
        del cp


def resetver():
    """重置版本信息"""
    import shutil
    shutil.rmtree(os.getenv('APPDATA') + '\\Musicreater\\')
