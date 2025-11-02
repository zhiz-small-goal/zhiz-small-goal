#pragma runtime_checks("", off)  // 关闭运行时检查
#pragma warning(disable: 4700)   // 禁用未初始化警告
#include <iostream>

int main() {
    std::cout << "=== 测试未初始化变量 ===\n\n";

    // 测试 1：未初始化的 int
    int uninit_int;
    std::cout << "未初始化的 int: " << uninit_int << "\n";

    // 测试 2：多次定义未初始化的变量
    int a;
    int b;
    int c;
    std::cout << "a = " << a << "\n";
    std::cout << "b = " << b << "\n";
    std::cout << "c = " << c << "\n\n";

    // 测试 3：对比初始化的变量
    int init_int = 0;
    std::cout << "初始化的 int: " << init_int << "\n\n";

    // 测试 4：未初始化的其他类型
    double uninit_double;
    bool uninit_bool;
    char uninit_char;

    std::cout << "未初始化的 double: " << uninit_double << "\n";
    std::cout << "未初始化的 bool: " << uninit_bool << "\n";
    std::cout << "未初始化的 char (as int): " << (int)uninit_char << "\n";

    return 0;
}