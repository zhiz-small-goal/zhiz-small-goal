#include <iostream>
#include <typeinfo>

int main() {
    auto g = 'H';

    std::cout << "=== 字符字面值类型测试 ===\n";
    std::cout << "auto g = 'H':\n";
    std::cout << "  g 的类型: " << typeid(g).name() << "\n";
    std::cout << "  sizeof(g): " << sizeof(g) << " 字节\n";
    std::cout << "  sizeof('H'): " << sizeof('H') << " 字节\n\n";

    // 直接测试字面值
    std::cout << "'H' 字面值:\n";
    std::cout << "  类型: " << typeid('H').name() << "\n";
    std::cout << "  大小: " << sizeof('H') << " 字节\n\n";

    // 对比不同类型
    std::cout << "=== 对比 ===\n";
    std::cout << "sizeof(char): " << sizeof(char) << " 字节\n";
    std::cout << "sizeof(int): " << sizeof(int) << " 字节\n";

    // 测试是否匹配
    if (sizeof('H') == sizeof(char)) {
        std::cout << "\n结论: 'H' 的大小等于 char (MSVC 行为)\n";
    }
    else if (sizeof('H') == sizeof(int)) {
        std::cout << "\n结论: 'H' 的大小等于 int (GCC/Clang 行为)\n";
    }

    return 0;
}