# 类型别名

type alias 也就是using 别名=XXX

为了让大家更深入且符合直觉的理解，我们将先介绍函数指针，接着引出 typedef 关键字，最后谈到类型别名。

## 认识函数指针

回忆一下，我们在刚开始接触函数时，都是先定义函数，再使用它的标识符进行调用，即：

```c++
#include <iostream>

void myfun() {
	std::cout << "This function is called.\n" << std::endl;
}

int main(int argc, char* argv[]) {
	myfun();  // 常规的函数调用
	return 0;
}
```

其实，函数也是可以被赋值给变量的，然后这个变量就可以被调用，即：

```c++
#include <iostream>

void myfun() {
	std::cout << "This function is called.\n" << std::endl;
}

int main(int argc, char* argv[]) {
	auto ptr_myfun = myfun;  // 将函数作为值传递
	ptr_myfun();  // 运行效果与myfun()一致
	return 0;
}
```

于是大家开始好奇，这个可以存储函数的变量，到底是什么类型的呢？我们使用`typeid(ptr_myfun).name()`查看它的类型，得到`void (__cdecl*)(void)`，我们称其为函数指针。

那么如何定义函数指针呢？首先把函数原型复制下来`void myfun()`，接着把函数名改为变量名`void ptr_myfun()`，然后加上括号和星号`void (*ptr_myfun)()`，这样我们就定义了一个函数指针变量。

思考一下，函数可以存储到函数指针变量中，这其实也是有道理的。用计算机系统底层的视角来看，函数就是一系列机器指令，那么函数调用其实就是把cpu控制流跳转到该函数对应的指令的入口，自然而然，函数指针存储的就是这个入口的地址。

### 函数指针的应用与困惑

从上边的分析我们知道：函数指针可以被当成参数来传递，使得编程更加的灵活，这在[ STL ](https://github.com/microsoft/STL/blob/main/stl/src/cthread.cpp#L109)和各种框架中（如[ oneflow ](https://github.com/Oneflow-Inc/oneflow/blob/master/oneflow/core/intrusive/ref.h#L58)）都有广泛的应用，还催生出了 c++ 的 lambda 语法。

但是语法的奇特带来了问题，比如这个古老的系统调用signal的函数原型

#### void ( \*signal(int signum, void (\*handler)(int)) ) (int);

您能否快速地找到它的返回值类型和参数类型？看了半晌？看来这对我们阅读代码有些许障碍，它的可读性实在是太差了。

不过别担心，typedef 的设计就很好的缓解了我们阅读此类代码时的心智负担。

## typedef登场

typedef的语法为：`typedef 原类型 新别名`

它可以赋予基本数据类型更多的含义，可读性更好。因为signal早于 typedef 诞生，所以它可读性差了一些，不过后来有了 typedef 之后它好看的多了，我们通过` man 2 signal `来看看：

```
NAME
       signal - ANSI C signal handling

SYNOPSIS
       #include <signal.h>

       typedef void (*sighandler_t)(int);  // 定义了参数为一个int，返回值为空的函数指针类型
       
       sighandler_t signal(int signum, sighandler_t handler);  		// after，可读性更高
       void ( *signal(int signum, void (*handler)(int)) ) (int);	// before

DESCRIPTION
       The behavior of signal() varies across UNIX versions.
```

但是还是不要高兴的太早了，因为这里的语法还是有一丢丢怪异。因为通常情况下我们的新别名出现在语句的最后，而论及函数指针时它却出现在了中间。于是乎，为了消除这种“不和谐成员”，我们呼叫 using。

## using救场

using 不仅让我们使用名称空间，还可以定义别名。用法为：`using 新别名=原类型`

```c++
// eg1
typedef void (*sighandler_t)(int);  // before
using sighandler_t = void(*)(int);  // after
// eg2
typedef std::string(Foo::* fooMemFnPtr) (const std::string&);  // before
using fooMemFnPtr = std::string(Foo::*) (const std::string&);  // after
```

很显然，using 的写法强制把别名的名字分离到左边，而把别名的指向放在右边，这一设计使代码可读性上了一个台阶。然而，对于一些同学来说，这不是一个可以让他/她抛弃 typedef 而转投 using 的充分理由。于是乎，我们来介绍 using 的独特功能：模板别名（alias template）。直接上代码：

```c++
template<typename T>
typedef std::vector<T> myvec;  // nonono，编译得到“typedef 模板 非法”的错误提示

template<typename T>
using myvec = std::vector<T>;  // okay，可以通过编译
```

可别小看了模板别名，它的应用可是相当广泛，不信您来欣赏欣赏[ oneflow 的代码](https://github.com/Oneflow-Inc/oneflow/blob/master/oneflow/core/common/cfg.h#L30)：

```c++
template<typename T>
using CfgRf = ::oneflow::cfg::_RepeatedField_<T>;
template<typename T>
using CfgRpf = ::oneflow::cfg::_RepeatedField_<T>;
template<typename T1, typename T2>
using CfgMapPair = std::pair<T1, T2>;
template<typename K, typename V>
using CfgMap = ::oneflow::cfg::_MapField_<K, V>;
```

好了，这就是本次分享（[视频](https://www.bilibili.com/video/BV1Cq4y1A7Zk)）的全部内容了，希望大家课下多多复习，在实战中使用，这和我们后续要讲的仿函数、工厂模式都有关系哦。
