# -*- conding: utf8 -*- 

import os 
from msctspt.funcOpera import keepart


l = 0

for path,dir_list,file_list in os.walk(r"./") :  
    for file_name in file_list:  
        if keepart(file_name,'.',None) == '.py':
            file = os.path.join(path, file_name)
            print("得到文件名："+str(file))
            for i in open(file,'r',encoding="utf-8"):
                code = i.replace(' ','').replace('\n','')
                try:
                    code -= code[code.index('#'):]
                except:
                    pass
                if code:
                    print("\t"+code)
                    l+=1
                else:
                    pass

input("\n最终代码行数为："+str(l))

