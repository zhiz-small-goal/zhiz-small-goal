#include <iostream>
#include <filesystem>

int main() {
    std::cout << "day01 ok" << std::endl;
    std::cout << std::filesystem::current_path() << std::endl;
    return 0;
}