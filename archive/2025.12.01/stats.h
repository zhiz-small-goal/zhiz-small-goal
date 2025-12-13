// what:提供针对一组整数数据的基础统计功能：求和、平均值、最大值
// 这个头文件只暴露接口，不关系具体实现细节（how)

#pragma once

#include <vector>

namespace stats {

// what:表示一组整数数据的统计摘要
struct Summary {
    int sum;        // 总和
    double avg;    // 平均值
    int max;       // 最大值
};

// what:计算一组整数的总和/平均值/最大值
// 要求：
//   - data 非空，否则抛出std::invalid_argument异常
//   - 本函数不会修改调用方的数据（通过const引用表达这一点）
Summary summarize(const std::vector<int>& data);

} // namespace stats