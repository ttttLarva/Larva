# using 关键字

简而言之， using 关键字可以定义类型别名（ type alias ）和别名模板（ alias template ）。为了让读者有更深入且符合直觉的理解，我们将先介绍函数指针，接着引出 typedef 关键字，最后谈到 using 的使用。

## 认识函数指针

回忆一下，在学习编程的初期，我们的常规操作是先定义函数，然后在合适的地方使用它的标识符（也就是用户定义的函数名）加上必要的参数进行调用，即：

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

一般来说，这就够了。不过，函数还有一个会令人感到惊讶的特性：它可以作为值被赋值，即：

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

我们会好奇，这个可以存储函数的变量究竟是什么类型的呢？毕竟，函数看起来不像是数字、字符、数组这样的数据，可以作为值被传递。我们使用 `typeid( ptr_myfun ).name()` 查看这个变量的类型，得到 `void (__cdecl*)(void)` ，这和我们熟悉的函数原型很相似，我们称其为函数指针类型。参照它来定义一个函数指针取代 auto 这个把底层细节封装地很好的关键字就有了思路了。

具体来说：首先获得函数原型 `void myfun()` ，接着把函数名改为用户自定义的变量名 `void ptr_myfun()` ，最后加上圆括号和星号 `void (*ptr_myfun)()` ，这样我们就定义好了一个函数指针变量。下边是具体的使用方法：

```c++
int main(int argc, char* argv[]) {
	void (*ptr_myfun)() = myfun;  // 显式地定义了函数指针
	ptr_myfun();
	std::cout << typeid(ptr_myfun).name() << std::endl;
	return 0;
}
```

思考一下，函数可以存储到函数指针变量中，这其实也是有道理的。从计算机系统底层的视角来看，函数就是一系列机器指令，那么函数调用其实就是把当前 cpu 的控制权移交给该函数对应的机器指令。自然而然，函数指针存储的就是这一系列指令的入口地址。

### 函数指针的应用与困惑

从上边的分析我们知道：函数指针可以被当成参数来传递，使得编程更加的灵活，这在[ STL ](https://github.com/microsoft/STL/blob/main/stl/src/cthread.cpp#L109)和各种框架中（如[ oneflow ](https://github.com/Oneflow-Inc/oneflow/blob/master/oneflow/core/intrusive/ref.h#L58)）都有广泛的应用，还催生出了 c++ 强大的 lambda 语法。

但是语法的奇特带来了问题，比如这个古老的系统调用signal的函数原型

> void ( \*signal(int signum, void (\*handler)(int)) ) (int);

显然这个函数原型可读性不高，面对高密度的此类代码无疑增添了我们的心智负担。不过，而后设计出的typedef 可以缓解这个问题。

## typedef 定义类型别名

基本语法为： `typedef 原类型 新别名`

它使得我们自定义原类型的新别名，让程序的可读性更好。我们通过 `man 2 signal` 来查看使用 typedef 后的 signal 函数原型：

```
NAME
       signal - ANSI C signal handling

SYNOPSIS
       #include <signal.h>

       typedef void (*sighandler_t)(int);  // 定义了参数为一个int，返回值为空的函数指针类型
       
       void ( *signal(int signum, void (*handler)(int)) ) (int);	// before
       sighandler_t signal(int signum, sighandler_t handler);  		// after，可读性更高
```

可以看到，这个语法还是稍显怪异，因为通常情况下我们的新别名出现在语句的最后，而论及函数指针时它却出现在了中间。为了消除这个“不优雅元素”，我们使用 C++11 推出的 using 关键字。

## using 定义类型别名

using 定义类型别名的语法为： `using 新别名=原类型`

```c++
// eg1
typedef void (*sighandler_t)(int);  // before
using sighandler_t = void(*)(int);  // after
// eg2
typedef std::string(Foo::* fooMemFnPtr) (const std::string&);  // before
using fooMemFnPtr = std::string(Foo::*) (const std::string&);  // after
```

很显然， using 强制把别名的名字分离到左边、把别名的指向放在右边的语法使代码可读性又上了一个台阶。

然而，对于一些同学来说，这不足以劝说他们使用 using 来取代 typedef 。所以，我们来介绍 using 的独特功能：模板别名（ alias template ）：

```c++
template<typename T>
typedef std::vector<T> myvec;  // 错误，编译得到“typedef 模板 非法”的错误提示

template<typename T>
using myvec = std::vector<T>;  // 可以通过编译
```

模板别名功能强大、应用广泛，在 [oneflow](https://github.com/Oneflow-Inc/oneflow/blob/master/oneflow/core/common/cfg.h#L30-L36) 中体现得很好：

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

## 总结

- 我们使用函数指针把函数作为值传递，增加了编程的灵活性
- 灵活的函数指针增大了理解代码的难度， typedef 通过自定义类型的别名对其加以缓解
- using 赋予了此类问题更好的解决方案

以上就是本次分享（[视频](https://www.bilibili.com/video/BV1Cq4y1A7Zk)）的全部内容，希望大家多多复习，在实战中掌握，这和我们后续要讲的仿函数、工厂模式都有密切的关系哦。
