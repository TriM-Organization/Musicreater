# -*- conding: utf8 -*- 

import os

m = 0

for path, dir_list, file_list in os.walk(r"./"):
    for file_name in file_list:
        if file_name.endswith('.py'):
            file = os.path.join(path, file_name)
            print("得到文件名：" + str(file))
            for i in open(file, 'r', encoding="utf-8"):
                code = i.replace(' ', '').replace('\n', '')
                
                if code.startswith('#'):
                    continue
                if code:
                    print("\t" + code)
                    m += 1
                else:
                    pass

input("\n最终代码行数为：" + str(m))
