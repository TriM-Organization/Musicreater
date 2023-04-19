import shutil
import os


# find the full path of .egg-info folder
egg_info = [i for i in os.listdir() if i.endswith(".egg-info")][0]
print(egg_info)

# remove build, dist, logs, TrimLog.egg-info folders
try:
    shutil.rmtree("build")
except FileNotFoundError:
    pass

try:
    shutil.rmtree("dist")
except FileNotFoundError:
    pass

try:
    shutil.rmtree(egg_info)
except FileNotFoundError:
    pass

try:
    shutil.rmtree("logs")
except FileNotFoundError:
    pass

print("Cleaned up!")
