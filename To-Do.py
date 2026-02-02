import tkinter as tk
from tkinter import ttk, messagebox

root = tk.Tk()
root.title("To-Do List")

APP_W, APP_H = 560, 680
screen_w = root.winfo_screenwidth()
screen_h = root.winfo_screenheight()
x = (screen_w - APP_W) // 2
y = (screen_h - APP_H) // 2
root.geometry(f"{APP_W}x{APP_H}+{x}+{y}")

BG = "#F7F1E5"
CARD = "#FDF7EC"
CARD_BORDER = "#E6DCCB"
TEXT = "#2B2B2B"
ACCENT = "#E08E79"
ACCENT_DARK = "#C97463"

root.configure(bg=BG)

input_frame = ttk.Frame(root)
input_frame.pack(pady=12)

task_entry = ttk.Entry(input_frame, width=35, font=("Segoe UI", 12))
task_entry.pack(side=tk.LEFT, padx=(0, 8))

tasks_container = tk.Frame(root, bg=BG)
tasks_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

ROW_H = 54
ROW_PAD = 10
tasks = []

def layout_tasks():
    y = 0
    for t in tasks:
        t["y"] = y
        t["row"].place(x=0, y=y, width=APP_W - 40, height=ROW_H)
        y += ROW_H + ROW_PAD

def animate_reflow(targets, duration_ms=180, step_ms=15):
    steps = max(1, duration_ms // step_ms)
    for t in targets:
        if "y" not in t:
            t["y"] = 0
        t["start_y"] = t["y"]
        t["dy"] = (t["target_y"] - t["start_y"]) / steps

    def step(i=0):
        done = (i >= steps)
        for t in targets:
            if done:
                t["y"] = t["target_y"]
            else:
                t["y"] = t["start_y"] + t["dy"] * (i + 1)
            t["row"].place(x=0, y=int(t["y"]), width=APP_W - 40, height=ROW_H)
        if not done:
            root.after(step_ms, lambda: step(i + 1))

    step()

def animate_slide_out(row, on_done):
    start_x = 0
    end_x = APP_W
    steps = 18
    dx = max(1, (end_x - start_x) // steps)

    def step(x):
        row.place(x=x)
        if x < end_x:
            row.after(15, lambda: step(x + dx))
        else:
            on_done()

    step(start_x)

def add_task():
    text = task_entry.get().strip()
    if not text:
        return

    row = tk.Frame(tasks_container, bg=CARD, padx=8, pady=6, highlightthickness=1, highlightbackground=CARD_BORDER)
    row.place(x=0, y=0)

    var = tk.BooleanVar(value=False)

    def on_check():
        if var.get():
            messagebox.showinfo("Nice!", "Congrats! Task completed.")

            def finish_remove():
                tasks[:] = [t for t in tasks if t["row"] != row]
                row.destroy()
                y = 0
                for t in tasks:
                    t["target_y"] = y
                    y += ROW_H + ROW_PAD
                animate_reflow(tasks, duration_ms=220, step_ms=15)

            animate_slide_out(row, finish_remove)

    cb = tk.Checkbutton(row, variable=var, command=on_check, bg=CARD, activebackground=CARD)
    cb.pack(side=tk.LEFT)

    label = tk.Label(row, text=text, bg=CARD, fg=TEXT, font=("Segoe UI", 12))
    label.pack(side=tk.LEFT, padx=8)

    tasks.append({"row": row, "y": 0})
    layout_tasks()

    task_entry.delete(0, tk.END)


add_button = ttk.Button(input_frame, text="Add", command=add_task)
add_button.pack(side=tk.LEFT)
task_entry.bind("<Return>", lambda event: add_task())
root.mainloop()
