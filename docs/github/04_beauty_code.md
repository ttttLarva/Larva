# 美化代码工具分享



:earth_asia: **Bilibili视频传送门：**[美化代码工具分享](https://www.bilibili.com/video/BV1iQ4y1X7xs?share_source=copy_web) :earth_asia:



本期视频和大家分享一下怎么让自己的代码变"漂亮"。

代码编程规范："华为C语言编程规范" 和 "微软一站式编码标准"



## 引入

在学习深度学习框架`OneFlow`时，我发现用命令

```
make of_format
```

就可以自动美化代码。所以就追溯了以上命令的实现，发现了black和clang-format这两个命令

## black和clang-format工具

**是什么**

* black 是python的一个第三方库，可以格式化python代码

* clang-format 是一个而精致文件，可以格式化C++、JAVA代码

**怎么用**

* black工具

  * 安装black工具

    ```
    pip insatll black
    ```

  * 使用方法

    ```
    python -m black 路径/文件名
    ```

    

* clang-format

  * 安装

    clang-format是LLVM工具集中的一款工具，我们可以通过安装LLVM获取。下载地址https://releases.llvm.org/

  * 使用方法

    ```
    clang-format 路径/文件名
    ```

    