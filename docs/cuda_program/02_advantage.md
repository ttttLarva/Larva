# CUDA编程02:让程序加速100倍！
:earth_asia: **Bilibili视频传送门：**[CUDA编程02：让程序加速100倍！](https://www.bilibili.com/video/BV1bF411s76k) :earth_asia:

本文通过具体的例子使读者理解CUDA的优势，为后续上手CUDA编程做好铺垫。

本文首先介绍了并行编程和串行编程的具体区别，然后介绍了CUDA异构编程的基本概念，最后展示了一个CUDA并行程序。

本文的结构如下：

- 并行编程VS串行编程
- CUDA异构编程的基本概念
- 完成一个CUDA并行程序


## 并行编程VS串行编程
在我们刚刚入门编程的时候，最熟悉的，很可能是串行编程，就是每次一行一行的执行代码。

以两个向量相加为例：

```c++
# 串行编程
void VectorAdd(int n, float *x, float *y)
{
    for(int i = 0; i < n; i++){
        y[i] = x[i] + y[i];
    }
}
```
这种方式就是串行的，一个个的去处理元素，从第零个，到第一个，直到最后一个元素处理完。

而在并行编程中，我们可以同时创建n个线程，每个线程只负责一个元素的计算，这样子，N个线程的运算是并发执行的，等所有线程都运行完，处理也就完成了。

GPU的硬件特点使得GPU创建多线程的开销远低于CPU，同时CUDA也通过扩展c++语法，方便我们同时创建多个线程。


## GPU是独立于CPU的外部设备
CUDA编程：Heterogeneous Programming，也就是异构编程。

异构：在本场景下指GPU和CPU，是两种独立的设备，在CUDA中使用host指代CPU，device指代GPU。

因为是相互独立的设备，所以内存空间也是相互独立的，在必要时，需要先进行拷贝才能使用。

而且host和device的机器码也不相同，因此，CUDA扩充了c++的语法关键字，所以需要使用CUDA提供的编译器nvcc。

![image](https://user-images.githubusercontent.com/63446546/158756870-269e4eb6-48e4-4cd6-ac79-b69499d22d9d.png)

以上是nvcc的编译过程，可以对其进行一个简单的理解：nvcc找出host和device代码，针对host代码采用原来的编译流程，例如gcc编译，对于device代码则编译成GPU指令。


## 实战CUDA编程-通过CUDA编写向量加法函数
首先实现一个cpu版本的串行向量加法
```c++
void VectorAdd(int n, float *x, float *y)
{
    for(int i = 0; i < n; i++){
        y[i] = x[i] + y[i];
    }
}

int main(int argc, char* argv[])
{
    int N = 1<<24; // 向量的长度 16,777,216
    float *x = nullptr;
    float *y = nullptr;
    
    // Allocate Unified Memory - accessible from CPU or GPU
	x = (float*)malloc(N*sizeof(float));
	y = (float*)malloc(N*sizeof(float));
	
	// Initialize x and y arrays on the host
	for (int i = 0; i < N; i++) {
		x[i] = 1.0f;
		y[i] = 2.0f;
	}
	
	double t1 = tick();
	VectorAdd(N, x, y);
	double t2 = tick();

	std::cout << "Completed in: " << t2 - t1 << " seconds" << std::endl;

	// Free memory
	free(x);
	free(y);

	return 0;
}
```

接下来看看CUDA版本：
```c++
#include <iostream>
#include <stdlib.h>
#include <sys/time.h>

double tick(){
	timeval time;
	gettimeofday(&time, nullptr);
	return time.tv_sec + time.tv_usec*1E-6;
}

// Kernel function to add the elements of two arrays
__global__
void VectorAdd(int n, float *x, float *y){
	int i = threadIdx.x + blockDim.x * blockIdx.x;
	if(i < n){
		y[i] = x[i] + y[i};
	}
}

int main(void)
{
    int N = 1<<24; //16,777,216
    float *x = nullptr;
    float *y = nullptr;
    
    // Allocate Unified Memory - accessible from CPU or GPU
	int mem_size = N*sizeof(float);
	x = (float*)malloc(mem_size);
	y = (float*)malloc(mem_size);
	
	// Initialize x and y arrays on the host
	for (int i = 0; i < N; i++) {
		x[i] = 1.0f;
		y[i] = 2.0f;
	}
	
	float *d_x = nullptr;
	float *d_y = nullptr;
	cudaMalloc(&d_x, mem_size);
	cudaMemcpy(d_x, x, mem_size, cudaMemcpyHostToDevice);
	cudaMalloc(&d_y, mem_size);
	cudaMemcpy(d_y, y, mem_size, cudaMemcpyHostToDevice);


	// Run kernel on 1M elements on the GPU
	double t1 = tick();
	VectorAdd<<<N/1024, 1024>>>(N, d_x, d_y);
	double t2 = tick();

	std::cout << "Completed in: " << t2 - t1 << " seconds" << std::endl;

	// Free memory
	cudaFree(d_x);
	cudaFree(d_y);

	return 0;
}
```

![image](https://user-images.githubusercontent.com/63446546/158760548-3d711cd4-5e55-48f3-bf15-f2e181bd25f4.png)
可以看到CUDA版本的性能约在cpu版本的100倍左右！所以学习CUDA编程是不是很有吸引力呢。

接下来就让我们一行一行的来解析代码吧！
### 内存转换

```c++
	cudaMalloc(&d_x, mem_size);
	cudaMemcpy(d_x, x, mem_size, cudaMemcpyHostToDevice);
	cudaMalloc(&d_y, mem_size);
	cudaMemcpy(d_y, y, mem_size, cudaMemcpyHostToDevice);

	// Free memory
	cudaFree(d_x);
	cudaFree(d_y);
```
之前我们提到，CPU和GPU的内存是不能进行共享的，那原有的`malloc`和`free`只能管理CPU的内存，所以为了管理GPU的内存，就需要使用到CUDA的API`cudaMalloc`，然后还需要调用`cudaMemcpy`把CPU上的内容拷贝到GPU上去，`cudaFree`则用来释放GPU内存。

### Kernel 函数
接着我们看看VectorAdd函数的实现。

```CUDA
__global__
```
`__global__`是使c++扩展到CUDA的关键字，被它修饰的函数，表示它是一个Kernel函数，也就是运行在device上的函数，并且是从host上调用的。换句话说，我们在CPU上调用Kernel函数时，就会启动GPU上的并发计算，类似关键字还有`__device__`, `__host__`。

这三个关键字的使用规则如下：

![image](https://user-images.githubusercontent.com/63446546/158762128-b27c9875-572c-4156-b88f-c774c3b37ef6.png)

当没有关键字修饰时，会默认在host上面执行，也保证了CUDA编程和c++编程是兼容的。

### 线程ID
继续来看`VectorAdd`函数的实现。
```c++
void VectorAdd(int n, float *x, float *y){
	int i = threadIdx.x + blockDim.x * blockIdx.x;
	if(i < n){
		y[i] = x[i] + y[i};
	}
}

```
会发现调用了`threadIdx`、`blockDim`、`blockIdx`，这是CUDA扩充的内置变量。这行代码会为每一个线程算出一个唯一索引 i ，然后每个线程根据这个唯一的 i ，处理一个元素，达到并发编程的目的。至于原理，请关注后续视频和博客。
### 启动Kernel
接下来看一下怎么调用Kernel函数的。
```c++
VectorAdd<<<N/1024, 1024>>>(N, d_x, d_y);
```
这是CUDA扩展的c++语法，```<<<>>>```是用来配置Kernel的启动时参数，关于它的语法，我们将在下个视频进行介绍。大家只要知道，因为这样配置，我们调用了很多线程进行并发编程。因此，他的效率也比CPU版本提高了不少。

后续的视频和博客会对本文中的内置变量和Kernel的启动细节进行详细的讲解。

# 参考文献
- [NVIDIA Corporation(Ed.)(2022). CUDA C++ Programming Guide.](https://docs.nvidia.com/cuda/pdf/CUDA_C_Programming_Guide.pdf)
- [Kirk, D. & Hwu, W.M.(2012). Programming Massively Parallel Processors:A Hands-on Approach. Elsevier Inc.](https://doi.org/10.1016/C2011-0-04129-7)
