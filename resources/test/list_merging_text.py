import random
import time
from itertools import chain

print("生成序列中")

fine_dict = {}

for i in range(50):
    print("正在生成第", i, "个序列",end="\r",flush=True)
    fine_dict[i] = [random.randint(0, 1000) for _ in range(random.randint(10000, 99999))]

print("序列生成完成")

def chain_merging(dict_info: dict):
    return sorted(chain(*dict_info.values()))

def seq_merging(dict_info: dict):
    return sorted([i for sub in dict_info.values() for i in sub])

def summing(*_):
    k = []
    for i in _:
        k += i
    return k
    
def plus_merging(dict_info: dict):
    return sorted(summing(*dict_info.values()))

function_list = [chain_merging, seq_merging, plus_merging]


for func in function_list:
    print("正在使用",func.__name__,"函数",)
    start = time.time()
    func(fine_dict)
    print("耗时",time.time() - start)

print("结束")