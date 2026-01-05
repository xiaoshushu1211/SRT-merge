import tkinter as tk
from tkinter import filedialog
from pathlib import Path

def read_srt(path):
    text = Path(path).read_text(encoding="utf-8-sig")
    text = text.replace("\r\n", "\n").replace("\r", "\n").strip()
    blocks = text.split("\n\n")

    entries = []
    for block in blocks:
        lines = [line for line in block.split("\n") if line.strip()]
        if len(lines) < 3:
            continue
        index = lines[0].strip()
        time_line = lines[1].strip()
        subtitle_text = "\n".join(lines[2:]).strip()
        entries.append((index, time_line, subtitle_text))
    return entries


def merge_srt(cn_file, en_file):
    cn_entries = read_srt(cn_file)
    en_entries = read_srt(en_file)

    # 自动输出文件名：原文件名 + TT
    cn_path = Path(cn_file)
    out_file = cn_path.with_name(cn_path.stem + "TT.srt")

    merged_blocks = []
    for i, (cn, en) in enumerate(zip(cn_entries, en_entries), start=1):
        _, cn_time, cn_text = cn
        _, en_time, en_text = en

        merged_text = f"{cn_text}\n{en_text}"
        block = f"{i}\n{cn_time}\n{merged_text}"
        merged_blocks.append(block)

    out_content = "\n\n".join(merged_blocks) + "\n\n"
    out_file.write_text(out_content, encoding="utf-8")

    print(f"生成完成：{out_file}")
    return out_file


def choose_and_run():
    root = tk.Tk()
    root.withdraw()

    print("请选择译文字幕文件（cn.srt）")
    cn_file = filedialog.askopenfilename(title="选择译文字幕文件", filetypes=[("SRT 字幕", "*.srt")])
    if not cn_file:
        print("未选择译文文件，退出。")
        return

    print("请选择原文字幕文件（en.srt）")
    en_file = filedialog.askopenfilename(title="选择原文字幕文件", filetypes=[("SRT 字幕", "*.srt")])
    if not en_file:
        print("未选择原文文件，退出。")
        return

    out_file = merge_srt(cn_file, en_file)
    print("字幕合并成功！输出文件：", out_file)


if __name__ == "__main__":
    choose_and_run()
