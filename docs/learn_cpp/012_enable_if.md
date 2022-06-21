# 新标准：enable_if
:earth_asia: **Bilibili视频传送门：**[C++新标准012  enable_if](https://www.bilibili.com/video/BV1Tv4y1N73A?spm_id_from=333.999.0.0&vd_source=0184d13a7c21515c19c1cdb9230751c8) :earth_asia:

[上一期视频](https://www.bilibili.com/video/BV1yr4y1t7qo?spm_id_from=333.999.0.0&vd_source=0184d13a7c21515c19c1cdb9230751c8)我们介绍了SFINAE原则，在此基础上，本篇文章将继续介绍了enable_if新标准，为后续深入学习模板元编程打下基础。

本文的结构如下：
- 为什么要使用enable_if新标准？
- enable_if&is_same的使用
- enable_if&is_same内部的实现原理


## 为什么要使用enable_if新标准？
C++模板函数重载依赖于 SFINAE (substitution-failure-is-not-an-error) 原则，即替换失败不认为是错误，编译器将会继续寻找合适的重载函数；以上一期视频中返回长度的函数为例，该函数针对STL中的vector容器来实现（容器中有size()成员函数）

```c++
#SFINAE原则的应用
class CMyclass
{
public:
    using size_type = unsigned int;
};

template <typename T>
decltype(T().size(), typename T::size_type()) len(T const &t) //该函数可以避免匹配到CMyclass类
{
    return t.size();
}
unsigned len(...)
{
    return 0;
}

int main()
{
    vector<int>vec={1,2,3};
    cout<<len(vec)<<endl;  //调用针对stl库容器的len函数
    cout << len(CMyclass()) << endl; //调用len(...)函数
}
```
上期视频已经介绍了重载函数如何实现避免匹配到CMyclass类，这种编程技巧需要程序员根据特例类不存在的方法制因此造“错误”,并不通用；

因此C++11采用了具有通用性的enable_if新标准来实现SFINAE；我们根据上期视频给出的测试程序，将重载函数的形式改写成使用enable_if的形式
```c++
#enable_if的应用
class CMyclass
{
public:
    using size_type = unsigned int;
};

// template <typename T>   //上期视频采用的编程技巧
// decltype(T().size(), typename T::size_type()) len(T const &t)
// {
//     return t.size();
// }

template <typename T, typename T2 = typename enable_if<!is_same<T, CMyclass>::value>::type> //enable_if形式
typename T::size_type len(T const &t)
{
    return t.size();
}

unsigned len(...)
{
    return 0;
}

int main()
{
    vector<int> vec = {1, 2, 3};
    cout << len(vec) << endl;
    cout << len(CMyclass()) << endl;
}
```
该程序的输出结果与上期视频的程序一致，说明采用enable_if也可以实现重载函数避免匹配到特例类的功能。

不同的地方在于，enable_if可以避免匹配到CMyclass这个类，而注释的程序是避免匹配到不包含size()成员函数的类

##  enable_if&is_same的使用
### 1.enable_if的使用
首先给出enable_if的基本形式
```c++
	template<bool B,typename T=void>struct enable_if
```
- 当传入的模板参数B为True的时候，enable_if模板类的type就等于T；如果不传入模板参数T，type也会默认为void
- 当传入的模板参数B为False的时候，enable_if模板类就不再拥有type。

因此使用enable_if时可以让重载函数自由丢弃不需要匹配的特例类；下面给出实际应用的例子

```c++
#判断类型字节数是否大于4 输出显示
template <typename T>
typename std::enable_if<(sizeof(T) <= 4)>::type show() //针对T的长度小于等于4的情况生效
{
    printf("size<=4\n");
}

template <typename T>
typename std::enable_if<(sizeof(T) > 4)>::type show()  //针对T的长度大于4的情况生效
{
    printf("size>4\n");
}

int main()
{
    show<double>();
    show<char>();
}
```
输出结果为
```c++
size>4
size<=4
```


### 2.is_same的使用
首先给出is_same的基本形式
```c++
	template<class T,class U>struct is_same
```
- 当T==U时， is_same<T,U>模板类的成员value等于True
- 当T==U时， is_same<T,U>模板类的成员value等于False



## enable_if&is_same内部的实现原理

了解这两个模板类的内部实现原理之前，需要了解type traits的概念

### 1.什么是type traits?
 traits是c++模板编程中使用的一种技术，主要功能： 
  把功能相同而参数不同的函数抽象出来，通过traits将不同的参数的相同属性提取出来，在函数中利用这些用traits提取的属性，使得函数对不同的参数表现一致。

### 2.enable_if源码解析
下面给出enable_if的源码
```c++
  template<bool, typename _Tp = void>
    struct enable_if
    { };

  template<typename _Tp>
    struct enable_if<true, _Tp>
    { typedef _Tp type; };
```
- 首先定义了一个空的通用模板，不包含任何成员
- 当第一个模板参数值为true时，将模板特例化，定义type；其中type的类型为第二个模板参数_Tp。

### 3.is_same源码解析
以下代码简单实现了is_same模板类的作用
```c++
template <typename T,typename U>
struct my_is_same
{
    static constexpr bool value=false;
};

template <typename T>
struct my_is_same
{
    static constexpr bool value=true;
};
```
- 定义一个通用模板，针对两个模板参数类型不一致的情况，默认value值为False。
- 模板特例化，针对两个模板参数类型一致的情况，将value值设置为true。


#### is_same&enable_if的基本实现方案可以总结为：通用模板加模板实例化。


## 总结
- enable_If是通用的避免重载函数匹配到特例类的解决方案,使用简单而且更加自由。
- is_same&enable_if是type traits技术的典型应用,实现函数对不同参数表现一致的功能。
- is_same&enable_if的源码实现采用了模板元编程的基本实现思想，大致分为通用模板与模板特例化。