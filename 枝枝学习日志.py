import datetime
import os
import re
import tkinter as tk
from tkinter import messagebox, ttk

# 今日日期文件夹
today = datetime.date.today().strftime("%Y.%m.%d")
folder_name = today
folder_path = os.path.join(os.getcwd(), folder_name)

def sanitize_filename(name):
    """手动清洗非法字符：替换 <>:\"/\\|?* 为空，并把空格转为下划线"""
    invalid_chars = r'[<>:"/\\|?*]'
    name = re.sub(invalid_chars, '', name).strip().replace(' ', '_')
    return name or "unnamed"

def create_cpp_log():
    cpp_input = entry_files.get("1.0", tk.END).strip()

    if not cpp_input:
        if not messagebox.askyesno("确认", "未输入任何文件名，只创建今日文件夹和 index.md？"):
            return

    # 创建日期文件夹
    try:
        os.makedirs(folder_path, exist_ok=True)
    except Exception as e:
        messagebox.showerror("错误", f"创建文件夹失败：{e}")
        return

    # 解析文件名 + 清洗
    cpp_input_converted = cpp_input.replace("；", ";").replace("，", ";").replace(",", ";")
    parts = [part.strip() for part in cpp_input_converted.replace("\n", ";").split(";") if part.strip()]
    cpp_files_raw = []
    for item in parts:
        cpp_files_raw.extend([f.strip() for f in item.split() if f.strip()])

    seen = set()
    cpp_files = []
    for x in cpp_files_raw:
        clean = sanitize_filename(x)
        if clean not in seen:
            seen.add(clean)
            cpp_files.append(clean)

    actual_files = []
    duplicates = []

    # 为每个 cpp 文件生成文件和 md 笔记
    for name in cpp_files:
        cpp_path = os.path.join(folder_path, f"{name}.cpp")
        md_path = os.path.join(folder_path, f"{name}.md")

        if os.path.exists(cpp_path) and os.path.exists(md_path):
            duplicates.append(name)
            continue

        if not os.path.exists(cpp_path):
            try:
                with open(cpp_path, "w", encoding="utf-8") as f:
                    f.write(
                        '#include <iostream>\n\n'
                        'int main() {\n'
                        f'    std::cout << "Hello from {name} ({today})" << std::endl;\n'
                        '    return 0;\n'
                        '}\n'
                    )
            except Exception as e:
                messagebox.showerror("错误", f"创建 {cpp_path} 失败：{e}")
                return

        if not os.path.exists(md_path):
            try:
                with open(md_path, "w", encoding="utf-8") as f:
                    f.write(
                        "---\n"
                        f"title: {name}\n"
                        f"date: {today}\n"
                        "tags: [cpp, practice]\n"
                        "---\n\n"
                        f"# {name}\n\n"
                        "## 代码说明\n\n"
                        "（这里写这段代码要解决什么问题、关键点是什么）\n\n"
                        "## 学习笔记\n\n"
                        "（记录遇到的坑、思路变化、调试过程和总结）\n"
                    )
            except Exception as e:
                messagebox.showerror("错误", f"创建 {md_path} 失败：{e}")
                return
        else:
            try:
                with open(md_path, "a", encoding="utf-8") as f:
                    f.write(f"\n\n---\n更新于 {today} 再次练习 {name}\n")
            except Exception as e:
                messagebox.showerror("错误", f"更新 {md_path} 失败：{e}")
                return

        actual_files.append(name)

    if duplicates:
        messagebox.showinfo("提示", "以下文件已存在对应的 cpp 和 md，未作修改：\n" + "\n".join(duplicates))
        if not actual_files:
            return

    # 生成 / 更新 index.md
    index_file = os.path.join(os.getcwd(), "index.md")
    if not os.path.exists(index_file):
        existing_content = "# C++ 学习日志\n\n"
    else:
        try:
            with open(index_file, "r", encoding="utf-8") as f:
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

    new_list_lines = []
    if actual_files:
        for name in actual_files:
            cpp_rel = f"{folder_name}/{name}.cpp"
            md_rel = f"{folder_name}/{name}.md"
            new_list_lines.append(f"- [{name}]({cpp_rel}) | [笔记]({md_rel})")

    if date_line_index is None:
        if lines and lines[-1].strip() != "":
            lines.append("")
        lines.append(date_header)
        lines.extend(new_list_lines)
        existing_content = "\n".join(lines) + "\n"
    else:
        start_index = date_line_index
        end_index = len(lines)
        for i in range(date_line_index + 1, len(lines)):
            if lines[i].startswith("## ") and i != date_line_index:
                end_index = i
                break
        updated_lines = lines[:start_index + 1]
        updated_lines.extend(new_list_lines)
        if end_index < len(lines):
            if updated_lines and updated_lines[-1].strip() != "":
                updated_lines.append("")
            updated_lines.extend(lines[end_index:])
        existing_content = "\n".join(updated_lines)

    try:
        with open(index_file, "w", encoding="utf-8") as f:
            f.write(existing_content)
    except Exception as e:
        messagebox.showerror("错误", f"更新 index.md 失败：{e}")
        return

    # 成功提示
    actual_count = len(actual_files)
    success_msg = f"成功！\n{folder_name}\n共 {actual_count} 个 cpp & md\n文件与索引已生成！"

    popup = tk.Toplevel(root)
    popup.title("")
    popup.geometry("360x140")
    popup.resizable(False, False)
    popup.configure(bg="#94D1EC")

    tk.Label(
        popup,
        text=success_msg,
        bg="#96D4DF",
        fg="white",
        font=("微软雅黑", 12, "bold"),
        justify="center"
    ).pack(expand=True)

    popup.update_idletasks()
    x = (popup.winfo_screenwidth() // 2) - (popup.winfo_width() // 2)
    y = (popup.winfo_screenheight() // 2) - (popup.winfo_height() // 2)
    popup.geometry(f"+{x}+{y}")

    popup.after(1500, popup.destroy)
    entry_files.delete("1.0", tk.END)

# GUI
root = tk.Tk()
root.title("C++ 每日练习一键生成")
root.geometry("560x420")
root.resizable(False, False)

ttk.Label(
    root,
    text=f"今天是：{today}",
    font=("微软雅黑", 14, "bold"),
    foreground="#2c3e50"
).pack(pady=20)

ttk.Label(
    root,
    text="请输入今天的 cpp 文件名（支持回车、空格、分号、逗号随意分隔）",
    font=("微软雅黑", 10)
).pack(pady=(0, 8))

entry_files = tk.Text(
    root,
    height=14,
    width=60,
    font=("Consolas", 11),
    relief="flat",
    bd=2
)
entry_files.pack(padx=30, pady=10)

ttk.Label(
    root,
    text="扁平高效，YAML索引加持，非法名自动清洗～",
    foreground="#7f8c8d"
).pack(pady=(0, 15))

ttk.Button(
    root,
    text="立刻生成今日文件夹和文件",
    command=create_cpp_log
).pack(pady=10)

root.bind("<Return>", lambda e: create_cpp_log())
entry_files.focus_set()

root.mainloop()
