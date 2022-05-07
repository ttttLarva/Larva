# VS Code插件 Remote SSH


:earth_asia: **Bilibili视频传送门：** [远程开发C++001_Remote SSH](https://www.bilibili.com/video/BV1YT4y1d78B?spm_id_from=333.999.0.0) :earth_asia:

学习过如何使用ssh登录github后[github SSH免密码登录](https://www.ttlarva.com/master/github/03_SSH_for_github.html), 我们对ssh已经有了基础的了解,比如像腾讯云, 阿里云这样租用的服务器,我们都是可以通过ssh去登录.
远程开发C++这一系列内容将向大家展示如何通过ssh登录一个服务器.
首先,这期主要向大家介绍一款非常好用的VS Code插件: Remote SSH, 它可以让我们在远程服务器开发像在本地开发一样简单.

## 登录远程服务器
SSH的使用较简单, 如果已经在远程服务器上配置了密钥, 那就可以直接通过SSH去登陆远程服务器:
在控制台`ssh remote-21-ttlarva` (remote-21-ttlarva需改成使用的远程服务器ip地址)
在登上远程服务器之后, 就来到了一个linux系统下, 可以使用linux命令, 例如`ls` 和 `man ssh`.
不过只有一个命令行是不够方便的, 如果不熟悉vim这一类软件, 并且喜欢用键盘加鼠标的组合, 那么就需要VS Code的一个神奇插件了: Remote SSH.

Remote SSH插件底层是通过ssh协议的, 并且做了非常多贴心的开发和优化, 使得我们安装好这个插件并配置好ssh登录选项后就可以直接打开远程服务器上的目录并且就像操作本地一样. 更强大的是, VS Code有了这个插件后, VS code的其他插件都可以直接安装在远程服务器上,换言之, 这就让远程的开发更接近本地开发了.

## 安装Remote SSH
安装较为简单,和其他插件安装方式相同:
![Xnip2022-05-06_02-23-36.jpg](docs/remote_cpp_development/remote_ssh_files/Xnip2022-05-06_02-23-36.jpg)
安装完成之后,会发现左下角多了一个按钮:
![Xnip2022-05-06_09-41-38.jpg](docs/remote_cpp_development/remote_ssh_files/Xnip2022-05-06_09-41-38.jpg)
点击它,然后选择open configuration file:
![pic1.png](docs/remote_cpp_development/remote_ssh_files/pic1.png)
打开我们配置文件,就是`.ssh/config`

``` 
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
```
这里的Host名就是方便我们去记的名,而HostName就是ip地址, 做完一系列配置之后,我们就可以去连接到远程服务器了.

当安装好这个插件之后, 我们还会发现左边多了一个电脑一样的图标:
![pic2.png](docs/remote_cpp_development/remote_ssh_files/pic2.png)
我们可以点击Connect to Host in Current Window在当前的窗口:
![pic3.png](docs/remote_cpp_development/remote_ssh_files/pic3.png)
等到左下角不转圈时,就说明我们已经连接好了.我们打开一个终端试试,可以看到可以敲下linux下的命令了,这就说明已经在远程服务器上了.
![pic5.png](docs/remote_cpp_development/remote_ssh_files/pic5.png)

接着我们还可以使用VS Code去打开远程服务器上的文件夹目录了,点击目录:open folder
![pic6.png](docs/remote_cpp_development/remote_ssh_files/pic6.png)
看到当前的这个文件夹就是在远程服务器上的, 打开它, 点击ok:
![pic7.png](docs/remote_cpp_development/remote_ssh_files/pic7.png)
这样我们就打开了一个远程服务器上的一个oneflow仓库.

## 在远程服务器上安装插件:
在已经有Remote SSH能登录到远程服务器的基础上,我们可以在远程服务器上安装VS Code插件.
一开始打开一个CMake的文件,是没有高亮的,这是因为没有插件对它做语法解析.
如果我们现在想让他高亮起来,就需要安装插件:打开插件安装按钮,搜索cmake
![pic9.png](docs/remote_cpp_development/remote_ssh_files/pic9.png)
看到这个按钮,是提示我们可以安装在远程服务器上,点击它:
![Xnip2022-05-06_09-58-25.jpg](docs/remote_cpp_development/remote_ssh_files/Xnip2022-05-06_09-58-25.jpg)
再回过来看我们的CMake文件,就已经高亮了.

当我们点击到插件安装栏,会发现它有帮我们展示出local本地安装了哪些插件,远程服务器上安装了哪些插件,如果大家有发现在本地非常好用的插件,那么就可以安装到远程服务器上,点击install in SSH:remote,就可以在远程服务器上使用了.

在我们给VS Code安装了Remote SSH 插件后,我们可以让在远程服务器开发像在本地开发一样简单,也让远程服务器可以支持安装一系列的插件.