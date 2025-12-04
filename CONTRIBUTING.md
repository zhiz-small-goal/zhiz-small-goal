# 枝枝个人学习仓库

## 仓库用途
1，机会枝枝个人成长
2，方便后续复习整理

## Git 提交信息规范（Conventional Commits）

采用格式：`<type>(<scope>): <subject>`

- 常用 type：
  - `feat`   新增功能或重要内容
  - `fix`    修复错误（包括文档、示例中的错误）
  - `docs`   仅修改文档（Markdown、注释）
  - `refactor` 重构示例代码，不改变行为
  - `chore`  其他与学习内容无关的杂项

- scope 示例：
  - `heap`           堆、存储期相关内容
  - `pointer`        指针与智能指针
  - `build`          构建相关

- 示例：
  - `docs(heap): 修正存储期的定义，贴近标准术语`
  - `fix(example): 修复 double delete 示例中的错误`
  - `feat(pointer): 增加 shared_ptr/unique_ptr 对比示例`

## 贡献流程

1. 发现问题或想补充内容
   - 优先检查 notes/ 中是否已有相关小节，避免重复。
   - 如是修正定义，优先修改“权威定义”所在位置。

2. 修改与自测
   - 对文档：检查术语一致性、链接是否正确。
   - 对代码：确保示例可以在 README 指定环境中编译运行。

3. 提交
   - 使用约定的 commit 信息格式（见上文）。
   - 每个 commit 尽量聚焦一个主题（例如“修正文档定义”“补充示例”分成两个提交）。

4. （可选）Pull Request
   - 若未来对外开放贡献：在此说明 PR 模板、评审预期等。
