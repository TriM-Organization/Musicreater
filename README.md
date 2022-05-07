<h1 align="center">音·创 Musicreater</h1>

<p align="center">
<img width="128" height="128" src="https://s1.ax1x.com/2022/05/06/Ouhghj.md.png" >
</p>

<p align="center">
<img src="https://forthebadge.com/images/badges/built-with-love.svg">
<p>

[![][Bilibili: 凌云金羿]](https://space.bilibili.com/397369002/)
[![][Bilibili: 诸葛亮与八卦阵]](https://space.bilibili.com/604072474) 
[![CodeStyle: black]](https://github.com/psf/black)
[![][python]](https://www.python.org/)
[![][license]](LICENSE)
[![][release]](../../releases)

简体中文🇨🇳 | [English🇬🇧](README_EN.md)


> 是谁把科技的领域布满政治的火药
> 
> 是谁把纯净的蓝天染上暗淡的沉灰
> 
> 中国人民无不热爱自己伟大的祖国
> 
> 我们不会忘记屈辱历史留下的惨痛
> 
> 我们希望世界和平
> 
> 我们希望获得世界的尊重
> 
> 愿世上再也没有战争
> 
> 无论是热还是冷
> 
> 无论是经济还是政治
> 
> 让美妙的和平的优雅的音乐响彻世界
> 
>           ——金羿
>             2022 5 7


## 介绍🚀

音·创 Musicreater 是一款免费开源的 **《我的世界：基岩版》** 音乐制作软件

音·创 pkgver (Musicreater Package Version) 是一款免费开源的 **《我的世界：基岩版》** 音乐转换库

欢迎加群：[861684859](https://jq.qq.com/?_wv=1027&k=hpeRxrYr)

**此分支为音·创的包版本，即便于其他软件使用的可被import版本**

## 软件作者✒

金羿 Eilles：我的世界基岩版指令师，个人开发者，B站不知名UP主，江西在校高中生。

诸葛亮与八卦阵 bgArray：我的世界基岩版玩家，喜欢编程和音乐，深圳初一学生。

## 软件架构🏢

这是一个简单的Python包

## 使用教程📕

> 正在到来

### 对于 进度条自定义 功能的说明

因为我们提供了可以自动转换进度条的功能，因此在这里给出进度条自定义参数的详细解释。

一个进度条，明显地，有**固定部分**和**可变部分**来构成。而可变部分又包括了文字和图形两种（当然，《我的世界》里头的进度条，可变的图形也就是那个“条”了）。这一点你需要了解，因为后文中包含了很多这方面的概念需要你了解。

进度条的自定义功能使用一个字符串来定义自己的样式，其中包含众多**标识符**来表示可变部分。

标识符如下（注意大小写）：

| 标识符   | 指定的可变量     |
|---------|----------------|
| `%%N`   | 乐曲名(即传入的文件名)|
| `%%s`   | 当前计分板值     |
| `%^s`   | 计分板最大值     |
| `%%t`   | 当前播放时间     |
| `%^t`   | 曲目总时长       |
| `%%%`   | 当前进度比率     |
| `_`     | 用以表示进度条占位|

表示进度条占位的 `_` 是用来标识你的进度条的。也就是可变部分的唯一的图形部分。

**样式定义字符串**的样例如下，这也是默认的进度条的样式：

`▶ %%N [ %%s/%^s %%% __________ %%t|%^t]`

这是单独一行的进度条，当然你也可以制作多行的，如果是一行的，输出时所使用的指令便是 `title`，而如果是多行的话，输出就会用 `titleraw` 作为进度条字幕。

哦对了，上面的只不过是样式定义，同时还需要定义的是可变图形的部分，也就是进度条上那个真正的“条”。

对于这个我们就采用了固定参数的方法，对于一个进度条，无非就是“已经播放过的”和“没播放过的”两种形态，所以，使用一个元组来传入这两个参数就是最简单的了。元组的格式也很简单：`(str: 播放过的部分长啥样, str: 没播放过的部分长啥样)` 。例如，我们默认的进度“条”的定义是这样的：

`('§e=§r', '§7=§r')`

综合起来，把这些参数传给函数需要一个参数整合，你猜用的啥？啊对对对，我用的还是元组！

我们的默认定义参数如下：

`(r'▶ %%N [ %%s/%^s %%% __________ %%t|%^t]',('§e=§r', '§7=§r'))`

*对了！为了避免生成错误，请尽量避免使用标识符作为定义样式字符串的其他部分*

## 致谢🙏

- 感谢 昀梦\<QQ1515399885\> 找出指令生成错误bug并指正
- 感谢由 Charlie_Ping “查理平” 带来的bdx文件转换参考
- 感谢由 CMA_2401PT 为我们的软件开发进行指导
- 感谢由 Dislink Sforza \<QQ1600515314\>带来的midi音色解析以及转换指令的算法，我们将其加入了我们众多算法之一
- 感谢广大群友为此程序提供的测试等支持
- 若您对我们有所贡献但您的名字没有显示在此列表中，请联系我！

## 联系我们📞

### 作者\<*金羿*\>(Eilles)联系方式

1.  QQ       2647547478
2.  电邮      EillesWan2006@163.com W-YI_DoctorYI@outlook.com EillesWan@outlook.com
3.  微信      WYI_DoctorYI

### 作者\<*诸葛亮与八卦阵*\>(bgArray) 联系方式

1.  QQ       4740437765



[Bilibili: 凌云金羿]: https://img.shields.io/badge/Bilibili-%E5%87%8C%E4%BA%91%E9%87%91%E7%BE%BF-00A1E7?style=for-the-badge
[Bilibili: 诸葛亮与八卦阵]: https://img.shields.io/badge/Bilibili-%E8%AF%B8%E8%91%9B%E4%BA%AE%E4%B8%8E%E5%85%AB%E5%8D%A6%E9%98%B5-00A1E7?style=for-the-badge
[CodeStyle: black]: https://img.shields.io/badge/code%20style-black-121110.svg?style=for-the-badge
[python]: https://img.shields.io/badge/python-3.6-AB70FF?style=for-the-badge
[release]: https://img.shields.io/github/v/release/EillesWan/Musicreater?style=for-the-badge
[license]: https://img.shields.io/badge/Licence-Apache-228B22?style=for-the-badge
