// how:通过一次性线性遍历完成所有统计，避免多次扫描数据

#include "stats.h"

#include <stdexcept>

namespace stats {

Summary summarize(const std::vector<int>& data) {
    if (data.empty()) {
        // why:空数据在本例视为逻辑错误，用异常而不是返回特殊值
        throw std::invalid_argument("data must not be empty");
    }

    Summary result{};
    result.sum = 0;
    result.max = data.front();

    //how:使用range-based for 在一次循环中完成累加与取最大值
    //    这是C++11引入的语法糖，能直接表达”对容器逐元素遍历“
    for (int value : data) {
        result.sum += value;

        if (value > result.max) {
            result.max = value;
        }
    }

    // why:强制转化为double再除，以获得最小精度而不是整数除法
    result.avg = static_cast<double>(result.sum) / data.size();

    return result;

}

}  // namespace stats