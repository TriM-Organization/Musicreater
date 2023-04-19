import shutil
import os


# find the full path of .egg-info folder
egg_info = [i for i in os.listdir() if i.endswith(".egg-info")][0]
print(egg_info)

# remove build, dist, logs, TrimLog.egg-info folders
shutil.rmtree("build")
shutil.rmtree("dist")
shutil.rmtree(egg_info)
shutil.rmtree("logs")

print("Cleaned up!")
