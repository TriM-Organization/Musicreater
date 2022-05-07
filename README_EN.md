<h1 align="center">音·创 Musicreater</h1>

<p align="center">
<img width="128" height="128" src="https://s1.ax1x.com/2022/05/06/Ouhghj.md.png" >
</p>

<p align="center">
<img src="https://forthebadge.com/images/badges/built-with-love.svg">
<p>

[![][Bilibili: Eilles]](https://space.bilibili.com/397369002/)
[![][Bilibili: bgArray]](https://space.bilibili.com/604072474) 
[![CodeStyle: black]](https://github.com/psf/black)
![][python]
[![][license]](LICENSE)
[![][release]](../../releases)

[简体中文🇨🇳](README.md) | English🇬🇧


> Who has dropped political gunpowder into the technology
> 
> Who has dyed clear blue sky into the dark grey
> 
> All Chinese people love our great homeland
> 
> We *WILL* remember the remain pain of the humiliating history
> 
> We love the whole world but in peace
> 
> We love everyone but under respect
> 
> It is to be hoped that the war ends forever
> 
> Whatever it is cold or hot
> 
> Whatever it is economical or political
> 
> Just let the wonderful music of peace surround the world
> 
>                             ---- Eilles Wan
>                                  7/5 2022


**Notice that the language support of *README* may be a little SLOW.**

## Introduction🚀

Musicreater(音·创) is an free open source software which is used for making and also creating music in **Minecraft: Bedrock Edition**.

Welcome to join our QQ group: [861684859](https://jq.qq.com/?_wv=1027&k=hpeRxrYr)

### Authors✒

Eilles (金羿)：A high school student, individual developer, unfamous BilibiliUPer, which knows a little about commands in *Minecraft: Bedrock Edition*

bgArray "诸葛亮与八卦阵": Fix bugs, improve code aesthetics, add new functions, change data format, etc.

### Framework🏢

A simple Python package.

## Instructions📕

> comming soon.

### Instructions for **Customize Progress Bar**

We have supported the function of making progress bar in *Minecraft*'s music player. And also the method of customize them. So the following instructions are about the parameters of the Progress Bar Customizition.

A Progress Bar, of course, is composed of **changeless** parts and **changable** parts. And the changable parts include texts or *images*(these images are made up of texts, or we can say, character paintings 😁). That is, for *Minecraft*, a changable image in a progress bar is just the "bar" part(which is like a stripe).

We use a string to describe the style of progress bar you need, and it includes many **identifier**s to replace the changable parts.

There are the identifiers:

| Identifier   | Changable Part                                       |
|--------------|------------------------------------------------------|
| `%%N`        | Music name(file name which is imported into program) |
| `%%s`        | Value of scoreboard of now                           |
| `%^s`        | Max value of scoreboard                              |
| `%%t`        | Current playback time                                |
| `%^t`        | Total music time                                     |
| `%%%`        | Current playback progress                            |
| `_`          | To be replaced by the *Bar* part of the progress bar |

The `_` is a placeholder to identifying the *bar* part, yeah, just the changable image.

This is an example of **style description string**, and this is also the default style of *Musicreater*'s progress bar.

`▶ %%N [ %%s/%^s %%% __________ %%t|%^t]`

This is a progress bar with only one line, but it is possible if you want to give a multiline parameter into the style description string.

But the string above is only for style identification, but we also need to identifying the changable image's image(just what the bar's look).

A "bar", simply, included 2 parts: *Have Been Played* & *Not Been Played*. So we use a tuple to pass the parameter. It's under a simple format: `(str: played, str: not)`. For example, the default parameter is below:

`('§e=§r', '§7=§r')`

So it's time to combine what I said in one parameter now!

This is a default definder parameter:

`('▶ %%N [ %%s/%^s %%% __________ %%t|%^t]',('§e=§r', '§7=§r'))`

*Tip: To avoid errors, please not to use the identifiers as the other part of your style.*

## Thanks🙏

- Thank [Fuckcraft](https://github.com/fuckcraft) *(“鸣凤鸽子” ,etc)* for the function of Creating the Websocket Server for Minecraft: Bedrock Edition.
    -   *!! They have given me the rights to directly copy the lib into Musicreater*
- Thank *昀梦*\<QQ1515399885\> for finding and correcting the bugs in the commands that *Musicreater* Created.
- Thank *Charlie_Ping “查理平”* for bdx convert funtion.
- Thank *CMA_2401PT* for BDXWorkShop as the .bdx structure's operation guide.
- Thank *Miracle Plume “神羽”* \<QQshenyu40403\> for the Miracle Plume Bedrock Edition Audio Resource Pack
- 感谢由 Dislink Sforza \<QQ1600515314\>带来的midi转换算法，我们将其加入了我们众多算法之一
- Thank *Arthur Morgan* for his/her biggest support for the debugging of Musicreater
- Thanks for a lot of groupmates who support me and help me to test the program.
- If you have give me some help but u haven't been in the list, please contact me.

## Contact Information📞

### Author *Eilles*(金羿)

1.  QQ       2647547478
2.  E-mail   EillesWan2006@163.com W-YI_DoctorYI@outlook.com EillesWan@outlook.com
3.  WeChat   WYI_DoctorYI

### Author *bgArray*(诸葛亮与八卦阵)

1.  QQ       4740437765



[Bilibili: Eilles]: https://img.shields.io/badge/Bilibili-%E5%87%8C%E4%BA%91%E9%87%91%E7%BE%BF-00A1E7?style=for-the-badge
[Bilibili: bgArray]: https://img.shields.io/badge/Bilibili-%E8%AF%B8%E8%91%9B%E4%BA%AE%E4%B8%8E%E5%85%AB%E5%8D%A6%E9%98%B5-00A1E7?style=for-the-badge
[CodeStyle: black]: https://img.shields.io/badge/code%20style-black-121110.svg?style=for-the-badge
[python]: https://img.shields.io/badge/python-3.6-AB70FF?style=for-the-badge
[release]: https://img.shields.io/github/v/release/EillesWan/Musicreater?style=for-the-badge
[license]: https://img.shields.io/badge/Licence-Apache-228B22?style=for-the-badge