// WHAT: 一个命令行小程序，从标准输入读取一组整数，
//       调用 stats::summarize 计算统计信息并打印结果。

#include <iostream>
#include <vector>
#include <windows.h>

#include "stats.h"


// WHAT: 负责以只读方式打印统计结果。
// 参数使用 const 引用：表达“不会修改 summary”，并避免值传递的拷贝。
void print_summary(const stats::Summary& summary) {
    std::cout << "sum = " << summary.sum
              << ", avg = " << summary.avg
              << ", max = " << summary.max << '\n';
}

int main() {
    // 1) 设置控制台输出/输入代码页为 UTF-8
    SetConsoleOutputCP(CP_UTF8);
    SetConsoleCP(CP_UTF8);
    
    std::vector<int> data;

    std::cout << "请输入若干整数，以非数字结束输入: ";

    int value = 0;
    while (std::cin >> value) {
        data.push_back(value);
    }

    // WHY: 如果用户没有输入任何数据，提前返回并提示，
    //      而不是让 summarize 抛出异常终止程序。
    if (data.empty()) {
        std::cout << "未输入数据，程序结束。\n";
        return 0;
    }

    const auto summary = stats::summarize(data);  // WHY: const 表示后续不会再修改 summary
    print_summary(summary);

    return 0;
}
