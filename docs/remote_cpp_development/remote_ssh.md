# VS Code插件 Remote SSH


:earth_asia: **Bilibili视频传送门：** [远程开发C++001_Remote SSH] (https://www.bilibili.com/video/BV1YT4y1d78B?spm_id_from=333.999.0.0) :earth_asia:

学习过如何使用ssh登录github后[github SSH免密码登录](https://www.ttlarva.com/master/github/03_SSH_for_github.html), 我们对ssh已经有了基础的了解,比如像腾讯云, 阿里云这样租用的服务器,我们都是可以通过ssh去登录.
远程开发C++这一系列内容将向大家展示如何通过ssh登录一个服务器.
首先,这期主要向大家介绍一款非常好用的VS Code插件: Remote SSH, 它可以让我们在远程服务器开发像在本地开发一样简单.
![Xnip2022-05-06_02-23-36.jpg]

SSH的使用较简单, 如果已经在远程服务器上配置了密钥, 那就可以直接通过SSH去登陆远程服务器:
例如在控制台
ssh 远程服务器ip地址(remote-21-ttlarva)
在我们登上远程服务器之后, 我们就来到了一个linux系统下, 我们就可以使用linux命令
例如
ls
man ssh
不过只有一个命令行是不够方便的, 如果不熟悉vim这一类软件(可加图), 而是喜欢用键盘加鼠标的组合, 那么就需要VS Code的另一个神奇插件了: Remote SSH (可加图), Remote SSH插件底层还是通过ssh协议的, 不过这个插件做了非常多贴心的开发和优化, 使得我们安装好这个插件并配置好ssh登录选项后就可以直接打开远程服务器上的目录并且想操作本地一样, 更强大的是, VS Code有了这个插件后, VS code的其他插件都可以直接安装在远程服务器上,换言之, 这就让远程的开发更接近本地开发了

	0.	安装Remote SSH
安装较为简单,像其他插件一样

安装完成之后,会发现左下角多了一个按钮

点击它,然后open configuration file

打开我们配置文件,就是.ssh/config

‘‘‘ 
Host oneflow-15-ttlarva-remote
	Host name 182.18.94.166
	Port 1615
	User ttlarva
	IdentityFile E:\oneflow_ssh\id_rsa

Host remote-12-ttlarva
	Host name 192.168.1.41
	Port 20021
	User ttlarva
	IdentityFile E:\oneflow_ssh\id_rsa
	ProxyCommand C:\Windows\System32\OpenSSH\ssh.exe -q -x -W %h:%p oneflow-15-ttlarva-remote
	StrictHostKeyChecking no
‘‘‘ 
通过配置host,这个Host名就是方便我们去记的名
HostName就是ip地址, 做一系列配置之后,我们就可以去连接到远程服务器了

当安装好这个插件之后, 我们还会发现左边多了一个电脑一样的图标


我们可以点击Connect to Host in Current Window在当前的窗口

等到左下角不转圈时,就说明我们已经连接好了
那如何证明自己在远程服务器呢, 我们打开一个终端试试,可以看到可以敲一下linux下的命令了

接着我们还可以使用VS Code去打开远程服务器上的文件夹目录了,点击目录 open folder

看到当前的这个文件夹就是在远程服务器上的, 打开它, ok

这样我们就打开了一个远程服务器上的一个oneflow仓库

	0.	在远程服务器上安装插件:
如何在已经有Remote SSH能登录到远程服务器的基础上,如何在远程服务器上安装VS Code插件

大家可以看到,我现在打开了一个CMake的文件,现在是没有高亮的,因为没有插件对它做语法解析,现在想让他高亮起来
打开插件安装按钮,搜索cmake

看到一个按钮,提示我们可以安装在远程服务器上,点击它

再回过来看我们的CMake文件,就已经高亮了
再点击到插件安装栏看看,发现它有帮我们展示出local本地安装了哪些,远程服务器上安装了哪些


如果大家有发现在本地非常好用的插件,那么就可以安装到远程服务器上,比如以前推荐过的Git History Diff,点击,就可以在远程服务器上使用了

在我们给VS Code安装了Remote SSH 插件后,我们可以让在远程服务器开发像在本地开发一样简单,那么也让远程服务器能支持安装一系列的插件,后续教大家如何在远程服务器上配置clangd插件,让VS Code也像VS一样成为一个非常强大的IDE