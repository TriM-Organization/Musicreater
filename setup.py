# -*- coding: utf-8 -*-
import setuptools
import os
from Musicreater import __version__

os.chdir(os.path.dirname(os.path.abspath(__file__)))

with open("./requirements.txt", "r", encoding="utf-8") as fh:
    dependences = fh.read().strip().split("\n")

with open("./README_EN.md", "r", encoding="utf-8") as fh:
    long_description = fh.read().replace(
        "./docs/", "https://github.com/TriM-Organization/Musicreater/blob/master/docs/"
    )

setuptools.setup(
    name="Musicreater",
    version=__version__,
    author="金羿Eilles, bgArray, 鱼旧梦ElapsingDreams",
    author_email="TriM-Organization@hotmail.com",
    description="A free open source library used for dealing with **Minecraft** digital musics.\n一款开源《我的世界》数字音频支持库。",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TriM-Organization/Musicreater",
    packages=setuptools.find_packages(),
    classifiers=[
        "Intended Audience :: Developers",
        "Natural Language :: Chinese (Simplified)",
        # "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Multimedia",
        "Topic :: Multimedia :: Sound/Audio :: MIDI",
    ],
    # 需要安装的依赖
    install_requires=dependences,
    python_requires=">=3.8",
)
