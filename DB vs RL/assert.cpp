#include <iostream>
#include <cassert>
#include <chrono>

int slow_function(int n) {
    int sum = 0;
    for (int i =0; i < n; ++i) {
        sum += i % 10;
    }
    return sum;
}

int main() {
    // 1, Debug 会出发断言， Release 会被优化掉
    int x = 1;
    assert( x >= 0 && "x must be non-negative");

    // 2, 性能测试
    auto start = std::chrono::high_resolution_clock::now();
    int result = slow_function(200);
    auto  end = std::chrono::high_resolution_clock::now();

    std::chrono::duration<double> elapsed = end -start;
    std::cout << "result = " << result << "\n";
    std::cout << "elapsed time = " << elapsed.count() << " seconds\n";
}