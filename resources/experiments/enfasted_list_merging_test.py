import random
import time
from itertools import chain
from multiprocessing import Pool, Process, freeze_support

from rich.console import Console
from rich.progress import Progress
from rich.table import Table

console = Console()

# gening_stst = {"NOWIDX": 0, "DATA": {}}


# 生成单个字典的函数（用于多进程）
def generate_single_dict(args):
    dict_id, dict_size = args
    # if dict_id:
    #     console.print(
    #         f"字典 {dict_id + 1} 大小 {dict_size} 生成中...",
    #     )
    # else:
    #     console.print(
    #         f"\n字典 {dict_id + 1} 大小 {dict_size} 生成中...",
    #     )
    # final_d = {}
    # gening_stst["DATA"][dict_id] = 0
    # for i in range(dict_size):
    #     final_d[i] = [random.randint(0, 1000) for _ in range(random.randint(10000, 99999))]
    #     gening_stst["DATA"][dict_id] += 1
    return dict_id, {
        i: [random.randint(0, 1000) for _ in range(random.randint(10000, 90000))]
        for i in range(dict_size)
    }
    # return dict_id, final_d


# 合并函数定义
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


if __name__ == "__main__":
    freeze_support()  # Windows系统需要这个调用

    # 测试配置
    dict_size = 50  # 每个字典的键值对数量
    num_tests = 50  # 测试次数

    function_list = [chain_merging, seq_merging, plus_merging]
    # dict_list = []
    results = {func.__name__: [] for func in function_list}

    # 多进程生成多个字典
    with Progress() as progress:
        task = progress.add_task("[green]进行速度测试...", total=num_tests)
        # gen_task = progress.add_task("[cyan] - 生成测试数据...", total=num_tests)
        with Pool() as pool:
            args_list = [
                (
                    i,
                    dict_size,
                )
                for i in range(num_tests)
            ]

            # def disp_work():
            #     while gening_stst["NOWIDX"] < num_tests:
            #         progress.update(
            #             gen_task,
            #             advance=1,
            #             description=f"[cyan]正在生成 {gening_stst['DATA']['NOWIDX']}/{dict_size -1}",
            #             # description="正在生成..."+console._render_buffer(
            #             #         console.render(table,),
            #             # ),
            #         )

            # Process(target=disp_work).start()

            for result in pool.imap_unordered(generate_single_dict, args_list):
                # dict_list.append(result)
                progress.update(
                    task,
                    advance=1,
                    description=f"[cyan]正在测试 {result[0] + 1}/{num_tests}",
                    # description="正在生成..."+console._render_buffer(
                    #         console.render(table,),
                    # ),
                    # refresh=True,
                )

                # gening_stst["NOWIDX"] += 1

                # for _ in range(num_tests):
                # 随机选择字典和打乱函数顺序
                # current_dict = generate_single_dict((_, dict_size))
                # progress.update(
                #     test_task,
                #     advance=1,
                #     # description=f"[cyan]正在测试 {_}/{num_tests -1}",
                #     # description="正在测试..."+console._render_buffer(
                #     #         console.render(table,progress.console.options),
                #     # ),
                #     # refresh=True,
                # )

                # rangen_task = progress.add_task(
                #     "[green]正在生成测试数据...",
                #     total=dict_size,
                # )
                # current_dict = {}
                # desc = "正在生成序列 {}/{}".format("{}",dict_size-1)

                # for i in range(dict_size):
                #     # print("正在生成第", i, "个序列",end="\r",flush=True)
                #     progress.update(rangen_task, advance=1, description=desc.format(i))
                #     current_dict[i] = [random.randint(0, 1000) for _ in range(random.randint(10000, 99999))]

                shuffled_funcs = random.sample(function_list, len(function_list))
                # table.rows
                # table.columns = fine_column
                # progress.live
                # progress.console._buffer.extend(progress.console.render(table))
                # for j in progress.console.render(table,progress.console.options):
                #     progress.console._buffer.insert(0,j)

                for i, func in enumerate(shuffled_funcs):

                    start = time.perf_counter()
                    func(result[1])
                    elapsed = time.perf_counter() - start
                    results[func.__name__].append(elapsed)
            # gening_stst["NOWIDX"] = num_tests

    # fine_column = table.columns.copy()

    # for func in function_list:
    #     name = func.__name__

    #     table.add_row(
    #         name,
    #         f"-",
    #         f"-",
    #         f"-",
    #         f"-",
    #     )

    # # proc_pool = []

    # 测试执行部分（保持顺序执行）
    # with Progress() as progress:
    #     # progress.live.update(table, refresh=True)
    #     # progress.live.process_renderables([table],)
    #     # print([console._render_buffer(
    #     #                     console.render(table,),
    #     #             )])
    #     # progress.console._buffer.extend(progress.console.render(table))
    #     test_task = progress.add_task("[cyan]进行速度测试...", total=num_tests)

    # for _ in range(num_tests):
    #     # 随机选择字典和打乱函数顺序
    #     # current_dict = generate_single_dict((_, dict_size))
    #     progress.update(
    #         test_task,
    #         advance=1,
    #         description=f"[cyan]正在测试 {_}/{num_tests -1}",
    #         # description="正在测试..."+console._render_buffer(
    #         #         console.render(table,progress.console.options),
    #         # ),
    #         # refresh=True,
    #     )

    #     rangen_task = progress.add_task(
    #         "[green]正在生成测试数据...",
    #         total=dict_size,
    #     )
    #     current_dict = {}
    #     desc = "正在生成序列 {}/{}".format("{}",dict_size-1)

    #     for i in range(dict_size):
    #         # print("正在生成第", i, "个序列",end="\r",flush=True)
    #         progress.update(rangen_task, advance=1, description=desc.format(i))
    #         current_dict[i] = [random.randint(0, 1000) for _ in range(random.randint(10000, 99999))]

    #     shuffled_funcs = random.sample(function_list, len(function_list))
    #     # table.rows
    #     # table.columns = fine_column
    #     # progress.live
    #     # progress.console._buffer.extend(progress.console.render(table))
    #     # for j in progress.console.render(table,progress.console.options):
    #     #     progress.console._buffer.insert(0,j)

    #     for i, func in enumerate(shuffled_funcs):

    #         start = time.perf_counter()
    #         func(current_dict)
    #         elapsed = time.perf_counter() - start
    #         results[func.__name__].append(elapsed)

    # times = results[func.__name__]
    # avg_time = sum(times) / len(times)
    # min_time = min(times)
    # max_time = max(times)

    # table.columns[0]

    # table.columns[0]._cells[i] = func.__name__
    # table.columns[1]._cells[i] = f"{avg_time:.5f}"
    # table.columns[2]._cells[i] = f"{min_time:.5f}"
    # table.columns[3]._cells[i] = f"{max_time:.5f}"
    # table.columns[4]._cells[i] = str(len(times))

    # progress.update(test_task, advance=0.5)

    # 结果展示部分

    # 结果表格
    table = Table(title="\n[cyan]性能测试结果", show_header=True, header_style="bold")
    table.add_column("函数名称", style="dim", width=15)
    table.add_column("平均耗时 (秒)", justify="right")
    table.add_column("最小耗时 (秒)", justify="right")
    table.add_column("最大耗时 (秒)", justify="right")
    table.add_column("测试次数", justify="right")

    for i, func in enumerate(function_list):
        name = func.__name__
        times = results[name]
        avg_time = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)

        table.add_row(
            name,
            f"{avg_time:.5f}",
            f"{min_time:.5f}",
            f"{max_time:.5f}",
            str(len(times)),
        )
        # table.columns[0]._cells[i] = name
        # table.columns[1]._cells[i] = f"{avg_time:.5f}"
        # table.columns[2]._cells[i] = f"{min_time:.5f}"
        # table.columns[3]._cells[i] = f"{max_time:.5f}"
        # table.columns[4]._cells[i] = str(len(times))

    console.print(table)
