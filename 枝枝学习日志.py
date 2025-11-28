import datetime
import os
import re
import subprocess  # git集成最佳实践
import tkinter as tk
from tkinter import messagebox, ttk

# 今日日期文件夹
today = datetime.date.today().strftime("%Y.%m.%d")
folder_name = today
folder_path = os.path.join(os.getcwd(), folder_name)

def sanitize_filename(name):
    """手动清洗非法字符：基于Stack Overflow 2025大神实践，替换<>:\"/\|?*为空格转_，跨平台稳"""
    invalid_chars = r'[<>:"/\\|?*]'
    name = re.sub(invalid_chars, '', name).strip().replace(' ', '_')
    return name or "unnamed"  # 空转unnamed，防崩

def create_cpp_log():
    cpp_input = entry_files.get("1.0", "end-1c").strip()

    if not cpp_input:
        if not messagebox.askyesno("确认", "没有输入文件名，是否只创建今天的空文件夹？"):
            return

    try:
        os.makedirs(folder_path, exist_ok=True)
    except Exception as e:
        messagebox.showerror("错误", f"创建文件夹失败：{e}")
        return

    # 解析文件名 + 清洗
    cpp_input = cpp_input.replace("；", ";").replace("，", ";").replace(",", ";")
    lines = [line.strip() for line in cpp_input.replace("\n", ";").split(";") if line.strip()]
    cpp_files = []
    for item in lines:
        cpp_files.extend([f.strip() for f in item.split() if f.strip()])
    seen = set()
    cpp_files = [x for x in cpp_files if not (x in seen or seen.add(x))]

    # 生成 cpp 文件（存在跳过）
    for name in cpp_files:
        safe_name = sanitize_filename(name)
        file_path = os.path.join(folder_path, f"{safe_name}.cpp")
        if not os.path.exists(file_path):
            template = f"""#include <iostream>

int main() {{
    std::cout << "Hello from {safe_name} ({today})!" << std::endl;
    // 在这里写今天的练习代码吧～
    return 0;
}}
"""
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(template.lstrip())

    # 每个cpp生成专属 md 文件（同级扁平）
    now = datetime.datetime.now().strftime('%H:%M:%S')
    for name in cpp_files:
        safe_name = sanitize_filename(name)
        md_path = os.path.join(folder_path, f"{safe_name}.md")
        if os.path.exists(md_path):
            # 存在：追加新分段历史
            with open(md_path, "a", encoding="utf-8") as f:
                f.write(f"\n## 更新于 {now}\n（在这里添加新笔记～）\n")
        else:
            # 新创建 + YAML frontmatter
            content = f"""---
tags: [c++, learning]  # 可手动加标签，Obsidian搜索神器
date: {today}
---

# {safe_name}.cpp 练习记录

## 代码说明
// 这里放你的cpp代码摘要或关键点

## 学习笔记 / 总结 / bug调试
- 创建于 {now}
（在这里写你的想法～）
"""
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(content)

    # 更新 index.md：高效内存替换
    index_file = "index.md"
    if not os.path.exists(index_file):
        with open(index_file, "w", encoding="utf-8") as f:
            f.write("# C++ 学习日志\n\n")

    try:
        with open(index_file, "r", encoding="utf-8") as f:
            existing_content = f.read()
    except Exception as e:
        messagebox.showerror("错误", f"读取 index.md 失败：{e}")
        return

    lines = existing_content.split('\n')
    start_index = -1
    for i, line in enumerate(lines):
        if re.match(r'^## \d{4}\.\d{2}\.\d{2}$', line.strip()) and line.strip() == f'## {today}':
            start_index = i
            break

    actual_files = [f[:-4] for f in os.listdir(folder_path) if f.endswith(".cpp")]
    new_list = [f"- [{name}]({folder_name}\\{name}.cpp) | [笔记]({folder_name}\\{name}.md)" for name in actual_files]

    if start_index == -1:
        new_content = f"\n## {today}\n\n" + '\n'.join(new_list) + '\n'
        existing_content += new_content
    else:
        end_index = len(lines)
        for j in range(start_index + 1, len(lines)):
            if re.match(r'^## \d{4}\.\d{2}\.\d{2}$', lines[j].strip()):
                end_index = j
                break
        updated_lines = lines[:start_index + 2] + new_list + lines[end_index:]
        existing_content = '\n'.join(updated_lines)

    try:
        with open(index_file, "w", encoding="utf-8") as f:
            f.write(existing_content)
    except Exception as e:
        messagebox.showerror("错误", f"更新 index.md 失败：{e}")
        return

    # git commit：安全集成，捕获异常
    try:
        subprocess.run(["git", "add", "."], cwd=os.getcwd(), check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", f"Update C++ logs for {today}"], cwd=os.getcwd(), check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass  # git不存在或失败，安静跳过

    # 成功提示
    actual_count = len(actual_files)
    success_msg = f"成功！\n{folder_name}\n共 {actual_count} 个 cpp & md\n扁平高效，git已备份！"
    popup = tk.Toplevel(root)
    popup.title("")
    popup.geometry("360x140")
    popup.resizable(False, False)
    popup.configure(bg="#27ae60")
    tk.Label(popup, text=success_msg, bg="#27ae60", fg="white",
             font=("微软雅黑", 12, "bold"), justify="center").pack(expand=True)
    popup.update_idletasks()
    x = (popup.winfo_screenwidth() // 2) - (popup.winfo_width() // 2)
    y = (popup.winfo_screenheight() // 2) - (popup.winfo_height() // 2)
    popup.geometry(f"+{x}+{y}")
    root.after(700, popup.destroy)
    root.after(700, root.destroy)

# GUI
root = tk.Tk()
root.title("C++ 每日练习一键生成")
root.geometry("560x420")
root.resizable(False, False)

ttk.Label(root, text=f"今天是：{today}", font=("微软雅黑", 14, "bold"), foreground="#2c3e50").pack(pady=20)
ttk.Label(root, text="请输入今天的 cpp 文件名（支持回车、空格、分号、逗号随意分隔）",
          font=("微软雅黑", 10)).pack(pady=(0, 8))

entry_files = tk.Text(root, height=14, width=60, font=("Consolas", 11), relief="flat", bd=2)
entry_files.pack(padx=30, pady=10)

ttk.Label(root, text="扁平高效，YAML/git加持，非法名自动清洗～", 
          foreground="#7f8c8d").pack(pady=(0, 15))

ttk.Button(root, text="立刻生成今日文件夹和文件", command=create_cpp_log).pack(pady=10)

root.bind("<Return>", lambda e: create_cpp_log())
entry_files.focus_set()  # 自动焦点

root.mainloop()
