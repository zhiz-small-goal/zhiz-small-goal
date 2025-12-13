# build
- `cmake -S . -B build`                  构建build目录
- `cmake --build build --config Debug`   构建Debug目录并在其目录下生成exe文件
- `.\build\Debug\zhiz_tool.exe`          启动可执行文件


# run
![run_result](image.png)

# Repo Layout: 
- /app：      放置主程序main.cpp（每个程序有并且有唯一入口）、说明文档、运行结果截图
- /docs：     放置细致天计划、今日计划Done_get
- /core:      核心源代码
- /scripts:   脚本目录