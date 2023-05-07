


import os
import zipfile


def compress_zipfile(sourceDir, outFilename, compression=8, exceptFile=None):
    """使用compression指定的算法打包目录为zip文件\n
    默认算法为DEFLATED(8),可用算法如下：\n
    STORED = 0\n
    DEFLATED = 8\n
    BZIP2 = 12\n
    LZMA = 14\n
    """

    zipf = zipfile.ZipFile(outFilename, "w", compression)
    pre_len = len(os.path.dirname(sourceDir))
    for parent, dirnames, filenames in os.walk(sourceDir):
        for filename in filenames:
            if filename == exceptFile:
                continue
            pathfile = os.path.join(parent, filename)
            arc_name = pathfile[pre_len:].strip(os.path.sep)  # 相对路径
            zipf.write(pathfile, arc_name)
    zipf.close()