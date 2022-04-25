# 模板特例


:earth_asia: **Bilibili视频传送门：** [C++新标准009_模板特例](https://www.bilibili.com/video/BV1ea411v7Xa?spm_id_from=333.999.0.0) :earth_asia:

[上一篇文章](08_template.md)我们了解了模版，在此基础上，我们这期谈谈模板特例，包括三个主要内容：

- 泛型编程的特殊情况
- 偏特化
- 特化的应用

## 泛型编程的特殊情况

我们还是使用原来写过的MYMAX代码来作为例子：

```C++
#include <stdio.h>
#include <type_traits>
#include <string.h>


template <typename T>
T MYMAX(T x , T y){
    static_assert(std::is_integral<T>::value || std::is_floating_point<T>::value,
    "T must be  integral or floating point");
    return x<y ? y : x;
}

int main(int argc, char* argv[])
{
    printf("%d\n", MYMAX<int>(10, 5));
    printf("%1f\n", MYMAX<double>(3.14, 2.73));
    printf("%s\n", MYMAX("short string","very very long string"));
    return 0;
}
```

原来的代码做了静态检查，遇到输入是字符串时可以达到编译时就报错。这种做法其实是回避问题而不是解决问题，因此我们可以使用模版特例来解决：

```c++
template <typename T>
T MYMAX(T x , T y){
    static_assert(std::is_integral<T>::value || std::is_floating_point<T>::value,
    "T must be  integral or floating point");
    return x<y ? y : x;
}

template <>
const char* MYMAX(const char* x , const char* y){
    if (strlen(x) < strlen(y)) {
      return y;
    }
 		else {
      return x;
    }
}
```

这里我们增加了一个模版特化的MYMAX，有template关键字，但是没有参数。这个函数仅仅只针对`const char*`类型生效，函数内部的实现也是专门针对字符串的。其实就是针对某些模版参数进行了特化，编译器在实例化模版的过程中，会优先选择特化的模版，那模版特化的优点也是很明显的了。首先，从功能上来说，有类似虚函数那样“多态”的效果，我们对不同的数据调用的都是MYMAX，但是会自动选择不同的处理逻辑。其次，模版特化的性能更优，虚函数依赖的是运行时刷新虚表、查询虚表，而模板特化在编译时就完成了“分支的选择”，不占用运行时的资源，因此一般来说它的性能更优。 

## 偏特化

刚刚写的模版特化，template括号中是没有任何模版参数的，这种情况被称为“全特化”，其表示所有的模版参数都被特别指定了。与之对应的，对于类模版而言还有“偏特化”，表示只用特化部分模版参数。

```c++
#include <iostream>

using namespace std;

enum class DEVICE {
  CPU,
  GPU
};

template <DEVICE dev, typename IN_T1, typename IN_T2>
struct CExample {
  void operator()(IN_T1 a, IN_T2 b);
};

template <typename IN_T1, typename IN_T2>
struct CExample<DEVICE::CPU, IN_T1, IN_T2> {
  void operator()(IN_T1 a, IN_T2 b) {
    cout << "CPU template for: " << a << " " << b << endl;
  }
};

template <typename IN_T1, typename IN_T2>
struct CExample<DEVICE::GPU, IN_T1, IN_T2> {
  void operator()(IN_T1 a, IN_T2 b) {
    cout << "GPU template for: " << a << " " << b << endl;
  }
};

int main() {
  CExample<DEVICE::CPU, double, double>()(1.5, 2.4);
  CExample<DEVICE::GPU, int, int>()(4, 2);
  return 0;
}
```

这里实现了一个`CExample`的模版类，其有三个模版参数。然后我们实现两个模版类，分别对CPU和GPU的DEVICE进行偏特化。可以看到针对给定的不同“设备类型”，我们调用时使用的都是统一的接口，但是却触发了完全不同的运行流程。

## 特化的应用

通过上面的介绍，我们了解了模版的全特化和偏特化，接下来我们就从知名开源软件PyTorch和OneFlow来体会模版特化的用处。我们知道，工业级别的深度学习框架，无论是PyTorch还是OneFlow，都要去适配多种硬件，最常见的就是适配GPU和CPU。

### PyTorch的适配风格

PyTorch一般会针对CPU和GPU分别写一套独立的代码，接下来我们就以PyTorch的`eye`算子为例看看：

```c++
result.resize_({n, m});
result.zero_();

int64_t sz = std::min<int64_t>(n, m);
AT_DISPATCH_ALL_TYPES_AND_COMPLEX_AND2(at::ScalarType::Half, at::ScalarType::Bool, result.scalar_type(), "eye", [&]() -> void {
  scalar_t* result_data = result.data_ptr<scalar_t>();
  at::parallel_for(0, sz, internal::GRAIN_SIZE, [&](int64_t p_begin, int64_t p_end) {
    for (const auto i : c10::irange(p_begin, p_end))result_data[i*(result.strides()[0] + result.stride()[1])] = 1;
  });
});
```

上面是CPU版本的`eye`算子实现，而在GPU版本中：

```c++
result.resize_({n, m});
result.zero_();

int64_t sz = std::min<int64_t>(n, m);
int64_t stride = result.stride(0) + result.stride(1);

Tensor diag = result.as_strided({sz}, {stride});
diag.fill_(1);
```

PyTorch这种风格为每一种硬件都写一套kernel，这样代码清爽简洁，更容易让人看懂，但是可能会产生比较多的重复代码。

### OneFlow的适配风格

OneFlow中就运用了模版特例等技巧，把在适配硬件过程中可能会重复的代码降低到最少：

```c++
template<typename T>
OF_DEVICE_FUNC void SetOneInDiag(const int64_t cols, const int64_t rows, T* out) {
  const T one = static_cast<T>(1);
  XPU_1D_KERNEL_LOOP(i, rows) {
    const int64_t index = i * cols + i;
    out[index] = one;
  }
}
```

不管是CPU还是GPU用的都是同一份代码，不同设备的入口也是统一的。OneFlow针对不同的设备做了特化，把那些无法统一的代码都放到了特化的模版里。OneFlow这种风格代码更精炼，冗余度也更低，但是对C++的要求也更高了。