import datetime
import os
import re
import sys
import subprocess
import tkinter as tk
from tkinter import messagebox, ttk

# ======================
# 全局配置 / 常量
# ======================

today = datetime.date.today().strftime("%Y.%m.%d")

BASE_DIR = os.getcwd()
CARDS_DIR = os.path.join(BASE_DIR, "cards")
REVIEWS_DIR = os.path.join(BASE_DIR, "reviews")
INDEX_FILE = os.path.join(BASE_DIR, "index.md")

NOTE_TYPE_LABELS = {
    "card": "概念卡",
    "review": "学习复盘",
}


def ensure_dirs():
    """确保基础目录存在"""
    os.makedirs(CARDS_DIR, exist_ok=True)
    os.makedirs(REVIEWS_DIR, exist_ok=True)


def sanitize_filename(name: str) -> str:
    """清洗非法字符：替换 <>:\"/\\|?* 为空，并把空格转为下划线"""
    invalid_chars = r'[<>:"/\\|?*]'
    name = re.sub(invalid_chars, "", name).strip().replace(" ", "_")
    return name or "unnamed"


def open_with_default_app(path: str):
    """调用系统默认程序打开文件"""
    try:
        if sys.platform.startswith("win"):
            os.startfile(path)  # type: ignore[attr-defined]
        elif sys.platform == "darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])
    except Exception as e:
        messagebox.showerror("错误", f"打开文件失败：\n{path}\n\n{e}")


# ======================
# 模板渲染
# ======================

def render_cpp_template(name: str, md_rel_path: str | None = None) -> str:
    """生成默认的 cpp 模板内容"""
    doc_comment = f"// docs: ./{md_rel_path}" if md_rel_path else ""
    comment_block = doc_comment + ("\n\n" if doc_comment else "")
    return (
        comment_block
        + '#include <iostream>\n'
        '#include <windows.h>\n\n'
        "int main() {\n"
        "    // 1) 设置控制台输出/输入代码页为 UTF-8\n"
        "    SetConsoleOutputCP(CP_UTF8);\n"
        "    SetConsoleCP(CP_UTF8);\n\n"
        f'    std::cout << "Hello from {name} ({today})" << std::endl;\n'
        "    return 0;\n"
        "}\n"
    )


def render_md_content(name: str, note_type: str, cpp_rel_path: str | None) -> str:
    """
    生成 md 内容：
    - note_type = card / review
    - cpp_rel_path: 形如 "cards/对象定义.cpp"，review 时为 None
    """
    header_lines = [
        "---",
        f"title: {name}",
        f"date: {today}",
    ]

    if note_type == "card":
        header_lines.append(f"updated: {today}")
        header_lines.append("kind: card")
        header_lines.append("topic: cpp")
        header_lines.append("version: v1")
        if cpp_rel_path:
            header_lines.append(f"code: [{cpp_rel_path}]")
        else:
            header_lines.append("code: []")
        header_lines.append("tags: [cpp, card]")
        header_lines.append("---")

        # 创建卡片时的时间戳（精确到秒）
        now_ts = datetime.datetime.now().strftime("%Y.%m.%d %H:%M:%S")
        cpp_link_text = os.path.basename(cpp_rel_path) if cpp_rel_path else None
        cpp_link_line = f"*关联代码*: [{cpp_link_text}]({cpp_link_text})" if cpp_link_text else ""
        title_block = f"# {name}\n\n" + (f"{cpp_link_line}\n\n" if cpp_link_line else "")

        body = (
            title_block
            + "### 当前工作定义(v1)\n\n"
            + "（在当前理解下，给出清晰、准确、必要的定义）\n\n"
            + "### 关键属性\n\n"
            + "- （列出该概念必备的 3〜5 条属性）\n\n"
            + "### 典型正例（含代码）\n\n"
            + f"- （关联代码示例：`{cpp_link_text or 'TODO_填入代码路径'}` 等，写明为什么是正例）\n\n"
            + "### 反例 / 易混概念\n\n"
            + "- （列出容易混淆的写法或“不属于该概念”的例子，并说明原因）\n\n"
            + "### 版本记录\n\n"
            + f"- v1（{today}）：第一次整理该概念/主题的定义与属性。\n\n"
            + "### 未解决问题 / 待验证\n\n"
            + "- （写下你还不确定、要在实践中验证的点）\n\n"
            + "### 更新追踪\n\n"
            + f"- {now_ts}：创建卡片。\n"
        )
        return "\n".join(header_lines) + "\n\n" + body

    else:  # review
        header_lines.append("kind: review")
        header_lines.append("topic: cpp/review")
        header_lines.append("version: v1")
        header_lines.append("code: []")
        header_lines.append("tags: [cpp, review]")
        header_lines.append("---")

        body = (
            f"# {name}\n\n"
            "### 今天处理的卡片 / 概念\n\n"
            "- （列出今天重点关注或修改的 cards/<名称>.md）\n\n"
            "### 关键收获 / 新的理解\n\n"
            "- \n\n"
            "### 困惑 / 未解决问题\n\n"
            "- \n\n"
            "### 下一步计划\n\n"
            "- \n"
        )
        return "\n".join(header_lines) + "\n\n" + body


# ======================
# 工具函数
# ======================

def parse_names(raw: str) -> list[str]:
    """解析用户输入的多个名字，做分隔和清洗"""
    cpp_input_converted = (
        raw.replace("；", ";")
        .replace("，", ";")
        .replace(",", ";")
    )
    parts = [
        part.strip()
        for part in cpp_input_converted.replace("\n", ";").split(";")
        if part.strip()
    ]
    cpp_files_raw: list[str] = []
    for item in parts:
        cpp_files_raw.extend([f.strip() for f in item.split() if f.strip()])

    seen = set()
    cpp_files: list[str] = []
    for x in cpp_files_raw:
        clean = sanitize_filename(x)
        if clean not in seen:
            seen.add(clean)
            cpp_files.append(clean)
    return cpp_files


def update_yaml_updated(md_path: str, when: str) -> bool:
    """更新 md 文件 YAML 头里的 updated 字段，没有则插入（用于概念卡）"""
    try:
        with open(md_path, "r", encoding="utf-8") as f:
            text = f.read()
    except Exception as e:
        messagebox.showerror("错误", f"读取 {md_path} 失败：{e}")
        return False

    lines = text.splitlines()
    in_yaml = False
    updated_line_idx = None
    date_line_idx = None
    yaml_end_idx = None

    for i, line in enumerate(lines):
        if line.strip() == "---":
            if not in_yaml:
                in_yaml = True
                continue
            else:
                yaml_end_idx = i
                break
        if in_yaml:
            if line.startswith("updated:"):
                updated_line_idx = i
            if line.startswith("date:"):
                date_line_idx = i

    if not in_yaml or yaml_end_idx is None:
        new_header = [
            "---",
            f"updated: {when}",
            "---",
        ]
        new_text = "\n".join(new_header) + "\n" + text
    else:
        if updated_line_idx is not None:
            lines[updated_line_idx] = f"updated: {when}"
        else:
            if date_line_idx is not None:
                insert_idx = date_line_idx + 1
            else:
                insert_idx = 1
            lines.insert(insert_idx, f"updated: {when}")
        new_text = "\n".join(lines)

    try:
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(new_text)
    except Exception as e:
        messagebox.showerror("错误", f"写回 {md_path} 失败：{e}")
        return False

    return True


def append_update_tracking(md_path: str, when: str, action: str) -> bool:
    """
    在卡片 md 的 `### 更新追踪` 小节末尾追加一条 `- when：action`
    如果小节不存在，则在文件末尾新建该小节。
    """
    try:
        with open(md_path, "r", encoding="utf-8") as f:
            text = f.read()
    except Exception as e:
        messagebox.showerror("错误", f"读取 {md_path} 失败：{e}")
        return False

    marker = "### 更新追踪"
    line_to_add = f"- {when}：{action}\n"

    if marker not in text:
        new_text = (
            text.rstrip()
            + "\n\n"
            + marker
            + "\n\n"
            + line_to_add
        )
    else:
        new_text = text.rstrip() + "\n" + line_to_add

    try:
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(new_text)
    except Exception as e:
        messagebox.showerror("错误", f"写回 {md_path} 失败：{e}")
        return False

    return True


def ensure_md_cpp_link(md_path: str, cpp_filename: str) -> bool:
    """在 md 标题后补充指向同名 cpp 的跳转"""
    link_line = f"*关联代码*: [{cpp_filename}]({cpp_filename})"
    try:
        with open(md_path, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
    except Exception as e:
        messagebox.showerror("错误", f"读取 {md_path} 失败：{e}")
        return False

    joined = "\n".join(lines)
    if link_line in joined:
        return True

    # 跳过 YAML 头，寻找第一个标题行
    idx = 0
    yaml_delims = 0
    while idx < len(lines) and yaml_delims < 2:
        if lines[idx].strip() == "---":
            yaml_delims += 1
        idx += 1

    insert_pos = idx
    for i in range(idx, len(lines)):
        if lines[i].startswith("# "):
            insert_pos = i + 1
            break

    if insert_pos < len(lines) and lines[insert_pos].strip():
        lines.insert(insert_pos, "")
        insert_pos += 1

    lines.insert(insert_pos, link_line)
    lines.insert(insert_pos + 1, "")

    try:
        with open(md_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
    except Exception as e:
        messagebox.showerror("错误", f"写回 {md_path} 失败：{e}")
        return False

    return True


def ensure_cpp_md_comment(cpp_path: str, md_filename: str) -> bool:
    """在 cpp 顶部添加指向 md 的注释"""
    comment_line = f"// docs: ./{md_filename}"
    try:
        with open(cpp_path, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
    except Exception as e:
        messagebox.showerror("错误", f"读取 {cpp_path} 失败：{e}")
        return False

    # 如果已有包含 md 文件名的注释，用新格式替换第一处，避免重复
    for i, line in enumerate(lines[:5]):
        if md_filename in line:
            if comment_line in line:
                return True
            lines[i] = comment_line
            break
    else:
        lines.insert(0, comment_line)
        if len(lines) > 1 and lines[1].strip():
            lines.insert(1, "")

    try:
        with open(cpp_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
    except Exception as e:
        messagebox.showerror("错误", f"写回 {cpp_path} 失败：{e}")
        return False

    return True


# ======================
# 主逻辑（业务）
# ======================

def create_cpp_log():
    """GUI 按钮 / 回车触发的主函数"""

    note_type = note_type_var.get() or "card"  # 默认概念卡
    raw_input = entry_files.get("1.0", tk.END).strip()

    if not raw_input:
        if not messagebox.askyesno("确认", "未输入任何名称，只创建基础目录和 index.md？"):
            return

    ensure_dirs()
    names = parse_names(raw_input) if raw_input else []

    created_entries: list[dict] = []   # 新建 md，用于写 index
    updated_names: list[str] = []      # 概念卡更新
    existing_reviews: list[str] = []   # 已存在的复盘
    open_paths: list[str] = []         # 需要打开的文件路径

    for name in names:
        if note_type == "review":
            # 复盘：文件名带日期前缀，避免跨日冲突
            safe_name = sanitize_filename(name)
            filename = f"{today}_{safe_name}_review.md"
            md_path = os.path.join(REVIEWS_DIR, filename)
            md_rel = os.path.join("reviews", filename).replace("\\", "/")

            if not os.path.exists(md_path):
                # 新建复盘
                try:
                    md_content = render_md_content(name, note_type, cpp_rel_path=None)
                    with open(md_path, "w", encoding="utf-8") as f:
                        f.write(md_content)
                    created_entries.append(
                        {
                            "name": name,
                            "cpp_rel": None,
                            "md_rel": md_rel,
                            "note_type": note_type,
                        }
                    )
                except Exception as e:
                    messagebox.showerror("错误", f"创建 {md_path} 失败：{e}")
                    return
            else:
                # 已存在：记录一下名字，用于最后提示
                existing_reviews.append(name)

            # 无论新建还是已存在，都打开这份复盘
            open_paths.append(md_path)

        else:
            # 概念卡：cards/<name>.cpp + cards/<name>.md
            safe_name = sanitize_filename(name)
            cpp_path = os.path.join(CARDS_DIR, f"{safe_name}.cpp")
            cpp_rel = os.path.join("cards", f"{safe_name}.cpp").replace("\\", "/")
            md_path = os.path.join(CARDS_DIR, f"{safe_name}.md")
            md_rel = os.path.join("cards", f"{safe_name}.md").replace("\\", "/")
            cpp_filename = os.path.basename(cpp_path)
            md_filename = os.path.basename(md_path)

            # cpp：不存在才创建
            if not os.path.exists(cpp_path):
                try:
                    cpp_content = render_cpp_template(name, md_rel_path=md_filename)
                    with open(cpp_path, "w", encoding="utf-8") as f:
                        f.write(cpp_content)
                except Exception as e:
                    messagebox.showerror("错误", f"创建 {cpp_path} 失败：{e}")
                    return

            # md：不存在则新建，存在则更新“更新追踪”+ updated
            if not os.path.exists(md_path):
                try:
                    md_content = render_md_content(name, note_type, cpp_rel_path=cpp_rel)
                    with open(md_path, "w", encoding="utf-8") as f:
                        f.write(md_content)
                    created_entries.append(
                        {
                            "name": name,
                            "cpp_rel": cpp_rel,
                            "md_rel": md_rel,
                            "note_type": note_type,
                        }
                    )
                except Exception as e:
                    messagebox.showerror("错误", f"创建 {md_path} 失败：{e}")
                    return
            else:
                # 精确到秒的时间戳
                now_ts = datetime.datetime.now().strftime("%Y.%m.%d %H:%M:%S")
                action = "脚本记录：今天再次查看/修改此卡片（具体改动请见正文）"
                ok1 = append_update_tracking(md_path, now_ts, action)
                if not ok1:
                    return
                # updated 字段仍然只用“日期”即可
                ok2 = update_yaml_updated(md_path, today)
                if not ok2:
                    return
                updated_names.append(name)

            ok_link_md = ensure_md_cpp_link(md_path, cpp_filename)
            if not ok_link_md:
                return
            ok_link_cpp = ensure_cpp_md_comment(cpp_path, md_filename)
            if not ok_link_cpp:
                return

            # 概念卡：总是打开 cpp + md
            open_paths.append(cpp_path)
            open_paths.append(md_path)

    # 生成 / 更新 index.md（只为“新建”的 md 追加索引）
    if not os.path.exists(INDEX_FILE):
        existing_content = "# C++ 学习日志\n\n"
    else:
        try:
            with open(INDEX_FILE, "r", encoding="utf-8") as f:
                existing_content = f.read()
        except Exception as e:
            messagebox.showerror("错误", f"读取 index.md 失败：{e}")
            return

    lines = existing_content.splitlines()
    date_header = f"## {today}"
    date_line_index = None
    for i, line in enumerate(lines):
        if line.strip() == date_header:
            date_line_index = i
            break

    new_list_lines: list[str] = []
    if created_entries:
        for entry in created_entries:
            name = entry["name"]
            cpp_rel = entry["cpp_rel"]
            md_rel = entry["md_rel"]
            nt = entry["note_type"]
            label = NOTE_TYPE_LABELS.get(nt, "笔记")

            if cpp_rel:
                line = f"- [{name}]({cpp_rel}) | [{label}]({md_rel})"
            else:
                line = f"- [{label}：{name}]({md_rel})"
            new_list_lines.append(line)

    if date_line_index is None:
        if lines and lines[-1].strip() != "":
            lines.append("")
        lines.append(date_header)
        if new_list_lines:
            lines.extend(new_list_lines)
        existing_content = "\n".join(lines) + "\n"
    else:
        start_index = date_line_index
        end_index = len(lines)
        for i in range(date_line_index + 1, len(lines)):
            if lines[i].startswith("## ") and i != date_line_index:
                end_index = i
                break

        current_day_lines = lines[start_index + 1:end_index]
        updated_lines_all = lines[:start_index + 1]
        updated_lines_all.extend(current_day_lines)
        if new_list_lines:
            updated_lines_all.extend(new_list_lines)

        if end_index < len(lines):
            if updated_lines_all and updated_lines_all[-1].strip() != "":
                updated_lines_all.append("")
            updated_lines_all.extend(lines[end_index:])

        existing_content = "\n".join(updated_lines_all)

    try:
        with open(INDEX_FILE, "w", encoding="utf-8") as f:
            f.write(existing_content)
    except Exception as e:
        messagebox.showerror("错误", f"更新 index.md 失败：{e}")
        return

    # 自动打开本次涉及到的文件（去重）
    for path in dict.fromkeys(open_paths):
        if os.path.exists(path):
            open_with_default_app(path)

    # 成功提示
    created_count = len(created_entries)
    updated_count = len(updated_names)
    existing_review_count = len(existing_reviews)
    label = NOTE_TYPE_LABELS.get(note_type, "笔记")

    if note_type == "review":
        if created_count and existing_review_count:
            summary = (
                f"新建 {created_count} 个学习复盘，"
                f"打开 {existing_review_count} 个已存在学习复盘"
            )
        elif created_count:
            summary = f"新建 {created_count} 个学习复盘"
        elif existing_review_count:
            summary = f"未新建学习复盘，仅打开 {existing_review_count} 个已存在学习复盘"
        else:
            summary = "未处理任何学习复盘"
    else:
        summary = (
            f"新建 {created_count} 个{label}（cpp + md），"
            f"更新 {updated_count} 个{label}（md）"
        )

    success_msg = f"成功！\n{today}\n{summary}\n文件与索引已处理完毕！"

    popup = tk.Toplevel(root)
    popup.title("")
    popup.geometry("380x180")
    popup.resizable(False, False)
    popup.configure(bg="#94D1EC")

    tk.Label(
        popup,
        text=success_msg,
        bg="#96D4DF",
        fg="white",
        font=("微软雅黑", 12, "bold"),
        justify="center",
        wraplength=340,
    ).pack(expand=True, padx=10, pady=10)

    popup.update_idletasks()
    x = (popup.winfo_screenwidth() // 2) - (popup.winfo_width() // 2)
    y = (popup.winfo_screenheight() // 2) - (popup.winfo_height() // 2)
    popup.geometry(f"+{x}+{y}")

    popup.after(1800, popup.destroy)
    entry_files.delete("1.0", tk.END)


# ======================
# GUI & main
# ======================

def main():
    global root, note_type_var, entry_files

    root = tk.Tk()
    root.title("枝枝 C++ 学习卡片工厂")
    root.geometry("620x520")
    root.resizable(False, False)

    ttk.Label(
        root,
        text=f"今天是：{today}",
        font=("微软雅黑", 14, "bold"),
        foreground="#2c3e50",
    ).pack(pady=10)

    ttk.Label(
        root,
        text="请输入要创建的条目名称（支持回车、空格、分号、逗号随意分隔）",
        font=("微软雅黑", 10),
    ).pack(pady=(0, 6))

    note_type_frame = ttk.Frame(root)
    note_type_frame.pack(pady=(0, 8))

    ttk.Label(
        note_type_frame,
        text="笔记类型：",
        font=("微软雅黑", 10, "bold"),
    ).pack(side=tk.LEFT, padx=(0, 8))

    note_type_var = tk.StringVar(value="card")

    for value, text in [
        ("card", "概念卡"),
        ("review", "学习复盘"),
    ]:
        ttk.Radiobutton(
            note_type_frame,
            text=text,
            value=value,
            variable=note_type_var,
        ).pack(side=tk.LEFT, padx=4)

    entry_files = tk.Text(
        root,
        height=16,
        width=70,
        font=("Consolas", 11),
        relief="flat",
        bd=2,
    )
    entry_files.pack(padx=30, pady=10)

    ttk.Label(
        root,
        text="· 概念卡：cards/ 下生成固定 md + cpp，一概念一张卡，长期演化\n"
             "· 卡片 md 含 date(创建) + updated(最近更新) + 文末 更新追踪（精确到秒）\n"
             "· 学习复盘：reviews/ 下按日期前缀保存，一天可多条\n",
        foreground="#83abad",
        justify="left",
    ).pack(pady=(0, 15))

    ttk.Button(
        root,
        text="生成文件和索引",
        command=create_cpp_log,
    ).pack(pady=10)

    root.bind("<Return>", lambda e: create_cpp_log())
    entry_files.focus_set()

    root.mainloop()


if __name__ == "__main__":
    main()
