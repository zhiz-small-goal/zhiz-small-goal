# Day05–Day14 超细致执行计划（基于 v2.2，承接至 Day04）
- 权威依据：`zhiz_learning_plan_v2.2.md`（v2.2，日期 2025-12-20，America/Los_Angeles）
- 覆盖范围：仅 Day05–Day14（共 10 天）
- 核心约束：**WIP=1**；Feature 颗粒 **0.5–1 天**；每天固定 **A/B/C**；**连续 20 分钟无法形成下一步 → 立刻切 C 类任务**；优先可观测性与复测脚手架；产物可运行、可打包、可发布。

---

## 结论（1 句）
Day05–Day07 打通“本机一键打包 zip + push 即 CI 构建 + tag 触发 Release 附件”，Day08–Day10 完成需求雷达并收敛 Week3–Week6 选题与节奏，Day11–Day14 进入 Week3 实现“可演示优先”的 Win32 最小窗口/消息循环/热键/交互闭环（可行）。

## 默认假设（缺信息时的默认）
1. **环境**：Windows 10/11 + VS2022 Build Tools / MSVC + VSCode + CMake Presets 已可用（默认假设）。  
2. **仓库权限**：你可修改 `.github/workflows/`、创建 tag、发布 GitHub Release（默认假设）。  
3. **目标形态**：工具为“本地桌面小工具/可解压即用 zip”，暂不做安装器、账号系统、云同步（与 v2.2 非目标一致，默认假设）。  
4. **Day04 已完成到“日志模块 v0 可产生日志文件”**，但 docs/脚手架可能未完全补齐（默认假设；Day05 开头会核对）。

---

## 两种排期视图（Day 编号不变）

> 说明：你未指定 Day05 的开工日期，因此这里给两个“可直接套用”的日历映射。若你从别的日期开始，只要保持 Day 编号顺序不变即可。

### A) 10 个连续自然日版本（Day05–Day14 连续）
- Day05：D1
- Day06：D2
- Day07：D3
- Day08：D4
- Day09：D5
- Day10：D6
- Day11：D7
- Day12：D8
- Day13：D9
- Day14：D10

### B) 每周 5 学习日 + 周末缓冲版本（周末可选 buffer）
- Week A（学习 5 天）：Day05–Day09
- 周末 Buffer（可选）：用于“补 C 类任务、双机复测、填坑、回归脚手架”
- Week B（学习 5 天）：Day10–Day14

**Buffer 的默认用途（不抢主线主题）：**
1) 机器 B 复测；2) 修 CI/Release 边角；3) 补 docs 与回归用例；4) 录屏/发帖/收集外部反馈证据。

---

## 关键依据（Primary-first，供你回查）
> 下表用于“关键结论可定位”，日常执行时不需要每次重读。

| 结论/行为 | URL | 版本/日期 | 来源类型 | 定位 |
|---|---|---|---|---|
| 触发工作流（push/tag 过滤） | https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow | Docs（抓取：2025-12-20） | 官方文档 | “Using filters to target specific branches or tags for push events” |
| workflow 事件触发器总表 | https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows | Docs（抓取：2025-12-20） | 官方文档 | “push” 事件 + tags/tags-ignore |
| 工件上传（actions/upload-artifact@v4） | https://github.com/actions/upload-artifact | v4（页面抓取：2025-12-20） | 官方仓库/README | README（v4 说明与行为变化） |
| GitHub CLI 创建 Release + 上传资产 | https://cli.github.com/manual/gh_release_create | CLI Manual（抓取：2025-12-20） | 官方文档 | Examples（含上传 zip 资产） |
| Win32 热键投递机制（WM_HOTKEY） | https://learn.microsoft.com/windows/win32/inputdev/wm-hotkey | Last updated 2025-07-14 | 官方文档 | Remarks/Parameters（消息投递到注册线程队列） |
| RegisterHotKey 行为与冲突 | https://learn.microsoft.com/windows/win32/api/winuser/nf-winuser-registerhotkey | 页面抓取：2025-12-20 | 官方文档 | Remarks（冲突与失败） |

---

## 10 天总览表（Day05–Day14）
| Day | 主题（与 v2.2 对齐） | 当日 DoD（最小验收） | 关键产物（文件/脚手架） | 外部证据（可验证） | 主要风险 |
|---|---|---|---|---|---|
| Day05 | 打包：zip 脚本 + 发布清单 v0 | 本机一键产出带版本号 zip；按清单解压可运行 | `scripts/package.ps1`、`docs/release_checklist.md` | zip 文件 + SHA256；README 截图 | 路径/依赖遗漏导致 zip 不可运行 |
| Day06 | CI：push 即构建 | push 后 Actions 绿灯；产物可下载（artifact） | `.github/workflows/ci.yml`、`docs/ci.md`、badge | Actions run 链接 + badge | runner 环境差异导致构建失败 |
| Day07 | Release 自动化：tag → zip 附件 | tag 推送后自动生成 Release + 附件；可下载运行 | `.github/workflows/release.yml`、Release notes 模板 | Release 页面链接 + 资产下载截图 | token 权限/gh 认证/附件路径错 |
| Day08 | 需求雷达 #1：收集而不评判 | 问题库模板落地 + 10 条高质量事实记录 | `docs/problem_db.md`（或目录化条目） | 10 条链接可回访；首个讨论串草稿 | 记录混乱导致后续无法聚类 |
| Day09 | 需求雷达 #2：聚类 + 粗评分 | ≥20 条记录；Top10 粗评分；3–5 类聚类 | `docs/problem_summary_week2.md` | 摘要文档 + 可发布版本草稿 | 评分口径不一致 |
| Day10 | 选题收敛：把 ≤3 功能写死 | 选题一句话 + 非目标；Milestone/Project 建好；WIP=1 固化 | `docs/stage1_scope.md`、GitHub Milestone/Project | GitHub Project/Milestone 截图；对外帖（最小） | 选题过大导致 Week3 不可演示 |
| Day11 | Week3：最小窗口 + 消息循环 | 窗口可显示/关闭；UI 代码隔离目录完成 | `/app/ui_win32/`、`docs/win32_message_loop.md` | 10–30s 录屏 | 编码/入口点（WinMain）配置偏差 |
| Day12 | 热键：能触发 | RegisterHotKey 成功；按热键触发日志/弹窗 | 热键模块 + `docs/default_hotkey.md` | 录屏/日志片段 | 热键冲突/权限限制 |
| Day13 | 核心边界：UI → core 单向依赖 | core 接口骨架完成；UI 调用 core 不互相 include | `/core/` 最小接口、`docs/architecture.md` | 架构图 + build 通过 | 依赖倒置失败导致耦合 |
| Day14 | 交互：呼出/隐藏 + 焦点 + ESC | 热键呼出→输入框聚焦→ESC 隐藏→再次呼出 | show/hide + focus 处理、`docs/manual_test_week3.md` | 录屏 + 手测清单勾选 | 前台焦点与置顶策略不稳定 |

---

# 逐日展开（Day05 → Day14）
> 每天严格按 A/B/C。A 段只做一个“决策/机制”；B 段只推进一个 Feature（WIP=1）；C 段用于复测/打包/文档/录屏/发帖/整理。  
> **停止条件（每日必执行）：连续 20 分钟无法形成下一步 → 立刻切到当天 C 任务（至少 3 条备选）。**

---

## Day05（打包：zip 脚本 + 发布清单 v0）
### 今日目标（1 句）
把“本机一键产出可运行 zip”的链路做成脚本，并用发布清单把“可交付”变成可判定。

### Day04 完成核对清单（5 分钟，Day05 开头必须做）
> 目的：确认你确实站在“日志模块 v0”之上继续前进；发现缺漏则在 **Day05 的 A 或 C 段补齐**，不改变 Day05 主线主题。

- [ ] **构建可过**：`cmake --build --preset <你的 Debug 或 Release preset>` 结束码 0  
- [ ] **日志可产出**：运行 exe 后，在约定目录出现日志文件（含时间戳/等级/关键字段）  
- [ ] **路径可定位**：你知道日志路径来自哪里（硬编码/相对路径/配置项），能在 docs 写 2 句  
- [ ] **最小回归用例**：至少 1 个“会写日志”的固定触发点（例如启动打印、异常分支）  
- [ ] **提交可回退**：Day04 的改动已经 commit（便于 Day05 变更出现问题时快速回滚）

若任意项未满足：  
- **优先放到 Day05-C**（补文档/补回归/补脚手架）；  
- 若属于“路径/版本号规则”这类决策，放到 Day05-A 的 DoD 清单里一并定义。

---

### A 段（20–40min）：决策点 + 输出物
**决策点（只做 1 个）：发布清单 DoD + 版本号规则**  
你要把“一个 zip 包什么叫可交付”写死（否则 Day06/Day07 自动化会反复返工）。

**输出物（文件）**
- `docs/release_checklist.md`（v0）：包含两部分  
  1) **zip 内容清单**（必须/可选/禁止）  
  2) **版本号规则**（本地构建号、tag 版本、zip 命名）

**推荐规则（可直接采用）**
- 版本来源优先级：`git tag (vX.Y.Z)` > `VERSION.txt` > `0.0.0-dev`  
- zip 命名：`<project>-<version>-win64.zip`（win64 先写死，后续再细分）  
- zip 根目录结构（避免解压后散落）：  
  ```
  <project>-<version>/
    bin/zhiz_tool.exe
    config/config.example.json
    docs/README.txt   (或直接用根目录 README.md 的副本)
    LICENSE
    THIRD_PARTY_NOTICES.md
  ```
- 必须可运行判定：解压后双击或命令行运行能输出 `--help` 或窗口能启动。

---

### B 段（60–90min）：主 Feature（WIP=1）= `scripts/package.ps1`
**Feature 定义**：执行一次命令即可在 `dist/` 下得到带版本号的 zip（包含必要文件），并输出 SHA256 供对外校验。

#### 实现步骤（建议 8 步，每步都带判据）
1. **创建目录骨架**：新增 `scripts/` 与 `dist/`（若已有则确认用途）  
   - 判据：仓库根目录出现 `scripts/`；`dist/` 默认加入 `.gitignore`（只存产物）  
2. **确定版本获取函数**：在 `package.ps1` 中实现 `Get-Version`（优先读取 `git describe --tags --dirty --always`）  
   - 判据：在无 tag 时也能得到非空字符串；在 tag 存在时输出 `vX.Y.Z`  
3. **确定构建输入**：明确你使用的 CMake preset 名称（例如 `vs2022_release`）并在脚本顶部配置常量  
   - 判据：脚本可在不同机器仅修改 1 行 preset 即工作  
4. **构建 Release**：脚本调用 `cmake --build --preset <preset>`（必要时先 `cmake --preset <configurePreset>`）  
   - 判据：结束码 0；`out/build/.../Release/`（或你的结构）出现 exe  
5. **构建 staging 目录**：创建临时目录 `dist/_staging/<project>-<version>/...`，并把 exe/配置示例/许可证等复制进去  
   - 判据：staging 目录结构与 A 段清单一致；缺任何必须文件则脚本 `throw` 并给出缺失清单  
6. **压缩 zip**：使用 `Compress-Archive` 输出到 `dist/<project>-<version>-win64.zip`  
   - 判据：zip 可打开；文件路径不多一层、不少一层  
7. **生成校验值**：`Get-FileHash -Algorithm SHA256` 输出到 `dist/<zip>.sha256.txt`  
   - 判据：hash 文件存在，且内容包含 hash + 文件名  
8. **本机 smoke**：脚本末尾可选执行 `bin/zhiz_tool.exe --help`（或运行一次产生日志）  
   - 判据：退出码 0；日志/输出符合 Day04 的可观测性要求

#### 验证方法（B 段结束前必须跑完一次）
- 命令：`powershell -ExecutionPolicy Bypass -File scripts/package.ps1`  
- 预期：`dist/` 下出现 zip + sha256 文件；解压后运行通过；日志位置可定位。

---

### C 段（20–40min）：复测/打包/文档/对外动作（≥3）
1. **写并跑本机复测清单 v0**：在 `docs/release_checklist.md` 里新增“本机复测步骤”并勾选一次  
   - 证据：清单勾选 + 运行截图（终端输出/文件列表）  
2. **补 README 的下载/运行说明占位**（先不发 Release 也可）  
   - 证据：README 中出现 `How to run from zip` 小节  
3. **提交与标签准备**：commit（包含脚本与清单）；为 Day07 的 tag 发布预留 `CHANGELOG.md` 或 `docs/release_notes_template.md`  
   - 证据：commit hash；release notes 模板文件存在

---

### 当日停止条件与切换策略（必须写死）
- 触发：**连续 20 分钟无法形成下一步**（例如路径找不到、脚本报错无定位）  
- 立刻动作：暂停 B 段实现，切到 C 类任务，优先产出“可复现 + 可回归”的证据。

**当日 C 类备选清单（至少 3 条，可直接执行）**
- 写 `docs/package_troubleshooting.md`：记录报错 + 复现命令 + 你猜测的原因 + 下一次要验证的 3 个点  
- 给 `package.ps1` 增加 `-Verbose` 输出和“找不到文件时列目录”诊断  
- 用 1 条 `scripts/smoke.ps1` 固化“解压后运行 + 生成日志”的最小回归脚本

---

### Day05 当日 DoD（满足才算完成）
- [ ] `scripts/package.ps1` 一键生成 zip + sha256（本机跑通 1 次）  
- [ ] `docs/release_checklist.md` 存在且包含：zip 清单 + 本机复测步骤 + 版本规则  
- [ ] README 至少出现“从 zip 运行”的占位说明  
- [ ] 提交已完成（可回滚）

### 风险点（1–3）与规避动作
1. **构建输出目录不稳定** → 脚本里用“查找 exe 的规则”而非硬编码长路径（例如在 build 输出下递归找 `zhiz_tool*.exe`）。  
2. **zip 漏文件导致不可运行** → staging 时对“必须文件列表”做显式校验，缺失就 fail-fast。  
3. **版本号来源混乱** → 先写死优先级：tag > VERSION.txt > dev，并在脚本打印最终版本号。

### 记录模板（复制粘贴到当天复盘）
```md
## Day05 复盘
- 完成了什么（可验证）：
  - [ ] 产物：dist/xxx.zip + sha256
  - [ ] 文档：docs/release_checklist.md（含 zip 清单 + 本机复测）
- 阻塞点（事实 + 复现）：
  - 现象：
  - 复现命令：
  - 当前假设：
- 明天第一步（必须是可执行动作）：
  - Step0：
- 新增回归用例 / 脚手架：
  - [ ] scripts/xxx.ps1：
- 外部反馈线索：
  - 计划发到哪里：
  - 需要对方回答的问题：
```

---

## Day06（CI：push 即构建）
### 今日目标（1 句）
让每次 push 都触发 Windows Runner 构建，并把可下载产物（artifact）保存下来，失败即阻断。

### A 段（20–40min）：决策点 + 输出物
**决策点（只做 1 个）：CI 的最小目标（DoD）与失败入口**  
建议你把 CI 目标限定为“构建 + 上传产物 + 失败可定位”，不在 Day06 叠加测试矩阵。

**输出物**
- `docs/ci.md`（v0）：写清  
  1) 工作流文件位置  
  2) 触发条件（push / PR）  
  3) 常见失败定位入口（Actions 日志的关键步骤、产物目录）

---

### B 段（60–90min）：主 Feature（WIP=1）= `.github/workflows/ci.yml`
**Feature 定义**：push → CI 自动运行 → 构建成功 → 上传 artifact（至少包含 exe 或 zip），并能从 Actions 页面下载。

#### 实现步骤（建议 9 步）
1. **新建工作流文件**：`.github/workflows/ci.yml`  
   - 判据：push 后 Actions 看到新 workflow  
2. **设置触发器**：`on: [push, pull_request]`（先不做路径过滤）  
   - 判据：任意 push 都触发；PR 也触发  
3. **选择 Runner**：`runs-on: windows-latest`  
   - 判据：日志显示 Windows runner  
4. **Checkout**：使用 `actions/checkout@v5`  
   - 判据：workspace 有仓库文件  
5. **配置 CMake**：用 preset（推荐）或命令行配置；示例：`cmake --preset vs2022`  
   - 判据：生成成功；日志里有 generator 信息  
6. **构建**：`cmake --build --preset vs2022_release`（或你的 release preset）  
   - 判据：结束码 0；出现 exe  
7. **收集产物目录**：将 exe 与必要文件复制到 `artifact/` 目录（CI 内临时）  
   - 判据：`artifact/` 下至少有 exe  
8. **上传 artifact**：`actions/upload-artifact@v4` 上传 `artifact/`  
   - 判据：Actions 页面出现可下载 artifact  
9. **失败即阻断**：不写 `continue-on-error`；必要时 `set -e`（PowerShell 默认遇到非零需显式处理）  
   - 判据：故意引入编译错误时 workflow 红灯

#### 验证方法
- 在任意文件做一个无害修改并 push：检查 Actions 是否绿色；下载 artifact 并确认 exe 存在。

---

### C 段（20–40min）：复测/文档/对外动作（≥3）
1. **在 README 加 CI badge**  
   - 证据：README 顶部出现 badge；点进去能看到最新运行结果  
2. **写“失败排查入口”**：`docs/ci.md` 增加 3 条常见失败（找不到 cmake/preset、找不到依赖、找不到 exe 输出）  
   - 证据：文档包含“定位路径 + 关键日志关键词”  
3. **把 CI 的 artifact 用作“回归对照”**：下载一次 artifact 并记录 SHA256（或文件大小）  
   - 证据：在 `docs/ci.md` 记录一次 run id + artifact 信息

---

### 当日停止条件与切换策略
- 触发：CI 连续 20 分钟无法绿灯（例如 runner 环境差异）  
- 立刻动作：切 C，目标变为“形成最小可定位证据”，不要继续盲改 workflow。

**C 类备选清单**
- 写 `docs/ci_failures.md`：记录失败 run 链接 + 关键日志段落 + 下一次实验计划  
- 把 CI 步骤拆成更细的输出（列目录、打印 CMake cache）  
- 先只构建 Debug 或只构建 Release，缩小变量后再扩回

---

### Day06 当日 DoD
- [ ] push/pull_request 触发 workflow，至少 1 次绿灯  
- [ ] artifact 可下载且包含 exe（或 staging 目录）  
- [ ] README 有 CI badge  
- [ ] `docs/ci.md` 存在且可作为“排查入口”

### 风险点与规避
1. **preset 名称不一致** → 在 workflow 顶部用变量集中定义 preset 名字。  
2. **PowerShell 出错不 fail** → 使用 `$ErrorActionPreference = "Stop"`，确保非零立即失败。  
3. **artifact 路径错误** → 在上传前 `dir /s artifact` 输出目录树。

### 记录模板
```md
## Day06 复盘
- 完成了什么：
  - [ ] Actions 绿灯 run 链接：
  - [ ] artifact 内容：
- 阻塞点：
  - 现象 / run 链接：
  - 我做了哪些实验（按时间）：
- 明天第一步：
  - Step0：
- 新增回归脚手架：
  - [ ] docs/ci.md 更新点：
- 外部反馈线索：
  - 想让别人帮你看的具体问题：
```

---

## Day07（Release 自动化：tag 产出 zip 附件）
### 今日目标（1 句）
把“打 tag → 自动打包 → 自动创建 Release 并上传 zip 附件”的链路跑通一次，并完成可下载可运行的演练发布。

### A 段（20–40min）：决策点 + 输出物
**决策点（只做 1 个）：Release 触发条件 + 资产命名规则**  
建议采用：push tag `v*` 触发 Release workflow；资产名称与 Day05 zip 命名一致。

**输出物**
- `docs/release_automation.md`（v0）：写清  
  1) 触发器：tag 模式  
  2) workflow 文件名  
  3) Release 资产：zip + sha256  
  4) 回滚策略：删 tag/删 release 的人工步骤（写清，不自动化）

---

### B 段（60–90min）：主 Feature（WIP=1）= `.github/workflows/release.yml`
**Feature 定义**：`git tag v0.0.1 && git push --tags` 后，GitHub 自动创建 Release，并附带 `dist/<project>-v0.0.1-win64.zip`（可下载运行）。

#### 实现步骤（建议 10 步）
1. **新建 workflow**：`.github/workflows/release.yml`  
   - 判据：push tag 后会触发（Actions 页面可见）  
2. **触发器**：`on: push: tags: - "v*"`  
   - 判据：只有 tag 推送触发，普通 push 不触发  
3. **权限**：`permissions: contents: write`（用于创建 release/上传资产）  
   - 判据：workflow 不因权限不足失败  
4. **Checkout**：`actions/checkout@v5` 且 `fetch-depth: 0`（方便取 tag/version）  
   - 判据：`git describe --tags` 在 CI 内能工作  
5. **运行打包脚本**：执行 `scripts/package.ps1` 产出 zip 到 `dist/`  
   - 判据：workflow 中能看到 zip 文件路径  
6. **安装/使用 gh**：windows runner 默认自带 gh（若缺则安装）；验证 `gh --version`  
   - 判据：能运行 gh  
7. **创建 Release**：`gh release create <tag> <zip> <sha256> --title ... --notes-file ...`（先用模板 notes）  
   - 判据：Release 页面出现，且 assets 列表里有 zip  
8. **避免重复发布**：如 tag 已有 release，使用 `gh release view` 判断并决定 fail 或 overwrite（先选择 fail-fast）  
   - 判据：重复执行时行为明确（不产生“半成功”状态）  
9. **演练发布**：在你的仓库创建 `v0.0.1`（或 v0.0.0）tag 并 push  
   - 判据：Release 自动生成  
10. **下载验证**：从 Release 页面下载 zip，在机器 A 解压运行；若有机器 B，优先用 B 验证  
   - 判据：能运行且日志可定位

---

### C 段（20–40min）：复测/文档/对外动作（≥3）
1. **发布演示证据**：录一段 10–30 秒（解压→运行→显示输出/窗口）  
   - 证据：`docs/demo_links.md` 记录文件名/路径；或 README 放 gif  
2. **写 Release notes 模板**：`docs/release_notes_template.md`（包含：变更点、已知问题、验证步骤）  
   - 证据：模板存在并被 Day07 的 workflow 使用  
3. **把“发布清单 DoD”与 Release 自动化对齐**：更新 `docs/release_checklist.md` 增加“tag 发布演练步骤”  
   - 证据：清单中出现明确命令与预期结果

---

### 当日停止条件与切换策略
- 触发：Release workflow 连续 20 分钟无法产出 assets（权限/gh/路径问题）  
- 立刻动作：切 C，优先把失败 run 的证据整理成“最小排查包”，下次在 A 段做决策。

**C 类备选清单**
- 写 `docs/release_failures.md`：记录失败 run 链接 + 关键日志 + 你要尝试的 3 个修复方向  
- 把 workflow 中每一步加 `dir dist`/`Get-ChildItem -Recurse` 输出  
- 暂时改成 `workflow_dispatch` 手动触发，先验证脚本与 gh，再回到 tag 触发

---

### Day07 当日 DoD
- [ ] tag 推送触发 release workflow  
- [ ] Release 页面存在且包含 zip + sha256 资产  
- [ ] 至少 1 次下载验证通过（优先机器 B；否则机器 A）  
- [ ] 有 10–30 秒可演示证据（gif/录屏）

### 风险点与规避
1. **GITHUB_TOKEN 权限不足** → 显式声明 `permissions: contents: write`。  
2. **gh 发布失败（认证/权限）** → 使用 `env: GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}` 并在日志中打印 `gh auth status`。  
3. **assets 路径不对** → 上传前 `Get-ChildItem dist` 输出并 assert 文件存在。

### 记录模板
```md
## Day07 复盘
- 完成了什么：
  - [ ] Release 链接：
  - [ ] Assets 列表：
  - [ ] 下载验证（机器/结果）：
- 阻塞点：
  - 失败日志关键词：
  - 当前假设：
- 明天第一步：
  - Step0：
- 新增回归脚手架：
  - [ ] docs/release_checklist.md 更新：
- 外部反馈线索：
  - 我准备把 Release 发到哪里：
```

---

## Day08（需求雷达 Session #1：收集而不评判）
### 今日目标（1 句）
建立“问题库模板 + 10 条高质量事实记录”，保证后续聚类与选题可复用且可回访。

### A 段（20–40min）：决策点 + 输出物
**决策点（只做 1 个）：问题库模板字段与记录粒度**  
要求：每条记录必须可回访（链接/截图），必须描述“可观察行为”，禁止直接下结论。

**输出物**
- `docs/problem_db.md`（v0 模板 + 10 条记录的容器）
  - 字段建议（与 v2.2 对齐）：  
    - 场景（谁/在什么上下文）  
    - 可观察行为（用户做了什么→系统发生了什么）  
    - 频率证据（同类问题出现次数/时间跨度）  
    - 代价（时间/金钱/风险；用事实表达）  
    - 现有替代方案（产品/脚本/手工流程）  
    - 复现/验证方式（你如何在本地模拟）  
    - 链接（至少 1 个英文来源链接；可多链接）

---

### B 段（60–90min）：主 Feature（WIP=1）= 需求雷达数据采集 v0（10 条）
**Feature 定义**：从 1–2 个公开社区抓取 10 条“抱怨/卡点/反复问的问题”，并写入问题库（只记录事实）。

#### 采集渠道（建议英文优先，避免非英语结论污染）
- GitHub Issues（同类工具）  
- Reddit（r/windows, r/software, r/AutoHotkey 等）  
- Stack Overflow（关键词：hotkey, RegisterHotKey, global hotkey, focus window）  
- Microsoft Learn Q&A（Win32/Hotkey/Focus）

#### 实现步骤（建议 7 步）
1. **定义主题边界**：今天只收集与你 Week3 方向相关的“热键/窗口/交互/配置/可分发”问题  
   - 判据：10 条里 ≥7 条与 Week3–Week6 方向直接相关  
2. **设置采集时间盒**：30 分钟抓取（计时），不评判、不筛选“好坏”  
   - 判据：30 分钟结束必须停  
3. **记录原始链接**：每条至少 1 个英文链接 + 关键句的截图/引用位置  
   - 判据：未来你点链接能直接看到原文  
4. **写“可观察行为”**：把问题转成“用户动作→系统表现”的句式  
   - 判据：每条都能写出 1 句行为描述  
5. **记录替代方案**：用户当前怎么解决（脚本/手动/别的软件）  
   - 判据：每条至少 1 个替代方案  
6. **标注“可验证”**：如果你未来做工具，可如何验证“解决了”（例如：热键冲突提示更清晰）  
   - 判据：每条给 1 条验证口径  
7. **提交问题库**：commit `docs/problem_db.md` 的新增内容  
   - 判据：问题库可追溯版本

---

### C 段（20–40min）：整理/对外动作（≥3）
1. **做一个“问题库公开入口”**：在 README 增加链接指向 `docs/problem_db.md`  
   - 证据：README 可点击到问题库  
2. **准备对外帖草稿**（不一定今天发布）：`docs/post_draft_problem_radar.md`  
   - 证据：草稿包含“我在收集什么 + 你可以怎么帮我”  
3. **把“记录规则”写成 6 条**：避免 Day09–Day10 评分阶段返工  
   - 证据：问题库顶部出现“记录规则”小节

---

### 当日停止条件与切换策略
- 触发：采集来源打不开/陷入筛选纠结导致 20 分钟无下一步  
- 立刻动作：切 C，优先把“模板与规则”写牢，采集数量允许降级但结构必须可复用。

**C 类备选清单**
- 给问题库模板补一个“例子条目（范例）”，作为未来对齐口径  
- 写一个小脚本 `scripts/open_problem_sources.ps1` 一键打开 10 个来源链接  
- 把 Day08 的 10 条做成 Issue（仅标题+链接），为 Day10 的 Project 准备素材

---

### Day08 当日 DoD
- [ ] `docs/problem_db.md` 模板落地并包含 ≥10 条记录  
- [ ] 每条记录含：英文链接 + 可观察行为 + 替代方案 + 可验证口径  
- [ ] README 指向问题库入口  
- [ ] 至少 1 个对外帖草稿存在

### 风险点与规避
1. **“记录结论而非事实”** → 强制句式：动作→表现→代价→证据链接。  
2. **来源碎片化** → 只选 1–2 个社区，先深挖再扩展。  
3. **后续无法聚类** → 每条加 1 个“关键词标签”（手动即可），用于 Day09 聚类。

### 记录模板
```md
## Day08 复盘
- 完成了什么：
  - [ ] problem_db 条目数：
  - [ ] 覆盖渠道：
- 阻塞点：
  - 哪些来源浪费时间/不可复用：
- 明天第一步：
  - Step0（先做哪一类聚类）：
- 新增回归/脚手架：
  - [ ] 记录规则新增：
- 外部反馈线索：
  - 我准备把草稿发到哪里（GitHub Discussion / Reddit / ...）：
```

---

## Day09（需求雷达 Session #2：聚类 + 粗评分）
### 今日目标（1 句）
把问题库扩到 ≥20 条，并用统一粗评分把 Top10 与 3–5 类聚类产出为 1 页摘要。

### A 段（20–40min）：决策点 + 输出物
**决策点（只做 1 个）：粗评分标准（统一口径）**  
建议使用 3 维度，每维 1–5 分，且写清判据：
- 频率（出现多不多，有无多来源重复）
- 代价（时间/金钱/风险/不可逆）
- 替代方案成熟度（替代是否足够好；越不成熟越有机会）

**输出物**
- `docs/problem_scoring_rubric.md`（或写在 `docs/problem_summary_week2.md` 开头）

---

### B 段（60–90min）：主 Feature（WIP=1）= 聚类 + Top10 粗评分
#### 实现步骤（建议 8 步）
1. **补齐到 ≥20 条**：再收集 10 条（仍然只记录事实）  
   - 判据：总条目数 ≥20  
2. **去重规则**：同一问题不同来源 → 合并为 1 条，保留多链接  
   - 判据：去重后仍 ≥15 条；每条可回访  
3. **打标签（3–5 类先验）**：例如 `hotkey-conflict`、`focus`、`config`、`distribution`、`logging`  
   - 判据：每条至少 1 个标签  
4. **按 rubric 打分**：对候选 Top10 条目填写 3 维分数与一句话理由（理由必须引用事实证据）  
   - 判据：Top10 每条都有完整评分  
5. **聚类输出**：把条目按标签聚合成 3–5 类，每类给一句“共同模式”  
   - 判据：每类 ≥2 条；模式描述不依赖主观词  
6. **选出 Top 类别**：根据 Top10 的分布，确定 1–2 个最值得推进的类  
   - 判据：能解释“为什么是它”且引用评分  
7. **产出 1 页摘要**：`docs/problem_summary_week2.md`（结构固定：背景→方法→Top10→聚类→下一步）  
   - 判据：单页即可读，且每个 Top10 带链接  
8. **提交与对外准备**：commit；并把摘要复制到对外帖草稿中  
   - 判据：草稿可直接发布（只需补 2–3 句）

---

### C 段（20–40min）：复测/对外动作（≥3）
1. **把摘要做成 GitHub Discussion 草稿**（建议英文）  
   - 证据：`docs/post_draft_problem_summary.md` 完整可发布  
2. **在仓库开 3 个 Issue（从 Top 类别中选）**：每个 Issue 只写：问题陈述 + 链接 + 你要验证的假设  
   - 证据：Issue 链接（或至少本地 Markdown 草稿）  
3. **更新 README 的“Roadmap/Next”**：加入 Week3–Week6 的“输入来自 problem summary”  
   - 证据：README 更新可追溯

---

### 当日停止条件与切换策略
- 触发：评分口径摇摆/聚类纠结导致 20 分钟无法推进  
- 立刻动作：切 C，把 rubric 写得更可判定；允许先粗分后再校准。

**C 类备选清单**
- 把评分表做成 Markdown 表格（固定列），减少思考开销  
- 写一个“评分示例条目”作为基准  
- 把 Top10 的链接整理成 `scripts/open_top10.ps1` 一键打开

---

### Day09 当日 DoD
- [ ] problem_db ≥20 条（去重后 ≥15 条）  
- [ ] rubric 明确且 Top10 完成评分  
- [ ] `docs/problem_summary_week2.md` 完成（可发布）  
- [ ] 至少 3 个从 Top 类别衍生的“验证型 Issue/草稿”存在

### 风险点与规避
1. **评分被个人偏好污染** → 每条理由必须引用“频率/代价/替代方案”的事实。  
2. **聚类太细导致失焦** → 强制 3–5 类，超过就合并。  
3. **输出不可复用** → 摘要必须可被 Day10 直接用来“选题 + 切分 backlog”。

### 记录模板
```md
## Day09 复盘
- 完成了什么：
  - [ ] 总条目数 / 去重后数：
  - [ ] 聚类类别：
  - [ ] Top10 列表位置：
- 阻塞点：
  - rubric 哪条最不确定：
- 明天第一步：
  - Step0（基于 Top 类别做选题）：
- 新增回归/脚手架：
  - [ ] open_top10 脚本：
- 外部反馈线索：
  - 我准备发布摘要到哪里：
```

---

## Day10（阶段 1 选题：把“≤3 功能”写死）
### 今日目标（1 句）
从需求雷达 Top 类别中选 1 个最易闭环方向，明确非目标，并把 Week3–Week6 的 backlog 切成可执行的 WIP=1 系统。

### A 段（20–40min）：决策点 + 输出物
**决策点（只做 1 个）：选题与非目标（写死）**  
判据：Week3 必须能演示；Week4–Week6 才逐步补 config/健壮性/发布。

**输出物**
- `docs/stage1_scope.md`（必须包含）  
  - 价值一句话（用户层面的可观察收益）  
  - 非目标（至少 5 条，明确“不做什么”）  
  - ≤3 个功能（每个功能一句话 + 验收口径）

---

### B 段（60–90min）：主 Feature（WIP=1）= Milestone/Project + backlog 切分
#### 实现步骤（建议 8 步）
1. **把 Day09 Top 类别映射到“≤3 功能”候选**  
   - 判据：候选功能都能在 0.5–1 天做出可演示增量  
2. **做删减**：如果一个功能需要 3 天以上，拆成“演示版/增强版/可配置版”三层  
   - 判据：Week3 只做演示版  
3. **建立 GitHub Milestone**：例如 `Stage1-Week3..6`（或按周拆 4 个 milestone）  
   - 判据：每个 Issue 都能归属到某周  
4. **建立 GitHub Project（看板）**：列：Backlog / Ready / Doing(WIP=1) / Verify / Done  
   - 判据：Doing 列设置 WIP=1（规则或人工约束）  
5. **创建 8–12 个 Issue（最小）**：从 Week3–Week6 各放 2–3 个，标题要可验证  
   - 判据：每个 Issue 都有验收口径（DoD）  
6. **把 Week3 的 4 天（Day11–Day14）写成 Issue 链**：Day11 窗口、Day12 热键、Day13 core 边界、Day14 交互  
   - 判据：Issue 描述可直接复制到每日计划执行  
7. **写“对外产物节奏”**：README 增加：Week3 demo、Week4 config、Week5 RC、Week6 release  
   - 判据：README 里节奏清晰且可回查  
8. **把 Day09 摘要发布出去（最小曝光）**：选择 1 个渠道发帖并明确要什么反馈  
   - 判据：外部链接可访问，且你能跟踪回复

---

### C 段（20–40min）：对外动作/证据（≥3）
1. **发布“问题库摘要”**（建议渠道优先级）：GitHub Discussions（仓库内）→ Reddit（相关板块）→ Hacker News（谨慎）  
   - 证据：讨论串链接或截图  
2. **收集反馈问题**：在帖子末尾附 3 个明确问题（例如：你最常遇到哪类热键/焦点问题？）  
   - 证据：帖子正文包含问题  
3. **把反馈入口写进仓库**：README 增加“反馈入口”（Issues/Discussions）  
   - 证据：README 更新

---

### 当日停止条件与切换策略
- 触发：选题摇摆导致 20 分钟没有可判定下一步  
- 立刻动作：切 C，把“非目标”写得更硬，强制删减，再回到选题。

**C 类备选清单**
- 做一个“选题对比表”（2–3 行即可）：每个选题的 Week3 可演示性/风险/依赖  
- 把 Top10 里最具体的 3 条做成“验收口径”样例  
- 先把 Project/看板建好，再填 Issue（分离决策与输入）

---

### Day10 当日 DoD
- [ ] `docs/stage1_scope.md` 完整（价值一句话 + 非目标 + ≤3 功能 + 验收口径）  
- [ ] GitHub Milestone/Project 建好且 WIP=1 可执行  
- [ ] README 写入 Week3–Week6 对外节奏  
- [ ] “问题库摘要”已对外发布一次（最小曝光），并留下反馈问题

### 风险点与规避
1. **选题过大** → 用“Week3 必须可演示”作为硬门槛，不满足直接淘汰。  
2. **Issue 质量低不可执行** → 每条 Issue 必须含：输入/输出/验证方式。  
3. **外部曝光成本过高** → 先在仓库 Discussions 做最小曝光，积累可引用链接。

### 记录模板
```md
## Day10 复盘
- 完成了什么：
  - [ ] stage1_scope.md：
  - [ ] Project/Milestone：
  - [ ] 外部帖子链接：
- 阻塞点：
  - 最难决定的是哪条非目标/功能边界：
- 明天第一步：
  - Step0（Day11 开始做窗口骨架）：
- 新增回归/脚手架：
  - [ ] README Roadmap 更新：
- 外部反馈线索：
  - 谁/哪里可能会给你反馈：
```

---

## Day11（Week3：窗口骨架：能跑）
### 今日目标（1 句）
实现最小 Win32 窗口 + 消息循环可显示/关闭，并把 UI 代码隔离到 `/app/ui_win32/`，为热键与交互做承载体。

### A 段（20–40min）：决策点 + 输出物
**决策点（只做 1 个）：UI 实现与目录边界**  
默认采用：Win32 原生窗口（避免引入大依赖），UI 代码放 `app/ui_win32/`，core 不依赖 UI。

**输出物**
- `docs/ui_structure_week3.md`：写清目录与依赖方向（两条即可）
  - `app/ui_win32/*` 只负责窗口与消息分发  
  - `core/*` 只负责“动作/配置/执行”，不包含 Win32 头文件

---

### B 段（60–90min）：主 Feature（WIP=1）= 最小窗口 + 消息循环
#### 实现步骤（建议 9 步）
1. **创建目录与文件**：`app/ui_win32/` 下新增 `win32_main.cpp`（或拆成 `window.cpp/h`）  
   - 判据：CMake 能编译新文件  
2. **入口点选择**：决定 `main()` vs `WinMain()`（建议 Week3 用 `WinMain` 更贴近消息循环）  
   - 判据：链接通过；子系统设置一致（Console/Windows）  
3. **注册窗口类**：`RegisterClassEx`（或 `RegisterClass`）  
   - 判据：返回非零；失败时 `GetLastError` 打日志  
4. **创建窗口**：`CreateWindowEx` 并 `ShowWindow` / `UpdateWindow`  
   - 判据：窗口可见；标题正确  
5. **消息循环**：`GetMessage/TranslateMessage/DispatchMessage`  
   - 判据：窗口响应关闭按钮；无卡死  
6. **处理 WM_DESTROY**：`PostQuitMessage(0)`  
   - 判据：退出码 0；进程结束  
7. **最小可观测性**：在关键路径写日志（创建成功/失败、收到 WM_*）  
   - 判据：日志含“窗口创建成功”与“退出”  
8. **隔离窗口创建代码**：`CreateMainWindow()` 返回 `HWND`，主函数只负责初始化与 loop  
   - 判据：主函数 ≤50 行；结构清晰  
9. **Release 构建验证**：用 Day05 脚本打包一次（可选，只 smoke）  
   - 判据：Release 版能启动窗口

---

### C 段（20–40min）：文档/演示（≥3）
1. **记录消息循环因果链**：`docs/win32_message_loop.md`（5–15 行）  
   - 证据：文档含“消息进入队列→GetMessage→Dispatch→WndProc”链条  
2. **录屏 10–30 秒**：窗口启动与关闭  
   - 证据：录屏文件 + 路径记录  
3. **补一条手测用例**：`docs/manual_test_week3.md` 先写 2 条（启动/关闭）  
   - 证据：清单可勾选

---

### 当日停止条件与切换策略
- 触发：WinMain/子系统/链接错误导致 20 分钟没有稳定下一步  
- 立刻动作：切 C，把“最小可复现”固化（最小 Win32 例子 + 构建命令 + 错误信息），避免继续扩大改动面。

**C 类备选清单**
- 写 `docs/win32_build_troubleshooting.md`：记录入口点/子系统/CMake 配置对应关系  
- 用一个最小 Win32 sample（仅创建窗口）单文件验证，再迁回项目结构  
- 给 CI 增加一个“只编译 UI 目标”的步骤，用于快速定位

---

### Day11 当日 DoD
- [ ] `app/ui_win32/` 中最小窗口可显示/关闭  
- [ ] 消息循环可运行且退出正常  
- [ ] `docs/win32_message_loop.md` 完成  
- [ ] 有演示证据（录屏或截图）

### 风险点与规避
1. **Console/Windows 子系统冲突** → 明确选择一种，并在 CMake 中固定（避免同一天切换多次）。  
2. **WndProc 结构混乱** → 只处理必要消息（WM_DESTROY），其他先 `DefWindowProc`。  
3. **日志路径影响演示** → 日志失败不阻断窗口启动，但必须可定位原因。

### 记录模板
```md
## Day11 复盘
- 完成了什么：
  - [ ] 窗口能跑（证据）：
  - [ ] win32_message_loop.md：
- 阻塞点：
  - 失败类型（编译/链接/运行）：
  - 复现命令：
- 明天第一步：
  - Step0（加热键注册）：
- 新增回归/脚手架：
  - [ ] manual_test_week3.md 新增用例：
- 外部反馈线索：
  - 我想让别人验证的是哪一步：
```

---

## Day12（热键：能触发）
### 今日目标（1 句）
实现 RegisterHotKey + WM_HOTKEY 处理：按下全局热键能触发可观察行为（日志/弹窗），并明确生命周期与冲突处理规则。

### A 段（20–40min）：决策点 + 输出物
**决策点（只做 1 个）：热键生命周期规则（5 条）**  
建议写死以下规则（输出到文档）：
1) 启动时注册；2) 注册失败要提示冲突并降级；3) 退出时必须注销；4) 配置变更需先注销再注册；5) UI 隐藏不等于注销（先不做动态切换也可）。

**输出物**
- `docs/default_hotkey.md`：默认热键、冲突策略、如何修改（占位也可）

---

### B 段（60–90min）：主 Feature（WIP=1）= RegisterHotKey + WM_HOTKEY
#### 实现步骤（建议 9 步）
1. **定义默认热键**：例如 `Ctrl+Alt+Space`（尽量避开系统保留）  
   - 判据：文档与代码一致；键值用 `MOD_CONTROL|MOD_ALT` + `VK_SPACE`  
2. **注册热键**：在窗口创建成功后调用 `RegisterHotKey(NULL 或 hwnd, id, modifiers, vk)`  
   - 判据：返回 TRUE；失败时记录 `GetLastError`  
3. **处理 WM_HOTKEY**：在 WndProc 里捕获并根据 `wParam` 的 id 分发  
   - 判据：按热键能触发日志或 MessageBox  
4. **可观察行为**：先用最直接的行为（`MessageBox` 或写日志）  
   - 判据：行为对用户可见且可录屏  
5. **冲突降级策略 v0**：失败时提示“被占用”，并建议用户改键（暂不实现 UI 改键）  
   - 判据：冲突时不会静默失败  
6. **注销热键**：在 WM_DESTROY 或退出路径调用 `UnregisterHotKey`  
   - 判据：退出后不残留热键占用（再次启动仍可注册）  
7. **日志补强**：记录注册成功/失败、收到 WM_HOTKEY 的时间戳与参数  
   - 判据：日志可用于远程排查  
8. **手测用例**：更新 `docs/manual_test_week3.md` 增加 2 条（注册成功、触发行为）  
   - 判据：清单可勾选  
9. **打包演示**：Day05 脚本打一个 zip，并确认热键在 Release 包里可用  
   - 判据：从 zip 启动也能注册热键并触发

---

### C 段（20–40min）：文档/演示（≥3）
1. **录屏**：按热键触发行为（10–30 秒）  
   - 证据：录屏文件  
2. **README 增加“默认热键/如何修改”占位**  
   - 证据：README 小节存在  
3. **写一条“热键冲突排查”**：`docs/default_hotkey.md` 增加：如何判断被占用、如何换一个组合键  
   - 证据：文档含具体建议与例子

---

### 当日停止条件与切换策略
- 触发：RegisterHotKey 持续失败且 20 分钟无定位（冲突/权限/线程问题）  
- 立刻动作：切 C，把失败分解为最小实验：在一个最小 demo 里注册同样热键，比较行为差异。

**C 类备选清单**
- 写 `docs/hotkey_debug.md`：记录 `GetLastError` 值 + 触发条件  
- 临时换一个更不冲突的组合键（例如加 SHIFT），先验证链路  
- 把“注册热键”移动到确定有消息循环的线程（与窗口线程一致），排除线程错误

---

### Day12 当日 DoD
- [ ] 默认热键注册成功（或冲突时可理解提示）  
- [ ] WM_HOTKEY 触发可观察行为（日志/弹窗）  
- [ ] 退出时热键注销  
- [ ] `docs/default_hotkey.md` 完成，`manual_test_week3.md` 更新

### 风险点与规避
1. **系统保留热键** → 避免使用 Win 键组合；优先 Ctrl+Alt+非系统键。  
2. **注册线程不对** → 注册与消息循环应在同一线程，避免“注册成功但收不到消息”。  
3. **冲突频繁** → 提供至少 2 套备选默认热键（文档写明）。

### 记录模板
```md
## Day12 复盘
- 完成了什么：
  - [ ] 热键注册/触发（证据）：
  - [ ] default_hotkey.md：
- 阻塞点：
  - GetLastError / 触发条件：
- 明天第一步：
  - Step0（建立 core 边界）：
- 新增回归/脚手架：
  - [ ] manual_test_week3.md 新增用例：
- 外部反馈线索：
  - 我想让别人验证的默认热键是否合理：
```

---

## Day13（核心边界：UI → core 的调用路径）
### 今日目标（1 句）
定义 `/core` 最小对外接口并实现 dummy action，保证 UI 调用 core，但 core 不依赖 UI（单向依赖边界清晰）。

### A 段（20–40min）：决策点 + 输出物
**决策点（只做 1 个）：core 的最小接口形态**  
建议先写 3 个类型（最小可用即可）：
- `Action`（id、name、execute）  
- `ActionRegistry`（注册/查询）  
- `ActionExecutor`（执行入口，返回结果/错误）

**输出物**
- `docs/architecture.md`（v0）：一张 ASCII 图 + 5 行边界说明  
  ```
  app/ui_win32  --->  core
  (Win32 types)      (no Win32 headers)
  ```

---

### B 段（60–90min）：主 Feature（WIP=1）= core 骨架 + UI 调用路径
#### 实现步骤（建议 10 步）
1. **建立 core 目标**：在 CMake 中新增 `add_library(core ...)`（或已有则调整）  
   - 判据：core 可单独编译  
2. **禁止 core 引 Win32**：core 头文件不包含 `<windows.h>`  
   - 判据：搜索 `windows.h` 不出现在 core/  
3. **定义接口头**：`core/action.h`、`core/action_registry.h`、`core/action_executor.h`  
   - 判据：接口清晰、最小可用  
4. **定义错误模型 v0**：返回 `bool` + error string，或 `std::optional<std::string>`  
   - 判据：调用者能获得错误原因  
5. **实现 dummy action**：例如 `Action{id="demo.log", execute=>写日志一行}`  
   - 判据：触发后日志可见  
6. **UI 调用 core**：在 WM_HOTKEY 触发时调用 `ActionExecutor::Execute("demo.log")`  
   - 判据：热键触发路径变为“UI→core→日志”  
7. **依赖方向自检**：UI 可 include core；core 不 include UI  
   - 判据：删除 UI 目录仍可编译 core  
8. **写最小单元测试（可选）**：若无测试框架，先写 `app/cli_smoke.cpp` 直接调用 core  
   - 判据：CI 可运行 smoke（先不做框架化）  
9. **更新文档**：`docs/architecture.md` 增加“调用路径/数据流”  
   - 判据：文档能解释一次热键触发后的调用链  
10. **打包与演示**：从 zip 运行，按热键触发 dummy action（日志）  
   - 判据：演示可录屏

---

### C 段（20–40min）：文档/回归（≥3）
1. **画清边界图**：`docs/architecture.md` 必须包含：模块边界 + 禁止依赖列表  
   - 证据：文档可审查  
2. **补一条回归用例**：`manual_test_week3.md` 增加“热键触发 dummy action”  
   - 证据：可勾选  
3. **整理 include 规则**：在 `CONTRIBUTING.md` 增加 3 条（core 不引 UI/Win32）  
   - 证据：贡献规范可回查

---

### 当日停止条件与切换策略
- 触发：接口设计纠结 20 分钟无下一步  
- 立刻动作：切 C，把接口缩小到“只支持 1 个 action 的 execute”，先跑通调用链，再扩展。

**C 类备选清单**
- 写一个“接口最小化”草稿：只保留 `Execute(ActionId)`  
- 把 dummy action 的日志输出与热键触发打通，先证明边界可行  
- 用 clang-tidy 或简单 grep 加一条检查：core/ 不允许出现 windows.h

---

### Day13 当日 DoD
- [ ] core 作为独立 target 可编译  
- [ ] UI→core 调用链跑通（热键触发 dummy action）  
- [ ] `docs/architecture.md` 有边界图与说明  
- [ ] 至少 1 条回归用例补齐

### 风险点与规避
1. **core 变成“万能杂物间”** → 只允许 core 提供“动作/配置/执行”，UI 细节留在 app。  
2. **错误模型不一致** → 先统一为“返回成功/失败 + 可读错误字符串”。  
3. **依赖倒置失败** → 明确“core 不 include windows.h”，违反即 CI fail（后续可加）。

### 记录模板
```md
## Day13 复盘
- 完成了什么：
  - [ ] core 接口文件列表：
  - [ ] UI→core 调用证据：
- 阻塞点：
  - 哪个接口最不确定：
- 明天第一步：
  - Step0（实现 show/hide + focus + ESC）：
- 新增回归/脚手架：
  - [ ] manual_test_week3.md 更新：
- 外部反馈线索：
  - 我想请别人评审 architecture.md 的点：
```

---

## Day14（交互：呼出/隐藏 + 焦点 + ESC）
### 今日目标（1 句）
实现“热键呼出窗口 → 输入框聚焦 → ESC 隐藏 → 再次热键呼出”的交互闭环，并用手测清单固化验证。

### A 段（20–40min）：决策点 + 输出物
**决策点（只做 1 个）：交互 DoD（写死）**  
交互 DoD（建议直接采用）：
1) 热键触发：窗口从隐藏变可见  
2) 窗口可见时：输入框获得焦点可立即输入  
3) 按 ESC：窗口隐藏但进程不退出  
4) 再按热键：窗口再次显示并聚焦  
5) 消息循环不阻塞（持续响应）

**输出物**
- `docs/manual_test_week3.md`（完善为 ≥5 条手测步骤，含预期）

---

### B 段（60–90min）：主 Feature（WIP=1）= show/hide + focus + ESC
#### 实现步骤（建议 10 步）
1. **增加 UI 状态**：维护 `bool is_visible`（或直接用 `IsWindowVisible(hwnd)`）  
   - 判据：状态与窗口实际一致  
2. **热键触发切换显示**：WM_HOTKEY 中调用 `ShowWindow(hwnd, SW_SHOW/SW_HIDE)`  
   - 判据：热键能切换显示/隐藏  
3. **前台与置顶策略 v0**：显示时调用 `SetForegroundWindow`（可选再 `SetWindowPos(HWND_TOPMOST, ...)`）  
   - 判据：窗口显示后能接收键盘输入  
4. **输入控件**：加一个 `Edit` 控件（最小）并保存其 HWND  
   - 判据：窗口内有输入框  
5. **焦点管理**：显示后 `SetFocus(hEdit)` 或在 `WM_ACTIVATE` 中处理  
   - 判据：显示后无需点击即可输入  
6. **ESC 隐藏**：处理 `WM_KEYDOWN`/`WM_CHAR`（或加 accelerator）捕获 VK_ESCAPE 并隐藏窗口  
   - 判据：ESC 隐藏但不退出  
7. **隐藏时焦点处理**：隐藏前可 `ShowWindow(SW_HIDE)`；下次显示再聚焦  
   - 判据：不出现“焦点丢失导致无法输入”的状态  
8. **可观测日志**：记录每次 show/hide、focus、ESC 的事件  
   - 判据：日志可复盘交互路径  
9. **回归脚本**：更新 `scripts/smoke.ps1`（若已有）执行：启动→等待→提示你按热键/ESC（半自动也可）  
   - 判据：手测步骤与脚本一致  
10. **演示打包**：Day05 脚本产出 zip，录屏一次“热键呼出→输入→ESC→再呼出”  
   - 判据：zip 环境下演示通过

---

### C 段（20–40min）：复测/文档/对外动作（≥3）
1. **完成手测清单**：`docs/manual_test_week3.md` ≥5 条，并勾选一次  
   - 证据：清单勾选 + 录屏  
2. **更新 README 的 Week3 Demo 指引**：包含：如何运行、默认热键、演示路径  
   - 证据：README 小节完整  
3. **发布 Week3 Demo 证据**：至少把录屏/gif 放到仓库（或 Release notes）并发一个最小帖子  
   - 证据：链接可访问（GitHub Release/Discussion/社媒其一）

---

### 当日停止条件与切换策略
- 触发：焦点/前台策略反复试错 20 分钟无可控下一步  
- 立刻动作：切 C，把策略降级为“显示后必须手动点击输入框”先确保 show/hide/ESC 完成，再逐步收敛焦点。

**C 类备选清单**
- 写 `docs/focus_strategies.md`：列出尝试过的 API 组合与现象（可复现）  
- 把 focus 处理放到 `WM_ACTIVATE`/`WM_SETFOCUS`，减少“时序猜测”  
- 先取消置顶，仅 SetForegroundWindow，缩小变量

---

### Day14 当日 DoD
- [ ] 热键呼出窗口可用  
- [ ] 输入框自动聚焦可输入（或按降级策略明确写入 DoD/文档）  
- [ ] ESC 隐藏窗口且可再次呼出  
- [ ] `docs/manual_test_week3.md` 完成并跑通  
- [ ] 有可演示证据（录屏/gif）且对外可见至少一次

### 风险点与规避
1. **前台/焦点限制** → 先保证 show/hide/ESC 完成；焦点策略允许 v0 降级并记录。  
2. **消息处理冲突** → 只在必要消息里加逻辑，其他交给 `DefWindowProc`。  
3. **演示不可复现** → 手测清单写“预期现象”，录屏覆盖完整链路。

### 记录模板
```md
## Day14 复盘
- 完成了什么：
  - [ ] show/hide + focus + ESC（证据）：
  - [ ] manual_test_week3.md 勾选情况：
  - [ ] 对外链接：
- 阻塞点：
  - 触发条件 / 现象：
- 明天第一步（若继续 Week3/Week4）：
  - Step0：
- 新增回归用例：
  - [ ] 手测用例新增：
- 外部反馈线索：
  - 收到的反馈 / 下一步要验证的假设：
```

---

# 全局自检（覆盖偏差/前提/验证）
1. **默认假设可能不成立**：例如你没有创建 Release 的权限/组织策略限制。验证方式：Day07 前先手工创建一次草稿 Release，确认权限链路。  
2. **CI 与本机路径差异**：本机 build 输出路径与 runner 不同。验证方式：workflow 内显式列目录并 assert。  
3. **Week3 焦点策略存在系统限制**：Windows 的前台窗口切换策略可能限制 SetForegroundWindow。验证方式：记录每个策略的可复现现象，允许 v0 降级。  

---

# 失败场景清单（至少 3 个，含缓解与备选）
1. **现象：package.ps1 找不到 exe**  
   - 原因：build 输出目录不稳定或 preset 不一致  
   - 缓解：脚本用“搜索规则”定位 exe；同时在脚本打印搜索路径  
   - 备选：在 CMake 加 install 规则，用 `cmake --install` 固化 staging  
2. **现象：CI 绿灯但 artifact 为空**  
   - 原因：上传路径写错或复制步骤未执行  
   - 缓解：上传前 `dir /s` 并 assert 文件存在；为空则 fail-fast  
   - 备选：先直接上传 build 输出目录作为 artifact（缩小变量）  
3. **现象：Release workflow 权限不足/gh 失败**  
   - 原因：permissions 未开 `contents: write` 或 token 未传给 gh  
   - 缓解：显式 permissions；`GH_TOKEN=${{ secrets.GITHUB_TOKEN }}`；日志打印 `gh auth status`  
   - 备选：先用 REST API/`actions/create-release` 方案，但优先保持 gh 方案可控  
4. **现象：RegisterHotKey 成功但收不到 WM_HOTKEY**  
   - 原因：注册线程与消息循环线程不一致，或窗口过程未处理  
   - 缓解：保证注册发生在窗口线程；WndProc 处理 WM_HOTKEY 并日志记录  
   - 备选：先注册到窗口句柄（非 NULL），减少线程歧义  

---

# MRE（最小可复现：用于你或他人复测）
> 目的：任何一天卡住时，都能用这套最小命令复现“构建/打包/CI/热键演示”。

**运行环境（记录版本）**
- Windows 10/11（版本号：______）
- VS2022 / MSVC（版本号：______）
- CMake（版本号：______）
- Git（版本号：______）
- PowerShell（版本号：______）

**核心命令（按顺序）**
```powershell
# 1) 配置（若你使用 configure preset）
cmake --preset vs2022

# 2) 构建
cmake --build --preset vs2022_release

# 3) 打包
powershell -ExecutionPolicy Bypass -File scripts/package.ps1

# 4) 运行（从 build 或从 zip 解压后运行）
.\out\build\vs2022_release\Release\zhiz_tool.exe --help
# 或者双击运行观察窗口

# 5) tag 发布（Day07）
git tag v0.0.1
git push --tags
```

**期望输出（最小）**
- 构建成功；`dist/*.zip` 存在；Release（若执行 Day07）出现并带附件；Week3（Day11–Day14）窗口可演示。

---

# 后续行动建议（3–4 条：收益 + 投入）
1. **把“install/staging”纳入 CMake**：收益是打包与 CI 路径更稳定；投入是补少量 `install(TARGETS ...)` 与 `install(FILES ...)`。  
2. **为 core 增加 1 条可自动运行的 smoke**：收益是 CI 可回归；投入是写一个 `app/cli_smoke` 或最小测试入口。  
3. **把“手测清单”升级为半自动脚本**：收益是跨机复测更稳定；投入是 1 个 PowerShell 脚本 + 明确输出。  
4. **建立反馈闭环**：收益是选题更接近真实需求；投入是每两周固定发帖一次并维护 1 个问题追踪列表。  
