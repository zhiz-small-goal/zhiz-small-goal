# CMake 配置完全指南 - 手动编写版

## 🎯 基础配置（最小可用版本）

你需要手动写入这些内容到 `CMakeLists.txt`：

```cmake
cmake_minimum_required(VERSION 3.10)
project(SmallGoal VERSION 1.0)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)
add_executable(SmallGoal main.cpp)
```

---

## ❓ ON vs True 的区别

### **重要说明：在CMake中，它们是等价的！**

```cmake
# 这三种写法完全相同：
set(CMAKE_CXX_STANDARD_REQUIRED True)   ✅
set(CMAKE_CXX_STANDARD_REQUIRED ON)     ✅
set(CMAKE_CXX_STANDARD_REQUIRED YES)    ✅

# 关闭也有三种写法：
set(CMAKE_CXX_STANDARD_REQUIRED False)  ✅
set(CMAKE_CXX_STANDARD_REQUIRED OFF)    ✅
set(CMAKE_CXX_STANDARD_REQUIRED NO)     ✅
```

### **CMake布尔值对照表**

| 真值（True） | 假值（False） |
|:------------|:-------------|
| `ON` | `OFF` |
| `YES` | `NO` |
| `TRUE` | `FALSE` |
| `True` | `False` |
| `Y` | `N` |
| `1` | `0` |

**结论**：用哪个都可以，习惯问题！官方文档常用 `ON/OFF`，但 `True/False` 更直观。

---

## ⚠️ 常见混淆点

### **1. `CMAKE_CXX_STANDARD` ≠ 布尔值**

```cmake
# ❌ 错误写法：
set(CMAKE_CXX_STANDARD ON)      # 错误！这不是布尔值

# ✅ 正确写法：
set(CMAKE_CXX_STANDARD 17)      # 这是版本号
```

**解释**：
- `CMAKE_CXX_STANDARD` 接受的是**数字**（11, 14, 17, 20, 23）
- **不是** ON/OFF 或 True/False

---

### **2. 三个容易混淆的变量**

#### **变量1：`CMAKE_CXX_STANDARD`**（版本号，不是布尔）
```cmake
set(CMAKE_CXX_STANDARD 17)
```
- **作用**：设置C++标准版本
- **可选值**：`11`, `14`, `17`, `20`, `23`
- **类型**：数字，不是布尔值

#### **变量2：`CMAKE_CXX_STANDARD_REQUIRED`**（布尔值）
```cmake
set(CMAKE_CXX_STANDARD_REQUIRED ON)   # 或 True
```
- **作用**：是否强制要求指定的C++标准
- **可选值**：`ON/OFF`, `True/False`
- **类型**：布尔值

#### **变量3：`CMAKE_CXX_EXTENSIONS`**（布尔值）
```cmake
set(CMAKE_CXX_EXTENSIONS OFF)         # 或 False
```
- **作用**：是否启用编译器特定的扩展（如 GNU 扩展）
- **可选值**：`ON/OFF`, `True/False`
- **类型**：布尔值

---

## 📝 推荐的完整配置（手动编写）

### **方案一：简洁版（新手推荐）**

```cmake
# 第1行：CMake最低版本
cmake_minimum_required(VERSION 3.10)

# 第2行：项目名称和版本
project(SmallGoal VERSION 1.0)

# 第3行：C++标准版本（数字！）
set(CMAKE_CXX_STANDARD 17)

# 第4行：强制要求标准（布尔值）
set(CMAKE_CXX_STANDARD_REQUIRED True)

# 第5行：创建可执行文件
add_executable(SmallGoal main.cpp)
```

---

### **方案二：标准版（常用）**

```cmake
cmake_minimum_required(VERSION 3.10)

project(SmallGoal 
    VERSION 1.0
    DESCRIPTION "My Small Goal Project"
    LANGUAGES CXX
)

# C++设置
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)      # ON和True等价
set(CMAKE_CXX_EXTENSIONS OFF)            # 关闭编译器扩展

# 源文件
add_executable(SmallGoal main.cpp)
```

---

### **方案三：专业版（推荐）**

```cmake
cmake_minimum_required(VERSION 3.10)

project(SmallGoal 
    VERSION 1.0
    DESCRIPTION "My Small Goal Project"
    LANGUAGES CXX
)

# C++设置
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED TRUE)    # 三种写法都可以
set(CMAKE_CXX_EXTENSIONS OFF)

# 源文件列表（方便管理多个文件）
set(SOURCES
    main.cpp
    # 未来添加更多源文件在这里
)

# 创建可执行文件
add_executable(SmallGoal ${SOURCES})

# 设置包含目录（如果有头文件）
target_include_directories(SmallGoal 
    PRIVATE 
        ${CMAKE_CURRENT_SOURCE_DIR}/include
)
```

---

## 🔍 逐行详细说明

### **第1行：`cmake_minimum_required(VERSION 3.10)`**

```
含义：要求CMake版本至少为3.10
作用：确保用户的CMake版本足够新，支持所需功能
建议：3.10是最低要求，3.15+更好
```

---

### **第2行：`project(SmallGoal VERSION 1.0)`**

```
含义：定义项目名为SmallGoal，版本1.0
作用：设置项目元信息，生成变量 ${PROJECT_NAME}
建议：项目名用英文，不要有空格和特殊字符
```

**可选参数**：
- `VERSION 1.0` - 版本号
- `DESCRIPTION "描述"` - 项目描述
- `LANGUAGES CXX` - 使用C++语言

---

### **第3行：`set(CMAKE_CXX_STANDARD 17)`**

```
含义：使用C++17标准编译
作用：启用C++17的所有语言特性
注意：这里是数字17，不是ON/OFF！
```

**版本选择**：
- `11` - C++11（基础）
- `14` - C++14（改进）
- `17` - C++17（推荐） ⭐
- `20` - C++20（现代）
- `23` - C++23（最新）

---

### **第4行：`set(CMAKE_CXX_STANDARD_REQUIRED True)`**

```
含义：强制要求C++17，不支持就报错
作用：确保代码在所有平台用相同标准编译
等价写法：True / ON / YES / 1
```

**True vs False 的区别**：
- `True` → 编译器必须支持C++17，否则报错
- `False` → 编译器不支持就降级（可能用C++14或C++11）

**推荐**：设为 `True`，避免兼容性问题

---

### **第5行：`set(CMAKE_CXX_EXTENSIONS OFF)`**（可选）

```
含义：禁用编译器特定的扩展
作用：保证代码可移植，不依赖特定编译器
等价写法：OFF / False / NO / 0
```

**ON vs OFF 的区别**：
- `ON` → 允许使用 GNU 扩展（如 `__attribute__`）
- `OFF` → 只使用标准C++，代码更可移植 ⭐推荐

---

### **第6行：`add_executable(SmallGoal main.cpp)`**

```
含义：创建名为SmallGoal的可执行文件，从main.cpp编译
作用：定义编译目标
输出：SmallGoal.exe（Windows）或 SmallGoal（Linux/Mac）
```

**多文件版本**：
```cmake
add_executable(SmallGoal 
    main.cpp
    utils.cpp
    helper.cpp
)
```

---

## 🎨 使用变量管理源文件

### **为什么用变量？**
- 源文件多了好管理
- 修改方便，只改一处
- 代码更清晰

### **示例：**

```cmake
# 定义变量存储所有源文件
set(SOURCES
    main.cpp
    src/utils.cpp
    src/helper.cpp
)

# 使用变量
add_executable(SmallGoal ${SOURCES})
```

**说明**：
- `set()` 创建变量 `SOURCES`
- `${SOURCES}` 引用变量的值
- 相当于展开为：`main.cpp src/utils.cpp src/helper.cpp`

---

## 📁 推荐的项目结构

```
zhiz-small-goal/
├── CMakeLists.txt          ← 你要手动写的配置文件
├── main.cpp                ← 主程序（入口点）
├── include/                ← 头文件文件夹（可选）
│   └── utils.h
├── src/                    ← 源文件文件夹（可选）
│   └── utils.cpp
└── build/                  ← 构建输出（VS自动创建）
    └── SmallGoal.exe
```

---

## 🚀 VS 2022 使用流程

### **步骤1：手动创建文件**
1. 右键项目文件夹
2. 新建文本文件
3. 重命名为 `CMakeLists.txt`（注意大小写）
4. 手动输入配置内容

### **步骤2：打开项目**
```
VS 2022 → 文件 → 打开 → CMake
选择你的 CMakeLists.txt
```

### **步骤3：等待配置**
```
查看 输出窗口 → CMake 选项卡
等待显示 "配置完成"
```

### **步骤4：选择启动项**
```
工具栏下拉菜单 → 选择 "SmallGoal.exe"
```

### **步骤5：运行**
```
F5           - 调试运行
Ctrl+F5      - 直接运行
Ctrl+Shift+B - 仅编译
```

---

## ⚙️ 常用变量参考表

### **项目相关变量**

| 变量 | 含义 | 示例值 |
|:-----|:-----|:-------|
| `${PROJECT_NAME}` | 项目名 | `SmallGoal` |
| `${PROJECT_VERSION}` | 项目版本 | `1.0` |
| `${CMAKE_PROJECT_NAME}` | 顶级项目名 | `SmallGoal` |

### **路径相关变量**

| 变量 | 含义 | 示例值 |
|:-----|:-----|:-------|
| `${CMAKE_SOURCE_DIR}` | 根源码目录 | `D:/zhiz-c++/zhiz-small-goal` |
| `${CMAKE_BINARY_DIR}` | 构建输出目录 | `D:/zhiz-c++/zhiz-small-goal/out/build/x64-Debug` |
| `${CMAKE_CURRENT_SOURCE_DIR}` | 当前CMakeLists.txt所在目录 | 当前目录路径 |

### **编译器相关变量**

| 变量 | 含义 | 示例值 |
|:-----|:-----|:-------|
| `${CMAKE_CXX_COMPILER}` | C++编译器路径 | `cl.exe` 或 `g++` |
| `${CMAKE_BUILD_TYPE}` | 构建类型 | `Debug` 或 `Release` |

---

## 💡 常见问题

### **Q1：必须叫 CMakeLists.txt 吗？**
A：是的，CMake固定识别这个文件名，大小写敏感！

### **Q2：VERSION 1.0 可以省略吗？**
A：可以，这是可选的，只写 `project(SmallGoal)` 也行

### **Q3：C++17 和 C++20 选哪个？**
A：新手推荐C++17，稳定且广泛支持；高手可以用C++20

### **Q4：为什么有时候用 ON，有时候用 True？**
A：它们完全等价！用哪个看个人习惯，官方文档常用ON/OFF

### **Q5：REQUIRED 设为 False 会怎样？**
A：如果编译器不支持C++17，会自动降级到C++14或C++11

---

## 🎯 下一步

1. **手动创建** `CMakeLists.txt`，输入基础配置
2. **创建** `main.cpp`，写一个简单的 Hello World
3. **打开 VS 2022**，加载 CMake 项目
4. **按 F5** 运行看看效果

祝你配置顺利！🎉

