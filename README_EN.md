[Bilibili: Eilles]: https://img.shields.io/badge/Bilibili-%E9%87%91%E7%BE%BFELS-00A1E7?style=for-the-badge
[Bilibili: bgArray]: https://img.shields.io/badge/Bilibili-%E8%AF%B8%E8%91%9B%E4%BA%AE%E4%B8%8E%E5%85%AB%E5%8D%A6%E9%98%B5-00A1E7?style=for-the-badge
[CodeStyle: black]: https://img.shields.io/badge/code%20style-black-121110.svg?style=for-the-badge
[python]: https://img.shields.io/badge/python-3.8-AB70FF?style=for-the-badge
[release]: https://img.shields.io/github/v/release/EillesWan/Musicreater?style=for-the-badge
[license]: https://img.shields.io/badge/Licence-%E6%B1%89%E9%92%B0%E5%BE%8B%E8%AE%B8%E5%8F%AF%E5%8D%8F%E8%AE%AE-228B22?style=for-the-badge

<h1 align="center">
    音·创 Musicreater
</h1>

<p align="center">
    <img width="128" height="128" src="https://s1.ax1x.com/2022/05/06/Ouhghj.md.png" >
    </img>
</p>

<h3 align="center">A free open-source library of <i>Minecraft</i> digital music.</h3>

<p align="center">
    <img src="https://img.shields.io/badge/BUILD%20WITH%20LOVE-FF3432?style=for-the-badge">
    </img>
<p>

[![][Bilibili: Eilles]](https://space.bilibili.com/397369002/)
[![][Bilibili: bgArray]](https://space.bilibili.com/604072474)
[![CodeStyle: black]](https://github.com/psf/black)
[![][python]](https://www.python.org/)
[![][license]](LICENSE)
[![][release]](../../releases)

[![GiteeStar](https://gitee.com/TriM-Organization/Musicreater/badge/star.svg?theme=gray)](https://gitee.com/TriM-Organization/Musicreater/stargazers)
[![GiteeFork](https://gitee.com/TriM-Organization/Musicreater/badge/fork.svg?theme=gray)](https://gitee.com/TriM-Organization/Musicreater/members)
[![GitHub Repo stars](https://img.shields.io/github/stars/TriM-Organization/Musicreater?color=white&logo=GitHub&style=plastic)](https://github.com/TriM-Organization/Musicreater/stargazers)
[![GitHub Repo Forks](https://img.shields.io/github/forks/TriM-Organization/Musicreater?color=white&logo=GitHub&style=plastic)](https://github.com/TriM-Organization/Musicreater/forks)

[简体中文 🇨🇳](README.md) | English🇬🇧

**Notice that the localizations of documents may NOT be up-to-date.**

## Introduction🚀

Musicreater is a free open-source library used for digital music that being played in _Minecraft_.

Welcome to join our QQ group: [861684859](https://jq.qq.com/?_wv=1027&k=hpeRxrYr)

## Installation 🔳

-   Via pypi

    ```bash
    pip install Musicreater --upgrade
    ```

-   If above command cannot fetch latest version, try:

    ```bash
    pip install -i https://pypi.python.org/simple Musicreater --upgrade
    ```

-   Clone repo and Install (Latest but **NOT RECOMMANDED**):
    ```bash
    git clone https://github.com/TriM-Organization/Musicreater.git
    cd Musicreater
    python setup.py install
    ```

Commands such as `python`、`pip` could be changed to some like `python3` or `pip3` according to the difference of platforms.

## Documentation 📄

(Not in English yet)

[生成文件的使用](./docs/%E7%94%9F%E6%88%90%E6%96%87%E4%BB%B6%E7%9A%84%E4%BD%BF%E7%94%A8%E8%AF%B4%E6%98%8E.md)

[仓库 API 文档](./docs/%E5%BA%93%E7%9A%84%E7%94%9F%E6%88%90%E4%B8%8E%E5%8A%9F%E8%83%BD%E6%96%87%E6%A1%A3.md)

### Authors ✒

**Eilles (金羿)**：A student, individual developer, unfamous Bilibili UPer, which knows a little about commands in _Minecraft: Bedrock Edition_

**bgArray (诸葛亮与八卦阵)**: A student, player of _Minecraft: Bedrock Edition_, which is a fan of music and programming.

**Touch (偷吃不是 Touch)**: A man who is good at using command(s) in _Minecraft: Bedrock Edition_, who supported us of debugging and testing program and algorithm

## Acknowledgements 🙏

This list is not in any order.

-   Thank _昀梦_\<QQ1515399885\> for finding and correcting the bugs in the commands that _Musicreater_ generated.
-   Thank _Charlie_Ping “查理平”_ for the bdx convert function for reference, and the reference chart that's used to convert the mid's instruments into Minecraft's instruments.
-   Thank _[CMA_2401PT](https://github.com/CMA2401PT)_ for BDXWorkShop for reference of the .bdx structure's operation, and his guidance in some aspects of our development.
-   Thank _[Dislink Sforza](https://github.com/Dislink) “断联·斯福尔扎”_ \<QQ1600515314\> for his midi analysis algorithm brought to us, we had adapted it and made it applied in one of our working method; Also, thank him for the [WebConvertor](https://dislink.github.io/midi2bdx/) which brought us so much pressure and power to develop as well as update our projects better, instead of loaf on our project.
-   Thank _Mono_\<QQ738893087\> for reporting problems while installing
-   Thank _Ammelia “艾米利亚”_\<QQ2838334637\> for urging us to develop new functions, and put forward a lot of excellent suggestions for new functions, as well as the BDX file's importing test support provided, which has given a lot of practical theoretical support for our new Structure Generating Algorithm
-   Thank _[神羽](https://gitee.com/snowykami) “[SnowyKami](https://github.com/snowyfirefly)”_ for supporting and promoting our project, and also thanks him for his server which given us to use for free.
-   Thank _指令师\_苦力怕 “playjuice123”_\<QQ240667197\> for finding bugs within our code, and noticed us to repair a big problem.
-   Thank _雷霆_\<QQ3555268519\> for his annoying and provoking operations which may awake some problems within the program by chance and reminding us to repair.
-   Thank _小埋_\<QQ2039310975\> for reporting the empty add-on packs title and description problem.
-   <table><tr><td>Thank <i>油炸</i> &lt;QQ2836146704&gt; for inspiring us to constantly develop something new.</td><td><img width="260" src="https://foruda.gitee.com/images/1695478907647543027/08ea9909_9911226.jpeg" alt="The groupmate on the picture was saying that our convert-QQ-bot had once brought him great convinience but now it closed down by some reason so he was feeling regretful." title="&quot;It was once, a convert-QQ-bot is just in front my eyes&quot;&#10;&quot;Until lose, I finally know cannot chase back what I needs&quot;"></td><td><small>&quot;It was once, a convert-QQ-bot is just in front my eyes&quot;<br>&quot;Until lose, I finally know cannot chase back what I needs&quot;</small></td></tr></table>
-   Thank _雨_\<QQ237667809\> for give us report that under the new `execute` command format that the scoreboard player's add-on packs cannot play correctly.
-   Thank _梦幻duang_\<QQ13753593\> for providing us with his knowlodeg of the command format in Minecraft: Java Edition Version 1.12.2.
-   Thank [_Open Note Block Studio_](https://github.com/OpenNBS/NoteBlockStudio)'s Project for giving us the power and energy of continual developing.

> Thanks for the support and help of a lot of groupmates  
> If you have given contributions but have not been in the list, please contact us!

## Contact Us 📞

Meet problems? Welcome to give out your issue [here](https://github.com/EillesWan/Musicreater/issues/new)!

Want to get in contact of developers? Welcome to join our [Chat QQ group](https://jq.qq.com/?_wv=1027&k=hpeRxrYr).

Or contact us via [TriM-Org Official Email](mailto:TriM-Organization@hotmail.com)!

---

NOT AN OFFICIAL MINECRAFT PRODUCT.

NOT APPROVED BY OR ASSOCIATED WITH MOJANG OR MICROSOFT.

NOT APPROVED BY OR ASSOCIATED WITH NETEASE.

此项目并非一个官方 《我的世界》（_Minecraft_）项目

此项目不隶属或关联于 Mojang Studios 或 微软

此项目亦不隶属或关联于 网易 相关

“Minecraft”是 Mojang Synergies AB 的商标，此项目中所有对于“我的世界”、“Minecraft”等相关称呼均为必要的介绍性使用

-   上文提及的 网易 公司，指代的是在中国大陆运营《我的世界：中国版》的上海网之易璀璨网络科技有限公司
