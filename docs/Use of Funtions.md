<h1 align="center">音·创 Musicreater</h1>

<p align="center">
<img width="128" height="128" src="https://s1.ax1x.com/2022/05/06/Ouhghj.md.png" >
</p>


## Instructions📕

> 0. Install Python 3.6+
>	
>	While installing, be sure to check "add Python 3.X to path", otherwise it needs to be set manually
>    
>    After the installation, remember to enter in CMD: "python" to try
> 
>    whether the installation is successful.
> 
>    Python installation tutorial can be found on the Internet easily.
> 
> 1. Install (download this program)
> Git, you can use the following commands:
> 
> `git clone -b pkgver https://gitee.com/EillesWan/Musicreater.git`
> 
> If Git is not installed, you can download the zip package from the website. Then decompress it 
> and enter the directory.
> 
> 2. Run (enter directory)
> 
>  Open CMD in the directory, enter the directory, and execute the following commands:
> 
> `pip install mido`
> 
> `pip install brotli`
> 
> `pip install openpyxl`
> 
> 3. Start using!
> 
>  Open CMD in the directory, enter the directory, and execute the following commands:
> 
> (Choose what you need)
> 
> `python example_convert_bdx.py`
> 
> `python example_convert_mcpack.py`

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
