#### Day01（基线：目标、结构、最小可运行）
- A：写清“阶段 0 DoD”，并把 Day01–Day10 的日计划贴到 `docs/`（减少临时决策）
- B：创建仓库结构（`/app /core /docs /scripts`），写一个 **可编译可运行** 的最小程序（先 Console/WinMain 二选一）
- C：补 `README.md` 的最小段落：构建命令、运行截图、目录说明

#### Day02（工具链：CMake/编译器/格式化）
- A：确定本阶段编译器（MSVC / clang-cl）与 C++ 版本（建议 C++17），确定是否启用 `/W4 /WX`
- B：把 CMake 跑通（Debug/Release），VSCode 的 CMake Tools 配好；确保“干净目录重建”可过
- C：落地 `clang-format`（或等价格式化工具）与最小 `.editorconfig`，并写进 `CONTRIBUTING.md`

#### Day03（依赖与许可证：为后续模块铺路）
- A：决定依赖策略：**零依赖**（自己实现 minimal） / **少量 header-only**（nlohmann/json 等）
- B：落地一个最小依赖（建议先 `nlohmann/json` 或 `fmt` 二选一），确保构建系统能稳定拉起
- C：补 `LICENSE` 与 `THIRD_PARTY_NOTICES.md`（即使目前只有 1 个依赖，也先搭骨架）

#### Day04（core 边界：日志模块 v0）
- A：定义 `/core/log` 的最小接口（例如 `log_info/log_error` 或 `ILogger`），写 DoD：能写到文件且可定位路径
- B：实现 **最小文件日志**（时间戳 + level + message），并在 `/app` 调用一次
- C：写 `docs/logging.md`：日志位置、如何开启 debug、如何提交日志

#### Day05（打包：zip 脚本 + 发布清单 v0）
- A：写“发布清单 DoD”：zip 内应包含哪些文件（exe/config 示例/README/许可证），以及版本号规则
- B：实现 `scripts/package.ps1`：一键产出 zip（带版本号目录）
- C：建立 `docs/release_checklist.md`（本机复测清单 + 双机复测清单）并在机器 A 跑 1 次

#### Day06（CI：push 即构建）
- A：定义 CI 的最小目标：push 就能编译 + 产物保存（artifact），失败就阻断
- B：写 GitHub Actions：Windows Runner 编译 Debug/Release（二选一也可，先保最小）
- C：把 CI badge 加到 README，并写 `docs/ci.md`（失败排查入口）

#### Day07（Release 自动化：tag 产出 zip 附件）
- A：定义“Release 触发条件”：打 tag（例如 `v0.0.x`）即生成 zip 并上传 Release 附件
- B：扩展 Actions：tag → package → upload release asset（先用 GitHub Release 自动化即可）
- C：做一次 **演练发布**（draft release），验证附件能被下载并可运行

#### Day08（需求雷达 Session #1：收集而不评判）
- A：写 `docs/problem_db.md` 模板（字段：场景/替代方案/频率/代价/可验证行为/链接）
- B：做 30min 雷达：从 1–2 个公开社区/论坛抓 10 条“抱怨/卡点/反复问的问题”
- C：把 10 条整理进问题库（只记录事实与链接，不下结论）

#### Day09（需求雷达 Session #2：聚类 + 粗评分）
- A：定义粗评分标准（例如：频率 1–5、代价 1–5、替代方案成熟度 1–5）
- B：再收集 10 条，合并去重；对 Top 10 做粗评分并聚类（3–5 类）
- C：把聚类结果写成 1 页 `docs/problem_summary_week2.md`

#### Day10（阶段 1 选题：把“≤3 功能”写死）
- A：从 Top 类别里选 1 个“最易闭环”的方向（不是最宏大的），写：价值一句话 + 非目标（明确不做什么）
- B：创建阶段 1 的 GitHub Milestone/Project：把 backlog 切成 4 周（Week3–6）并设 **WIP=1**
- C：把阶段 1 的“对外产物节奏”写进 README：Week3 demo、Week4 config、Week5 RC、Week6 release