cmake_minimum_required(VERSION 3.24)
project(zhiz-small-goal LANGUAGES CXX)

# -------------抓取第三方依赖-------------
include(FetchContent)

FetchContent_Declare(nlohmann_json
  URL      https://github.com/nlohmann/json/releases/download/v3.12.0/json.tar.xz
  URL_HASH SHA256=42f6e95cad6ec532fd372391373363b62a14af6d771056dbfc86160e6dfff7aa
)
FetchContent_MakeAvailable(nlohmann_json)


# -------------添加执行程序、限定目标使用c++17特性、禁用扩展------------------
add_executable(zhiz_tool app/main.cpp)
target_compile_features(zhiz_tool PRIVATE cxx_std_17)
set_property(TARGET zhiz_tool PROPERTY CXX_EXTENSIONS OFF)


# -------------安装规则：定义“交付目录树”---------------------
install(TARGETS zhiz_tool RUNTIME DESTINATION bin)    # 声明安装目标程序zhiz_tool，可执行文件安装到<prefix>/bin目录
install(FILES README.md LICENSE THIRD_PARTY_NOTICES.md DESTINATION .)     # 把文档、许可、notice也作为交付物安装到<prefix>/（包根目录）

#如果有配置、资源目录，用这个:整个目录拷贝进包
# install(DIRECTORY config/ BESTINATION config)


# ------------CPack：从 install 树打包 ------------
set(CPACK_PACKAGE_NAME "${PROJECT_NAME}")      # 包名
set(CPACK_PACKAGE_VERSION "${PROJECT_VERSION}")# 包版本
set(CPACK_GENERATOR "ZIP")                     # 默认生成zip（通用）
set(CPACK_PACKAGE_FILE_NAME
    "${PROJECT_NAME}-${PROJECT_VERSION}-${CMAKE_SYSTEM_NAME}-${CMAKE_SYSTEM_PROCESSOR}") # 13) 包文件名策略（可按需改）

# 添加SHA256校验
set(CPACK_PACKAGE_CHECKSUM "SHA256")

include(CPack)                              # 14) 生成 CPackConfig.cmake/CPackSourceConfig.cmake :contentReference[oaicite:9]{index=9}


# -------------添加日志库链接-----------------------
add_library(core_zhiz_log STATIC core/zhiz_log/logger.cpp)
target_compile_features(core_zhiz_log PUBLIC cxx_std_17)
set_property(TARGET core_zhiz_log PROPERTY CXX_EXTENSIONS OFF)

target_include_directories(core_zhiz_log PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})



target_link_libraries(zhiz_tool PRIVATE core_zhiz_log nlohmann_json::nlohmann_json)


target_link_libraries(zhiz_tool PRIVATE nlohmann_json::nlohmann_json)


# -------------设置自定义选项：warn是否是为错误-----------------
option(ZHIZ_WARN_AS_ERROR "Treat warnings as errors" OFF)

if(MSVC)
    target_compile_options(zhiz_tool PRIVATE /W4)
    if(ZHIZ_WARN_AS_ERROR)
        target_compile_options(zhiz_tool PRIVATE /WX)
    endif()
endif()