import json
import tkinter as tk
from tkinter import messagebox
from datetime import date
from pathlib import Path

DATA_FILE = Path("habit_data.json")

def load_data():
    if DATA_FILE.exists():
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"habits": [], "logs": []}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

class HabitTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Habit Tracker")
        self.root.geometry("800x550")
        self.root.configure(bg="#0f172a")

        self.data = load_data()

        self.habit_var = tk.StringVar()
        self.target_var = tk.StringVar(value="1")
        self.unit_var = tk.StringVar(value="times")
        self.log_count_var = tk.StringVar(value="1")
        self.log_date_var = tk.StringVar(value=str(date.today()))
        self.status_var = tk.StringVar(value="Add a habit to begin.")

        self.build_ui()
        self.refresh_all()

    def build_ui(self):
        title = tk.Label(self.root, text="Habit Tracker", font=("Arial", 22, "bold"),
                         bg="#0f172a", fg="white")
        title.pack(pady=10)

        main = tk.Frame(self.root, bg="#0f172a")
        main.pack(fill="both", expand=True, padx=15, pady=10)

        left = tk.Frame(main, bg="#111827", bd=0, highlightthickness=0)
        left.pack(side="left", fill="y", padx=(0, 10), ipadx=10, ipady=10)

        right = tk.Frame(main, bg="#111827", bd=0, highlightthickness=0)
        right.pack(side="right", fill="both", expand=True, ipadx=10, ipady=10)

        # Left panel: add habit
        tk.Label(left, text="Add Habit", font=("Arial", 16, "bold"),
                 bg="#111827", fg="white").pack(anchor="w", pady=(5, 10))

        tk.Label(left, text="Habit Name", bg="#111827", fg="white").pack(anchor="w")
        tk.Entry(left, textvariable=self.habit_var, width=28).pack(pady=5)

        tk.Label(left, text="Target Count", bg="#111827", fg="white").pack(anchor="w")
        tk.Entry(left, textvariable=self.target_var, width=28).pack(pady=5)

        tk.Label(left, text="Unit", bg="#111827", fg="white").pack(anchor="w")
        tk.Entry(left, textvariable=self.unit_var, width=28).pack(pady=5)

        tk.Button(left, text="Add Habit", bg="#38bdf8", fg="white",
                  command=self.add_habit).pack(fill="x", pady=(10, 5))

        tk.Button(left, text="Archive Selected Habit", bg="#ef4444", fg="white",
                  command=self.archive_habit).pack(fill="x", pady=5)

        tk.Label(left, text="Status", bg="#111827", fg="#94a3b8").pack(anchor="w", pady=(15, 0))
        tk.Label(left, textvariable=self.status_var, wraplength=220,
                 bg="#111827", fg="white", justify="left").pack(anchor="w", pady=5)

        # Right panel: habits list and log
        tk.Label(right, text="Habits", font=("Arial", 16, "bold"),
                 bg="#111827", fg="white").pack(anchor="w", pady=(5, 10))

        self.habit_listbox = tk.Listbox(right, height=10, bg="#1f2937", fg="white",
                                        selectbackground="#38bdf8", highlightthickness=0)
        self.habit_listbox.pack(fill="x", pady=(0, 10))

        tk.Label(right, text="Log Progress", font=("Arial", 14, "bold"),
                 bg="#111827", fg="white").pack(anchor="w", pady=(10, 5))

        log_frame = tk.Frame(right, bg="#111827")
        log_frame.pack(fill="x")

        tk.Label(log_frame, text="Habit", bg="#111827", fg="white").grid(row=0, column=0, sticky="w", pady=5)
        self.log_habit_var = tk.StringVar()
        self.log_habit_menu = tk.OptionMenu(log_frame, self.log_habit_var, "")
        self.log_habit_menu.grid(row=0, column=1, sticky="ew", padx=8, pady=5)

        tk.Label(log_frame, text="Date (YYYY-MM-DD)", bg="#111827", fg="white").grid(row=1, column=0, sticky="w", pady=5)
        tk.Entry(log_frame, textvariable=self.log_date_var).grid(row=1, column=1, sticky="ew", padx=8, pady=5)

        tk.Label(log_frame, text="Count", bg="#111827", fg="white").grid(row=2, column=0, sticky="w", pady=5)
        tk.Entry(log_frame, textvariable=self.log_count_var).grid(row=2, column=1, sticky="ew", padx=8, pady=5)

        log_frame.columnconfigure(1, weight=1)

        tk.Button(right, text="Save Log", bg="#22c55e", fg="white",
                  command=self.save_log).pack(fill="x", pady=(10, 5))

        tk.Button(right, text="Delete Selected Log", bg="#f59e0b", fg="white",
                  command=self.delete_log).pack(fill="x", pady=5)

        tk.Button(right, text="Refresh", bg="#64748b", fg="white",
                  command=self.refresh_all).pack(fill="x", pady=5)

        self.log_listbox = tk.Listbox(right, bg="#1f2937", fg="white",
                                      selectbackground="#38bdf8", highlightthickness=0)
        self.log_listbox.pack(fill="both", expand=True, pady=(10, 0))

    def add_habit(self):
        name = self.habit_var.get().strip()
        if not name:
            messagebox.showerror("Error", "Habit name cannot be empty.")
            return

        for habit in self.data["habits"]:
            if habit["name"].lower() == name.lower() and not habit.get("archived", False):
                messagebox.showerror("Error", "Habit already exists.")
                return

        try:
            target = int(self.target_var.get())
            if target <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Target count must be a positive integer.")
            return

        unit = self.unit_var.get().strip() or "times"

        self.data["habits"].append({
            "name": name,
            "target": target,
            "unit": unit,
            "archived": False
        })
        save_data(self.data)

        self.habit_var.set("")
        self.target_var.set("1")
        self.unit_var.set("times")
        self.status_var.set(f"Added habit: {name}")
        self.refresh_all()

    def archive_habit(self):
        selection = self.habit_listbox.curselection()
        if not selection:
            messagebox.showinfo("Info", "Select a habit to archive.")
            return

        index = selection[0]
        active_habits = [h for h in self.data["habits"] if not h.get("archived", False)]
        habit_name = active_habits[index]["name"]

        for habit in self.data["habits"]:
            if habit["name"] == habit_name:
                habit["archived"] = True
                break

        save_data(self.data)
        self.status_var.set(f"Archived habit: {habit_name}")
        self.refresh_all()

    def save_log(self):
        habit_name = self.log_habit_var.get().strip()
        if not habit_name:
            messagebox.showerror("Error", "Select a habit first.")
            return

        try:
            count = int(self.log_count_var.get())
            if count < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Count must be a non-negative integer.")
            return

        log_date = self.log_date_var.get().strip()
        if not log_date:
            messagebox.showerror("Error", "Date cannot be empty.")
            return

        for log in self.data["logs"]:
            if log["habit"] == habit_name and log["date"] == log_date:
                log["count"] = count
                break
        else:
            self.data["logs"].append({
                "habit": habit_name,
                "date": log_date,
                "count": count
            })

        save_data(self.data)
        self.status_var.set(f"Saved log for {habit_name} on {log_date}")
        self.refresh_all()

    def delete_log(self):
        selection = self.log_listbox.curselection()
        if not selection:
            messagebox.showinfo("Info", "Select a log to delete.")
            return

        index = selection[0]
        log_text = self.log_listbox.get(index)
        parts = log_text.split(" | ")
        if len(parts) < 3:
            return

        habit_name = parts[0].replace("Habit: ", "").strip()
        log_date = parts[1].replace("Date: ", "").strip()

        self.data["logs"] = [
            log for log in self.data["logs"]
            if not (log["habit"] == habit_name and log["date"] == log_date)
        ]
        save_data(self.data)
        self.status_var.set(f"Deleted log for {habit_name} on {log_date}")
        self.refresh_all()

    def refresh_all(self):
        self.refresh_habit_list()
        self.refresh_log_list()
        self.update_dropdown()

    def refresh_habit_list(self):
        self.habit_listbox.delete(0, tk.END)
        for habit in self.data["habits"]:
            if not habit.get("archived", False):
                self.habit_listbox.insert(
                    tk.END,
                    f"{habit['name']} - target {habit['target']} {habit['unit']}"
                )

    def refresh_log_list(self):
        self.log_listbox.delete(0, tk.END)
        for log in sorted(self.data["logs"], key=lambda x: x["date"], reverse=True):
            self.log_listbox.insert(
                tk.END,
                f"Habit: {log['habit']} | Date: {log['date']} | Count: {log['count']}"
            )

    def update_dropdown(self):
        active_habits = [h["name"] for h in self.data["habits"] if not h.get("archived", False)]

        menu = self.log_habit_menu["menu"]
        menu.delete(0, "end")

        if active_habits:
            for habit in active_habits:
                menu.add_command(label=habit, command=lambda value=habit: self.log_habit_var.set(value))
            if self.log_habit_var.get() not in active_habits:
                self.log_habit_var.set(active_habits[0])
        else:
            self.log_habit_var.set("")

if __name__ == "__main__":
    root = tk.Tk()
    app = HabitTrackerApp(root)
    root.mainloop()