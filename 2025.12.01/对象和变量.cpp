#include <iostream>
#include <windows.h>

int main() {
    // 1) 设置控制台输出/输入代码页为 UTF-8
    SetConsoleOutputCP(CP_UTF8);
    SetConsoleCP(CP_UTF8);

    std::cout << "Hello from 对象和变量 (2025.12.01)" << std::endl;

    // 1,栈上的2个对象，对应2个变量名 x 和 y
    int x = 10;    // 对象：一块int类型的内存（在RAM中）
                   // 变量名：x
                   // 值：10
    int y = x + 1; // 另一个对象，初始值为11
    
    // 2，引用：不创建新对象，只给x那块内存多一个名字rx
    int& rx = x;   // &rx and &x are the same address

    // 3,指针：本身也是一个对象，类型是int*，值是【某个地址】
    int* px = &x;   // p is a pointer variable, its value is the address of x

    // 4,动态分配：在对上创建了一个没有直接名字的int对象
    int* heapPtr = new int(77); // 对象：堆上的那块内存区域
                                // 变量名：heapPtr（指针对象）
                                // 值：那个堆对象的地址

    std::cout << "x = " << x << ", &x = " << &x << std::endl;
    std::cout << "y = " << y << ", &y = " << &y << std::endl;
    std:: cout << "rx = " << rx << ", &rx = " << &rx << std::endl;
    std::cout << "px = " << px << ", &px = " << &px << std::endl;
    std::cout << "*px = " << *px << std::endl;
    std::cout << "heapPtr = " << heapPtr << ", *heapPtr = " << *heapPtr << std::endl;

    // 通过引用和指针修改【同一对象】的值
    rx = 100;    //等价于x = 100；
    *px = 200;   // 修改的仍是 x 这个对象
    std::cout << "After rx=100, *px=200:" << std::endl;
    std::cout << "x = " << x << std::endl;
    std::cout << "rx = " << rx << std::endl;

    // 修改y和堆上的对象，证明他们不是同一个对象
    y = 300;
    *heapPtr = 520;
    std::cout << "y = " << y << std::endl;
    std::cout << "*heapPtr = " << *heapPtr << std::endl;

    // 释放堆内存
    delete heapPtr;

    return 0;
}
