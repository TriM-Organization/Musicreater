<h1 align="center">
    音·创 Musicreater
</h1>

<p align="center">
    <img width="128" height="128" src="https://gitee.com/TriM-Organization/Musicreater/raw/master/resources/msctIcon.ico">
    </img>
</p>

<h3 align="center">一款免费开源的《我的世界》数字音频转换库。</h3>

<p align="center">
    <img src="https://forthebadge.com/images/badges/built-with-love.svg">
    <a href='https://gitee.com/TriM-Organization/Musicreater'>
        <img align="right" src='https://gitee.com/TriM-Organization/Musicreater/widgets/widget_1.svg' alt='Fork me on Gitee'>
        </img>
    </a>
<p>

[![][Bilibili: 金羿ELS]](https://space.bilibili.com/397369002/)
[![][Bilibili: 诸葛亮与八卦阵]](https://space.bilibili.com/604072474)
[![CodeStyle: black]](https://github.com/psf/black)
[![][python]](https://www.python.org/)
[![][license]](LICENSE)
[![][release]](../../releases)

[![GiteeStar](https://gitee.com/TriM-Organization/Musicreater/badge/star.svg?theme=gray)](https://gitee.com/TriM-Organization/Musicreater/stargazers)
[![GiteeFork](https://gitee.com/TriM-Organization/Musicreater/badge/fork.svg?theme=gray)](https://gitee.com/TriM-Organization/Musicreater/members)
[![GitHub Repo stars](https://img.shields.io/github/stars/TriM-Organization/Musicreater?color=white&logo=GitHub&style=plastic)](https://github.com/TriM-Organization/Musicreater/stargazers)
[![GitHub Repo Forks](https://img.shields.io/github/forks/TriM-Organization/Musicreater?color=white&logo=GitHub&style=plastic)](https://github.com/TriM-Organization/Musicreater/forks)

简体中文 🇨🇳 | [English🇬🇧](README_EN.md)

## 介绍 🚀

音·创 是一个免费开源的针对 **《我的世界》** 的 MIDI 音乐转换库

欢迎加群：[861684859](https://jq.qq.com/?_wv=1027&k=hpeRxrYr)

## 安装 🔳

- 使用 pypi

  ```bash
  pip install Musicreater
  ```

- 如果出现错误，可以尝试：
  ```bash
  pip install -i https://pypi.python.org/simple Musicreater
  ```

- 升级：

  ```bash
  pip install -i https://pypi.python.org/simple Musicreater --upgrade
  ```

- 克隆仓库并安装
  ```bash
  git clone https://gitee.com/TriM-Organization/Musicreater.git
  cd Musicreater
  python setup.py install
  ```

以上命令中 `python`、`pip` 请依照各个环境不同灵活更换，可能为`python3`或`pip3`之类。

## 文档 📄

[生成文件的使用](./docs/%E7%94%9F%E6%88%90%E6%96%87%E4%BB%B6%E7%9A%84%E4%BD%BF%E7%94%A8%E8%AF%B4%E6%98%8E.md)

[仓库 API 文档](./docs/%E5%BA%93%E7%9A%84%E7%94%9F%E6%88%90%E4%B8%8E%E5%8A%9F%E8%83%BD%E6%96%87%E6%A1%A3.md)

## 作者 ✒

**金羿 Eilles**：我的世界基岩版指令师，个人开发者，B 站不知名 UP 主，江西在校高中生。

**诸葛亮与八卦阵 bgArray**：我的世界基岩版玩家，喜欢编程和音乐，深圳初二学生。

**偷吃不是Touch Touch**：我的世界基岩版指令师，提供 BDX 导入测试支持

## 致谢 🙏

本致谢列表排名无顺序。

- 感谢 **昀梦**\<QQ1515399885\> 找出指令生成错误 bug 并指正
- 感谢由 **Charlie_Ping “查理平”** 带来的 BDX 文件转换参考，以及 MIDI-我的世界对应乐器 参考表格
- 感谢由 **[CMA_2401PT](https://github.com/CMA2401PT)** 为我们的软件开发的一些方面进行指导，同时我们参考了他的 BDXworkshop 作为 BDX 结构编辑的参考
- 感谢由 **[Dislink Sforza](https://github.com/Dislink) “断联·斯福尔扎”**\<QQ1600515314\> 带来的 midi 音色解析以及转换指令的算法，我们将其改编并应用；同时，感谢他的[网页版转换器](https://dislink.github.io/midi2bdx/)给我们的开发与更新带来巨大的压力和动力，让我们在原本一骑绝尘的摸鱼道路上转向开发。
- 感谢 **Mono**\<QQ738893087\> 反馈安装时的问题，辅助我们找到了视窗操作系统下的兼容性问题；感谢其反馈延迟播放器出现的重大问题，让我们得以修改全部延迟播放错误；尤其感谢他对于我们的软件的大力宣传
- 感谢 **Ammelia “艾米利亚”**\<QQ2838334637\> 敦促我们进行新的功能开发，并为新功能提出了非常优秀的大量建议，以及提供的 BDX 导入测试支持，为我们的新结构生成算法提供了大量的实际理论支持
- 感谢 **[神羽](https://gitee.com/snowykami) “[SnowyKami](https://github.com/snowyfirefly)”** 对我们项目的支持与宣传，非常感谢他为我们提供的服务器！
- 感谢 **指令师\_苦力怕 playjuice123**\<QQ240667197\> 为我们的程序找出错误，并提醒我们修复一个一直存在的大 bug。
- 感谢 **雷霆**\<QQ3555268519\> 用他那令所有开发者都大为光火的操作方法为我们的程序找出错误，并提醒修复 bug。
- 感谢 **小埋**\<2039310975\> 反馈附加包生成时缺少描述和标题的问题。

>     感谢广大群友为此程序提供的测试等支持
>
>     若您对我们有所贡献但您的名字没有显示在此列表中，请联系我们！

## 联系 📞

若遇到库中的问题，欢迎在[此](https://gitee.com/TriM-Organization/Musicreater/issues/new)提出你的 issue。

如果需要与开发组进行交流，欢迎加入我们的[开发闲聊 Q 群](https://jq.qq.com/?_wv=1027&k=hpeRxrYr)。

亦可以联系我们[睿乐组织官方邮箱](mailto:TriM-Organization@hotmail.com)，取得进一步联系！

---

此项目并非一个官方 《我的世界》（_Minecraft_）项目

此项目不隶属或关联于 Mojang Studios 或 微软

此项目亦不隶属或关联于 网易

“Minecraft”是 Mojang Synergies AB 的商标，此项目中所有对于“我的世界”、“Minecraft”等相关称呼均为引用性使用

- 上文提及的 网易 公司，指代的是在中国大陆运营《我的世界：中国版》的上海网之易网络科技发展有限公司

NOT AN OFFICIAL MINECRAFT PRODUCT.

NOT APPROVED BY OR ASSOCIATED WITH MOJANG OR MICROSOFT.

NOT APPROVED BY OR ASSOCIATED WITH NETEASE.

[Bilibili: 金羿ELS]: https://img.shields.io/badge/Bilibili-%E5%87%8C%E4%BA%91%E9%87%91%E7%BE%BF-00A1E7?style=for-the-badge
[Bilibili: 诸葛亮与八卦阵]: https://img.shields.io/badge/Bilibili-%E8%AF%B8%E8%91%9B%E4%BA%AE%E4%B8%8E%E5%85%AB%E5%8D%A6%E9%98%B5-00A1E7?style=for-the-badge
[CodeStyle: black]: https://img.shields.io/badge/code%20style-black-121110.svg?style=for-the-badge
[python]: https://img.shields.io/badge/python-3.8-AB70FF?style=for-the-badge
[release]: https://img.shields.io/github/v/release/EillesWan/Musicreater?style=for-the-badge
[license]: https://img.shields.io/badge/Licence-Apache-228B22?style=for-the-badge
