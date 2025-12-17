cmake_minimum_required(VERSION 3.24)
project(zhiz-small-goal LANGUAGES CXX)

add_executable(zhiz_tool app/main.cpp)
target_compile_features(zhiz_tool PRIVATE cxx_std_17)
set_property(TARGET zhiz_tool PROPERTY CXX_EXTENSIONS OFF)

option(ZHIZ_WARN_AS_ERROR "Treat warnings as errors" OFF)

if(MSVC)
    target_compile_options(zhiz_tool PRIVATE /W4)
    if(ZHIZ_WARN_AS_ERROR)
        target_compile_options(zhiz_tool PRIVATE /WX)
    endif()
endif()