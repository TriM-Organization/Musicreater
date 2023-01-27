import brotli

input(brotli.decompress(open(input("BDX文件："), 'rb').read()[3:]))
