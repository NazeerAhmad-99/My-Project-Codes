import tkinter as tk
from tkinter import ttk


def formula(weight, height, age):
    bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
    return bmr


def calculate_tdee(bmr, activity_level):
    if activity_level == "sedentary":
        return bmr * 1.2
    elif activity_level == "light":
        return bmr * 1.375
    elif activity_level == "moderate":
        return bmr * 1.55
    elif activity_level == "active":
        return bmr * 1.725
    elif activity_level == "very active":
        return bmr * 1.9
    else:
        return None


def gui():
    root = tk.Tk()
    root.geometry("600x520")
    root.title("BMR and TDEE Calculator by your Twin")
    root.configure(bg="#0f1115")
    
    bg = "#0f1115"
    card = "#151922"
    text = "#e6e9ef"
    muted = "#9aa4b2"
    accent = "#4cc9f0"
    entry_bg = "#1c2230"
    
    style = ttk.Style()
    style.theme_use("clam")
    
    style.configure("TLabel", background=card, foreground=text, font=("Segoe UI", 11))
    style.configure("Header.TLabel", background=card, foreground=text, font=("Segoe UI Semibold", 18))
    style.configure("Muted.TLabel", background=card, foreground=muted, font=("Segoe UI", 9))
    
    style.configure("TEntry", fieldbackground=entry_bg, foreground=text)
    style.configure("TCombobox", fieldbackground=entry_bg, foreground=text)
    
    style.configure(
        "Custom.TCombobox",
        fieldbackground=entry_bg,
        foreground=text,
        background=entry_bg,
        arrowsize=14
    )
    style.map(
        "Custom.TCombobox",
        fieldbackground=[("readonly", entry_bg), ("active", "#232a3a")],
        foreground=[("readonly", text)]
    )

    style.configure("Accent.TButton", background=accent, foreground="#0f1115", font=("Segoe UI Semibold", 10))
    style.map("Accent.TButton", background=[("active", "#5ddcff")])

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    
    container = tk.Frame(root, bg=card)
    container.grid(row=0, column=0, padx=24, pady=24)
    
    container.columnconfigure(0, weight=1)
    container.columnconfigure(1, weight=1)
    
    ttk.Label(container, text="BMR + TDEE", style ="Header.TLabel").grid(row=0, column=0, columnspan=2, padx=16, pady=(20, 2),sticky="w")
    ttk.Label(container, text="Daily energy estimate", style = "Muted.TLabel").grid(row=1, column=0, columnspan=2, padx=16, pady=(0, 16),sticky="w")
    
    ttk.Label(container, text="Weight (kg)").grid(row=2, column=0, padx=16, pady=(20, 8), sticky="w")
    weight_entry = ttk.Entry(container)
    weight_entry.grid(row=2, column=1, padx=16, pady=(20, 8), sticky="ew")
    
    ttk.Label(container, text="Height (cm)").grid(row=3, column=0, padx=16, pady=8, sticky="w")
    height_entry = ttk.Entry(container)
    height_entry.grid(row=3, column=1, padx=16, pady=8, sticky="ew")
    
    ttk.Label(container, text="Age (years)").grid(row=4, column=0, padx=16, pady=8, sticky="w")
    age_entry = ttk.Entry(container)
    age_entry.grid(row=4, column=1, padx=16, pady=8, sticky="ew")
    
    ttk.Label(container, text="Activity level").grid(row=5, column=0, padx=16, pady=8, sticky="w")
    activity_var = tk.StringVar(value ="sedentary")
    activity_combo = ttk.Combobox(
        container,
        textvariable=activity_var,
        values=["sedentary", "light", "moderate", "active", "very active"],
        state="readonly",
        style="Custom.TCombobox"
    )
    activity_combo.grid(row=5, column=1, padx=16, ipady=3, sticky="ew")
    def on_calculate():
        try:
            weight = float(weight_entry.get())
            height = float(height_entry.get())
            age = float(age_entry.get())
        except ValueError:
            result_label.config(text="Please enter a valid number for weight, height and age to continue twin.")
            return
        
        bmr= formula(weight, height, age)
        tdee = calculate_tdee(bmr, activity_var.get())
        
        if tdee is None:
            result_label.config(text="Invalid activity level entered.")
        else:
            result_label.config(text=f"Your BMR is: {bmr:.2f}\nYour TDEE is: {tdee:.2f}")
    calc_button = ttk.Button(container, text="Calculate Your BMR and TDEE", command=on_calculate, style="Accent.TButton")
    calc_button.grid(row=6, column=0, columnspan=2, padx=16, pady=(16, 8), sticky="ew")

    result_label = ttk.Label(container, text="Result will appear here")
    result_label.grid(row=7, column=0, columnspan=2, padx=16, pady=(8, 20))

    root.mainloop()


if __name__ == "__main__":
    
    gui()
