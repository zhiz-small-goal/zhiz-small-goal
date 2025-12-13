// docs: ./声明和定义.md

#include <iostream>
#include <windows.h>

// 在cards/声明和定义.cpp内定义一个叫add的函数
int add(int x, int y) {
    return x + y;
}
   

int main() {
    // 1) 设置控制台输出/输入代码页为 UTF-8
    SetConsoleOutputCP(CP_UTF8);
    SetConsoleCP(CP_UTF8);

    std::cout << "Hello from 声明和定义 (2025.12.08)" << std::endl;

    int a;   // 在main.cpp内声明一个叫a的变量
    class MyClass {}; // 在main.cpp内声明一个叫MyClass的类

    int add(int x, int y); // 在main.cpp内声明一个叫add的函数

    return 0;
}
