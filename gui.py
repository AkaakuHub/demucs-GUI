import tkinter as tk
from tkinter import filedialog
import subprocess
import threading
import json
import os

VERSION = "ver 1.0"

with open("config.json", "r") as json_file:
    data = json.load(json_file)
OPENDIR = data["OPENDIR"]
SAVEDIR = data["SAVEDIR"]
CWD = os.getcwd()
stopSrc = False
isRunning = False


def run_command(command):
    global isRunning
    try:
        isRunning = True
        run_show.configure(text="True")
        run_frame.configure(bg="Red")
        run_label.configure(bg="Red")
        path_text.configure(state="disabled")
        results_text.configure(state="normal")
        results_text.insert(tk.END, f"{CWD}>" + command + "\n")
        process = subprocess.Popen(
            command,
            shell=True,
            text=True,
            stderr=subprocess.STDOUT,  # 進捗バーのため
            stdout=subprocess.PIPE,
            encoding="utf-8",
            errors="ignore",
        )

        pre_line = ""
        for line in process.stdout:
            if "seconds/s" in line:
                results_text.delete(tk.END + f"-{len(pre_line) + 1}c", tk.END)
                results_text.insert(tk.END, "\n" + line)
                pre_line = line
            else:
                results_text.insert(tk.END, line)

            if stopSrc == False:
                results_text.see(tk.END)

        process.wait()

    except subprocess.CalledProcessError as e:
        results_text.insert(tk.END, f"Error: {e.output}\n")

    isRunning = False
    run_show.configure(text="False")
    run_frame.configure(bg="aquamarine")
    run_label.configure(bg="aquamarine")
    path_text.configure(state="normal")
    results_text.configure(state="disabled")
    notification_label.configure(text="")


def Scrolling():
    global stopSrc
    if stopSrc == True:
        stopScr_button.configure(text="スクロール停止")
        stopSrc = False
        results_text.see(tk.END)
        stopScr_state.configure(text="")
    else:
        stopScr_button.configure(text="スクロール再開")
        stopSrc = True
        stopScr_state.configure(text="スクロール停止中")


def execute_command(kind):
    global results_text
    global isRunning
    if isRunning:
        notification_label.configure(text="他のコマンドが実行中です")
        return
    else:
        results_text.see(tk.END)
        file = path_text.get("1.0", tk.END).strip().replace("/", "\\")
        bitrate = bitrate_entry.get()
        isol = isol_entry.get()
        if kind == 1:
            command = f'demucs --mp3 --mp3-bitrate {bitrate} "{file}"'
        elif kind == 2:
            command = f'demucs --mp3 --mp3-bitrate {bitrate} -n htdemucs_6s "{file}"'
        elif kind == 3:
            command = (
                f'demucs --mp3 --mp3-bitrate {bitrate} "{file}" --two-stems={isol}'
            )
        elif kind == 4:
            command = f'demucs --mp3 --mp3-bitrate {bitrate} -n htdemucs_ft "{file}"'
        elif kind == 5:
            command = f'demucs --mp3 --mp3-bitrate {bitrate} -n hdemucs_mmi "{file}"'
        elif kind == 6:
            command = f'demucs --mp3 --mp3-bitrate {bitrate} -n mdx "{file}"'
        elif kind == 7:
            command = f'demucs --mp3 --mp3-bitrate {bitrate} -n mdx_extra "{file}"'
        elif kind == 8:
            command = f'demucs --mp3 --mp3-bitrate {bitrate} -n mdx_q "{file}"'
        elif kind == 9:
            command = f'demucs --mp3 --mp3-bitrate {bitrate} -n mdx_extra_q "{file}"'
        elif kind == 10:
            command = "demucs " + own_entry.get()

        # コマンド実行を非同期に行うためのスレッドを開始
        thread = threading.Thread(target=run_command, args=(command,))
        thread.start()


def select_file():
    typ = [
        ("音声ファイル", "*.mp3;*.wav;*.m4a;*.aac;*.flac;*.ogg;*.wma"),
        ("すべてのファイル", "*.*"),
    ]
    file = filedialog.askopenfilename(
        filetypes=typ, initialdir=OPENDIR, title="ファイルを選択"
    )
    if file:
        path_text.delete("1.0", tk.END)
        path_text.insert(tk.END, file)


def open_savedir():
    os.startfile(SAVEDIR)


# GUIの設定
root = tk.Tk()
root.title("demucsコマンド実行GUI")
# root.attributes("-fullscreen", True)
root.geometry("1920x1080")

wrapper = tk.Frame(root, padx=5, pady=5, width=700, height=600, bg="gray100")
wrapper.pack()

############################################

input_frame = tk.Frame(wrapper, padx=5, pady=5, width=350, bg="gray100")
input_frame.pack(side=tk.LEFT)

# title
title_frame = tk.Frame(
    input_frame, padx=5, pady=5, bg="LightGreen", relief=tk.GROOVE, bd=5
)
title_frame.pack(anchor=tk.N)
title_label = tk.Label(
    title_frame, text="demucsコマンド実行GUI", font=("Arial", 22), anchor=tk.W, bg="LightGreen"
)
title_label.pack(side=tk.LEFT)

version = tk.Label(input_frame, text=f"{VERSION}", font=("Arial", 16), bg="gray100")
version.pack()

br = tk.Label(input_frame, text="\n", font=("Arial", 16), bg="gray100")
br.pack()

# ファイル選択欄
select_frame = tk.Frame(
    input_frame, padx=5, pady=5, bg="LightPink", relief=tk.RIDGE, bd=5
)
select_frame.pack(anchor=tk.W)
select_button_1 = tk.Button(
    select_frame,
    text="ファイルを選択",
    command=lambda: select_file(),
    font=("Arial", 12),
    bg="gray100",
)
select_button_1.pack(side=tk.LEFT)
select_label = tk.Label(
    select_frame, text="または", font=("Arial", 16), anchor=tk.W, bg="LightPink"
)
select_label.pack(side=tk.LEFT)

# パス表示/入力欄
path_frame = tk.Frame(
    input_frame, padx=5, pady=5, bg="LightPink", relief=tk.RIDGE, bd=5
)
path_frame.pack(anchor=tk.W)
path_text = tk.Text(
    path_frame, height=1, width=40, font=("Arial", 12), wrap=tk.WORD, bg="White"
)
path_text.pack(side=tk.LEFT)

br = tk.Label(input_frame, text="\n", font=("Arial", 16), bg="gray100")
br.pack()

# bitrate入力欄
bitrate_frame = tk.Frame(
    input_frame, padx=5, pady=5, bg="alice blue", relief=tk.RIDGE, bd=5
)
bitrate_frame.pack(anchor=tk.W)
bitrate_label = tk.Label(
    bitrate_frame, text="mp3-bitrate", font=("Arial", 16), anchor=tk.W, bg="alice blue"
)
bitrate_label.pack(side=tk.LEFT)
bitrate_entry = tk.Entry(bitrate_frame, width=10, justify=tk.CENTER, bg="White")
bitrate_entry.pack(side=tk.LEFT)

bitrate_entry.insert(0, "128000")


# isol入力欄
isol_frame = tk.Frame(
    input_frame, padx=5, pady=5, bg="alice blue", relief=tk.RIDGE, bd=5
)
isol_frame.pack(anchor=tk.W)
isol_label = tk.Label(
    isol_frame, text="特定のトラック", font=("Arial", 16), anchor=tk.W, bg="alice blue"
)
isol_label.pack(side=tk.LEFT)
isol_entry = tk.Entry(isol_frame, width=10, justify=tk.CENTER, bg="White")
isol_entry.pack(side=tk.LEFT)

isol_entry.insert(0, "vocals")

br = tk.Label(input_frame, text="\n", font=("Arial", 16), bg="gray100")
br.pack()

# isRunning欄
run_frame = tk.Frame(
    input_frame, padx=5, pady=5, bg="aquamarine", relief=tk.RIDGE, bd=5
)
run_frame.pack(anchor=tk.W)
run_label = tk.Label(
    run_frame, text="isRunning", font=("Arial", 16), anchor=tk.W, bg="aquamarine"
)
run_label.pack(side=tk.LEFT)
run_show = tk.Label(
    run_frame, height=1, width=10, text="False", font=("Arial", 24), bg="White"
)
run_show.pack(side=tk.LEFT)

br = tk.Label(input_frame, text="\n", font=("Arial", 16), bg="gray100")
br.pack()

# stopScrolling
stopScr_frame = tk.Frame(
    input_frame, padx=5, pady=5, bg="LightGoldenrod1", relief=tk.RIDGE, bd=5
)
stopScr_frame.pack(anchor=tk.W)
stopScr_button = tk.Button(
    stopScr_frame,
    text="スクロール停止",
    command=lambda: Scrolling(),
    font=("Arial", 12),
    bg="gray100",
)
stopScr_button.pack(side=tk.LEFT)

stopScr_state = tk.Label(
    stopScr_frame, text="", font=("Arial", 16), bg="LightGoldenrod1"
)
stopScr_state.pack()

br = tk.Label(input_frame, text="\n", font=("Arial", 4), bg="gray100")
br.pack()

# フォルダ開く
save_frame = tk.Frame(
    input_frame, padx=5, pady=5, bg="LightSlateBlue", relief=tk.RIDGE, bd=5
)
save_frame.pack(anchor=tk.W)
save_button = tk.Button(
    save_frame,
    text="フォルダを開く",
    command=lambda: open_savedir(),
    font=("Arial", 12),
    bg="gray100",
)
save_button.pack(side=tk.LEFT)

br = tk.Label(input_frame, text="\n", font=("Arial", 4), bg="gray100")
br.pack()


# notification欄
notification_frame = tk.Frame(input_frame, padx=5, pady=5, bg="gray100", bd=5)
notification_frame.pack(anchor=tk.W)
notification_label = tk.Label(
    notification_frame, text="", font=("Arial", 16), anchor=tk.W, bg="gray100"
)
notification_label.pack(side=tk.LEFT)

############################################

button_frame = tk.Frame(wrapper, padx=5, pady=5, width=350, bg="gray100")
button_frame.pack(side=tk.RIGHT)

# ボタン1
frame1 = tk.Frame(button_frame, padx=5, pady=5, bg="gray100")
frame1.pack(anchor=tk.W)
execute_button_1 = tk.Button(
    frame1,
    text="実行",
    command=lambda: execute_command(1),
    font=("Arial", 12),
    bg="gray100",
)
execute_button_1.pack(side=tk.LEFT)
text_label1 = tk.Label(
    frame1, text="htdemucs", font=("Arial", 12), anchor=tk.W, bg="gray100"
)
text_label1.pack(side=tk.LEFT)
desc1 = tk.Label(
    frame1,
    text="bass, drums, other, vocalsの4つに分ける通常バージョンです。",
    font=("Arial", 10),
    anchor=tk.W,
    bg="gray100",
)
desc1.pack(side=tk.LEFT)

# ボタン2
frame2 = tk.Frame(button_frame, padx=5, pady=5, bg="gray100")
frame2.pack(anchor=tk.W)
execute_button_2 = tk.Button(
    frame2,
    text="実行",
    command=lambda: execute_command(2),
    font=("Arial", 12),
    bg="gray100",
)
execute_button_2.pack(side=tk.LEFT)
text_label2 = tk.Label(
    frame2, text="htdemucs_6s", font=("Arial", 12), anchor=tk.W, bg="gray100"
)
text_label2.pack(side=tk.LEFT)
desc2 = tk.Label(
    frame2,
    text="htdemucsに加えて、guitar, pianoの2つが増えたバージョンです。",
    font=("Arial", 10),
    anchor=tk.W,
    bg="gray100",
)
desc2.pack(side=tk.LEFT)


# ボタン3
frame3 = tk.Frame(button_frame, padx=5, pady=5, bg="gray100")
frame3.pack(anchor=tk.W)
execute_button_3 = tk.Button(
    frame3,
    text="実行",
    command=lambda: execute_command(3),
    font=("Arial", 12),
    bg="gray100",
)
execute_button_3.pack(side=tk.LEFT)
text_label3 = tk.Label(frame3, text="--two-stems", font=("Arial", 12), bg="gray100")
text_label3.pack(side=tk.LEFT)
desc3 = tk.Label(
    frame3,
    text="「特定のトラック」欄に入力したものと、それ以外に分けるバージョンです。(つまりvocalsならカラオケ)",
    font=("Arial", 10),
    anchor=tk.W,
    bg="gray100",
)
desc3.pack(side=tk.LEFT)


# ボタン4
frame4 = tk.Frame(button_frame, padx=5, pady=5, bg="gray100")
frame4.pack(anchor=tk.W)
execute_button_4 = tk.Button(
    frame4,
    text="実行",
    command=lambda: execute_command(4),
    font=("Arial", 12),
    bg="gray100",
)
execute_button_4.pack(side=tk.LEFT)
text_label4 = tk.Label(frame4, text="htdemucs_ft", font=("Arial", 12), bg="gray100")
text_label4.pack(side=tk.LEFT)
desc4 = tk.Label(
    frame4,
    text="htdemucsより時間がかかるが、少し性能が良いバージョンです。",
    font=("Arial", 10),
    anchor=tk.W,
    bg="gray100",
)
desc4.pack(side=tk.LEFT)


# ボタン5
frame5 = tk.Frame(button_frame, padx=5, pady=5, bg="gray100")
frame5.pack(anchor=tk.W)
execute_button_5 = tk.Button(
    frame5,
    text="実行",
    command=lambda: execute_command(5),
    font=("Arial", 12),
    bg="gray100",
)
execute_button_5.pack(side=tk.LEFT)
text_label5 = tk.Label(frame5, text="hdemucs_mmi", font=("Arial", 12), bg="gray100")
text_label5.pack(side=tk.LEFT)


# ボタン6
frame6 = tk.Frame(button_frame, padx=5, pady=5, bg="gray100")
frame6.pack(anchor=tk.W)
execute_button_6 = tk.Button(
    frame6,
    text="実行",
    command=lambda: execute_command(6),
    font=("Arial", 12),
    bg="gray100",
)
execute_button_6.pack(side=tk.LEFT)
text_label6 = tk.Label(frame6, text="mdx", font=("Arial", 12), bg="gray100")
text_label6.pack(side=tk.LEFT)


# ボタン7
frame7 = tk.Frame(button_frame, padx=5, pady=5, bg="gray100")
frame7.pack(anchor=tk.W)
execute_button_7 = tk.Button(
    frame7,
    text="実行",
    command=lambda: execute_command(7),
    font=("Arial", 12),
    bg="gray100",
)
execute_button_7.pack(side=tk.LEFT)
text_label7 = tk.Label(frame7, text="mdx_extra", font=("Arial", 12), bg="gray100")
text_label7.pack(side=tk.LEFT)


# ボタン8
frame8 = tk.Frame(button_frame, padx=5, pady=5, bg="gray100")
frame8.pack(anchor=tk.W)
execute_button_8 = tk.Button(
    frame8,
    text="実行",
    command=lambda: execute_command(8),
    font=("Arial", 12),
    bg="gray100",
)
execute_button_8.pack(side=tk.LEFT)
text_label8 = tk.Label(frame8, text="mdx_q", font=("Arial", 12), bg="gray100")
text_label8.pack(side=tk.LEFT)


# ボタン9
frame9 = tk.Frame(button_frame, padx=5, pady=5, bg="gray100")
frame9.pack(anchor=tk.W)
execute_button_9 = tk.Button(
    frame9,
    text="実行",
    command=lambda: execute_command(9),
    font=("Arial", 12),
    bg="gray100",
)
execute_button_9.pack(side=tk.LEFT)
text_label9 = tk.Label(frame9, text="mdx_extra_q", font=("Arial", 12), bg="gray100")
text_label9.pack(side=tk.LEFT)


# ボタン10
frame10 = tk.Frame(button_frame, padx=5, pady=5, bg="gray100")
frame10.pack(anchor=tk.W)
execute_button_10 = tk.Button(
    frame10,
    text="実行",
    command=lambda: execute_command(10),
    font=("Arial", 12),
    bg="gray100",
)
execute_button_10.pack(side=tk.LEFT)
text_label10 = tk.Label(frame10, text="任意コード demucs ", font=("Arial", 12), bg="gray100")
text_label10.pack(side=tk.LEFT)
own_entry = tk.Entry(frame10, width=140, bg="White")
own_entry.pack(side=tk.LEFT)

own_entry.insert(0, "自信がない限り使用しないでください")

####################

results_text = tk.Text(button_frame, width=140, height=25, bg="black", fg="white")
results_text.pack(fill=tk.BOTH, expand=True)

results_text.configure(state="disabled")

# GUIループの開始
root.mainloop()
