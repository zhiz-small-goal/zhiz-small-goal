#版本要求
cmake_minimum_required(VERSION 3.10)

#项目名称
project(zhiz_cpp
    DESCRIPTION "zhiz_cpp"
    VERSION 1.0.0
    LANGUAGES CXX
    )

#set c++标准
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)
set(CMAKE_CXX_EXTENSIONS OFF)

#add executable
add_executable(assert_test "DB vs RL/assert-review.cpp")