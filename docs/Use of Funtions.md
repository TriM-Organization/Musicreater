<h1 align="center">音·创 Musicreater</h1>

<p align="center">
<img width="128" height="128" src="https://s1.ax1x.com/2022/05/06/Ouhghj.md.png" >
</p>


# Instructions for Using Demo(s)

*This is a tutorial for using the demo(s) of this library, not the Development Guide.*

*Developing Documentation is now not translated yet, you can see here for the [Chinese Orignal Version](%E5%BA%93%E7%9A%84%E7%94%9F%E6%88%90%E4%B8%8E%E5%8A%9F%E8%83%BD%E6%96%87%E6%A1%A3.md) if you understand Chinese*

## Instructions of Downloading and Starting using Demo

### [Windows OS](./download%26start_EN/Windows.md)
### [Linux OS](./download%26start_EN/Linux.md)
### [Android OS](./download%26start_EN/Android.md)






2. More Info for Parameters of Our Demo Program(s)

	<img src=https://foruda.gitee.com/images/1659974810147043475/运行.png>

	|Input Prompt|English Translation|Description|
	|----------------|----------------|-------|
	|请输入MIDI文件路径|Midi File Path|Path of a .mid file or a directory. While directory entered, our demo will convert all midi(s) in the directory|
	|请输入输出路径|Output Path|Where files converted in|
	|是否重置计分板|Whether Reset Scoreboard Automatically|Can only be 1 or 0(Recommanded 1)|
	|*进度条[注]|Progressbar|Whether to enable Progressbar and customize progressbar style. Type 0 or False to disable, 1 or True to use default style, or type using format taught in follow the Instructions below to customize one you like|
	|请输入计分板名称|Scoreboard Name|*Only not byDelay* The name of scoreboard that player using|
	|请输入音量|Volume|Only decimal in [0,1],(Recommanded 1)|
	|请输入速度倍率|Speed Multiplying Factor|Maybe you want to play it faster(＞1) or slower(＞0 ＜1)?|
	|请输入玩家选择器|Player Selector|Full Selector including `@x`. E.g: Play for players tagged `Holo`, enter `@a[tag=Holo]` on this parameter|




# Instructions for **Customize Progress Bar**

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
