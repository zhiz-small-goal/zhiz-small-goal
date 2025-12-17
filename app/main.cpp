#include <iostream>
#include <filesystem>
#include <nlohmann/json.hpp>

int main() {
    std::cout << "day01 ok" << std::endl;
    std::cout << std::filesystem::current_path() << std::endl;
    std::cout << "枝枝宝最可爱" << std::endl;

    nlohmann::json j = {{"day", 3}, {"ok", true}};
    std::cout << j.dump() << "\n";
    return 0;
}