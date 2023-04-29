import shutil
import os
from rich.console import Console
from rich.progress import track

console = Console()


def main():
    with console.status("Find the full path of .egg-info folder"):
        egg_info: list = []
        for file in os.listdir():
            if os.path.isfile(file) and file.endswith(".egg-info"):
                egg_info.append(file)
                console.print(file)
    for file in track(["build", "dist", "logs", *egg_info], description="Deleting files"):
        if os.path.isdir(file) and os.access(file, os.W_OK):
            shutil.rmtree(file)


if __name__ == "__main__":
    main()
