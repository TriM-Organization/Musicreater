
from time import sleep
from msctLib.buildIN import author_reader
from os import system

authors = author_reader()

def run(string):
    try:
        system(string)
    except:
        return

run('color 70')

for bigname,languages in authors.items():
    run('color 02') 
    for i in bigname:
        print(i,end="",flush=True)
        sleep(0.1)
    run('color 70')
    print(' :')
    for language,author in languages.items():
        line = '  '+language+' > '+author
        for i in line:
            print(i,end="",flush=True)
            sleep(0.05)
        print()

input()