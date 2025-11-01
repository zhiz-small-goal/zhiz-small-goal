1，cmake最低版本要求：cmake_minimum_required(VERSION 3.10)

2，项目名称：project(zhi_cpp
                VERSION 1.0.0 版本信息
                LAMGUAGE CXX
                DESCRIPTION "zhiz cpp learning")
            
3，设置c++标准
set(CMAKE_CXX_STANDARD c++17）
set(CMAKE_CXX_STANDARD_REQRUIRED ON)设置必须最低标准
set(CMake_CXX_EXCTENTIONS OFF) 设置禁用c++扩展

4，添加调试文件
add_executable(zhiz_cpp "zhiz_/assert.cpp) 第一个参数是生成的可执行文件名字，第二个是源文件路径

