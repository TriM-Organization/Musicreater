import os
import pickle
# import tkinter.filedialog
# from namesConstant import zip_name
# from namesConstant import mcpack_name
import bgArrayLib.namesConstant
import shutil
zipN = bgArrayLib.namesConstant.zip_name
mpN = bgArrayLib.namesConstant.mcpack_name

manifest = {
  "format_version": 1,
  "header": {
    "name": "羽音缭绕-midiout_25.5--音创使用",
    "description": "羽音缭绕-midiout_25.0--音创使用",
    "uuid": "c1adbda4-3b3e-4e5b-a57e-cde8ac80ee19",
    "version": [25, 5, 0]
  },
  "modules": [
    {
      "description": "羽音缭绕-midiout_25.0--音创使用",
      "type": "resources",
      "uuid": "c13455d5-b9f3-47f2-9706-c05ad86b3180 ",
      "version": [25, 5, 0]
    }
  ]
}


def resources_pathSetting(newPath: str = ""):
    if not os.path.isfile("./bgArrayLib/resourcesPath.rpposi") and newPath == "":
        return [False, 1]  # 1:没有路径文件
    elif newPath != "":  # not os.path.isfile("./bgArrayLib/resourcesPath.rpposi") and
        path = newPath
        print(path)
        with open("./bgArrayLib/resourcesPath.rpposi", 'w') as w:
            w.write(path)
        if "mcpack(国际版推荐)格式_25.0" in os.listdir(path) and "zip格式_25.0" in os.listdir(path):
            return [True, path, 1]  # 1:都有
        elif "mcpack(国际版推荐)格式_25.0" in os.listdir(path) and "zip格式_25.0" not in os.listdir(path):
            return [True, path, 2]  # 2:有pack
        elif "mcpack(国际版推荐)格式_25.0" not in os.listdir(path) and "zip格式_25.0" in os.listdir(path):
            return [True, path, 3]  # 3:有zip
        else:
            return [False, 2]  # 2:路径文件指示错误
    if os.path.isfile("./bgArrayLib/resourcesPath.rpposi" and newPath == ""):
        with open("./bgArrayLib/resourcesPath.rpposi", 'r') as f:
            path = f.read()
        if "mcpack(国际版推荐)格式_25.0" in os.listdir(path) and "zip格式_25.0" in os.listdir(path):
            return [True, path, 1]  # 1:都有
        elif "mcpack(国际版推荐)格式_25.0" in os.listdir(path) and "zip格式_25.0" not in os.listdir(path):
            return [True, path, 2]  # 2:有pack
        elif "mcpack(国际版推荐)格式_25.0" not in os.listdir(path) and "zip格式_25.0" in os.listdir(path):
            return [True, path, 3]  # 3:有zip
        else:
            return [False, 2]  # 2:路径文件指示错误


def choose_resources():
    global zipN
    global mpN
    back_list = []
    try:
        with open(r"L:\0WorldMusicCreater-MFMS new edition\框架\v0.3.2\Musicreater\1.pkl", 'rb') as rb:
            instrument = list(pickle.load(rb))
        print(instrument)
    except FileNotFoundError:
        try:
            with open(r"L:\0WorldMusicCreater-MFMS new edition\框架\v0.3.2\Musicreater\nmcsup\1.pkl", 'rb') as rb:
                instrument = list(pickle.load(rb))
            print(instrument)
        except FileNotFoundError:
            return False
    path = resources_pathSetting()
    if path.__len__() == 2:
        return path
    else:
        dataT = path[2]
        pathT = path[1]
    if dataT == 1:
        if instrument[1] is True:
            index = zipN.get(-1)
            percussion_instrument = str(pathT) + "\\zip格式_25.0\\" + index
            # print(percussion_instrument)
            back_list.append(percussion_instrument)
        for i in instrument[0]:
            ins_p = str(pathT) + "\\zip格式_25.0\\" + str(zipN.get(i))
            # print(ins_p)
            back_list.append(ins_p)
        print(back_list)
        return back_list
    elif dataT == 2:
        if instrument[1] is True:
            index = mpN.get(-1)
            percussion_instrument = str(pathT) + "\\mcpack(国际版推荐)格式_25.0\\" + index
            # print(percussion_instrument)
            back_list.append(percussion_instrument)
        for i in instrument[0]:
            ins_p = str(pathT) + "\\mcpack(国际版推荐)格式_25.0\\" + str(mpN.get(i))
            # print(ins_p)
            back_list.append(ins_p)
        print(back_list)
        return back_list
    elif dataT == 3:
        if instrument[1] is True:
            index = zipN.get(-1)
            percussion_instrument = str(pathT) + "\\zip格式_25.0\\" + index
            # print(percussion_instrument)
            back_list.append(percussion_instrument)
        for i in instrument[0]:
            ins_p = str(pathT) + "\\zip格式_25.0\\" + str(zipN.get(i))
            # print(ins_p)
            back_list.append(ins_p)
        print(back_list)
        return back_list


def scatteredPack(path):
    pack_list = choose_resources()
    print(pack_list)
    print(path)
    # os.close("L:/0WorldMusicCreater-MFMS new edition")
    # shutil.copy("L:\\shenyu\\音源的资源包\\羽音缭绕-midiout_25.0\\mcpack(国际版推荐)格式_25.0\\0.Acoustic_Grand_Piano_大钢琴.mcpack",
    #                 "L:/0WorldMusicCreater-MFMS new edition")
    for i in pack_list:
        shutil.copy(i, path)


if __name__ == '__main__':
    # print(resources_pathSetting(r"L:\shenyu\音源的资源包\羽音缭绕-midiout_25.0"))
    choose_resources()
