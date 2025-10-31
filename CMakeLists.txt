cmake_minimum_required(VERSION 3.20)
project(zhiz_cpp LANGUAGES C++)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(assert_test "DB vs RL/assert.cpp")

target_compile_options(assert_test PRIVATE
    $<$<CONFIG:Debug>:=g -o0>
    $<$<CONFIG:Release>:-o2 -DNDEBUG>
)