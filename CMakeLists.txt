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

# MSVC 严格遵循标准的编译选项
if (MSVC)
    add_compile_options(
        /permissive-
        /Zc:__cplusplus
        /Zc:include
        /Zc:throwingNew
        /Zc:referenceBinding
        /Zc:strictStrings
        /W4
    )
endif()

#add executable
add_executable(assert_test "DB vs RL/assert-review.cpp")
add_executable(hello_world "hello.cpp")
add_executable(test_ "test_c++_standard.cpp")
add_executable(conts_learn "conts learning/contslearn.cpp")