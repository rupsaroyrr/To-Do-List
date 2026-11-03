import json
import os
import tkinter as tk
from tkinter import messagebox
from datetime import datetime


TASK_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tasks.txt")

COLORS = {
    "background": "#F5F7FA",
    "surface": "#FFFFFF",
    "surface_alt": "#F8FAFD",
    "text": "#1E293B",
    "muted": "#64748B",
    "primary": "#2563EB",
    "primary_dark": "#1D4ED8",
    "border": "#E2E8F0",
    "danger": "#DC2626",
    "success": "#15803D",
    "warning": "#B45309",
}

PRIORITY_COLORS = {
    "High": "#DC2626",
    "Medium": "#D97706",
    "Low": "#2563EB",
}


def show_status(message, message_type="success"):
    colors = {
        "success": COLORS["success"],
        "warning": COLORS["warning"],
        "error": COLORS["danger"],
    }
    status_label.config(text=message, fg=colors.get(message_type, COLORS["success"]))


def save_tasks():
    try:
        with open(TASK_FILE, "w", encoding="utf-8") as file:
            json.dump(tasks, file, ensure_ascii=False, indent=2)
        return True
    except OSError as error:
        messagebox.showerror("Save Error", "Tasks could not be saved.\n\n" + str(error))
        show_status("Could not save tasks.", "error")
        return False


def load_tasks():
    if not os.path.exists(TASK_FILE):
        return

    try:
        with open(TASK_FILE, "r", encoding="utf-8") as file:
            content = file.read().strip()

        if not content:
            return

        try:
            loaded = json.loads(content)
            if isinstance(loaded, list):
                for item in loaded:
                    if isinstance(item, dict) and item.get("name", "").strip():
                        tasks.append({
                            "name": item["name"].strip(),
                            "priority": item.get("priority", "Medium")
                            if item.get("priority") in ("High", "Medium", "Low")
                            else "Medium",
                            "due": normalize_due_date(item.get("due", "")),
                            "completed": bool(item.get("completed", False)),
                        })
                return
        except json.JSONDecodeError:
            pass

        for line in content.splitlines():
            name = line.strip()
            if name:
                tasks.append({
                    "name": name,
                    "priority": "Medium",
                    "due": "",
                    "completed": False,
                })
    except (OSError, UnicodeError) as error:
        messagebox.showerror("Load Error", "Tasks could not be loaded.\n\n" + str(error))
        show_status("Could not load saved tasks.", "error")


def normalize_due_date(value):
    value = str(value or "").strip()
    if not value:
        return ""
    try:
        parsed = datetime.strptime(value, "%d.%m.%Y")
    except ValueError:
        try:
            parsed = datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            return ""
    return parsed.strftime("%d.%m.%Y")


def due_status(task):
    if not task["due"]:
        return ""
    try:
        due_date = datetime.strptime(task["due"], "%d.%m.%Y").date()
    except ValueError:
        return ""

    if task["completed"]:
        return "Completed"
    if due_date < datetime.now().date():
        return "Overdue"
    if due_date == datetime.now().date():
        return "Due today"
    return "Due " + due_date.strftime("%d.%m.%Y")


def rounded_rectangle(canvas, x1, y1, x2, y2, radius=14, **kwargs):
    points = [
        x1 + radius, y1, x2 - radius, y1, x2, y1,
        x2, y1 + radius, x2, y2 - radius, x2, y2,
        x2 - radius, y2, x1 + radius, y2, x1, y2,
        x1, y2 - radius, x1, y1 + radius, x1, y1,
    ]
    return canvas.create_polygon(points, smooth=True, splinesteps=36, **kwargs)


def add_task(event=None):
    name = task_entry.get().strip()
    if not name:
        messagebox.showwarning("Input Warning", "Please enter a task.")
        show_status("Task cannot be empty.", "warning")
        task_entry.focus()
        return

    due = normalize_due_date(due_entry.get())
    if due_entry.get().strip() and not due:
        messagebox.showwarning("Invalid Due Date", "Use DD.MM.YYYY, for example 31.12.2026.")
        show_status("Due date format is DD.MM.YYYY.", "warning")
        due_entry.focus()
        return

    tasks.insert(0, {
        "name": name,
        "priority": priority_var.get(),
        "due": due,
        "completed": False,
    })
    task_entry.delete(0, tk.END)
    due_entry.delete(0, tk.END)
    priority_var.set("Medium")

    if save_tasks():
        current_filter.set("All")
        search_var.set("")
        refresh_tasks()
        show_status("Task added successfully.")
        task_entry.focus()


def toggle_task(index):
    tasks[index]["completed"] = not tasks[index]["completed"]
    if save_tasks():
        refresh_tasks()
        show_status("Task status updated.")


def delete_task(index):
    name = tasks[index]["name"]
    if messagebox.askyesno("Delete Task", "Delete " + repr(name) + "?"):
        del tasks[index]
        if save_tasks():
            refresh_tasks()
            show_status("Task deleted successfully.")


def clear_tasks():
    if not tasks:
        messagebox.showinfo("Clear Tasks", "The task list is already empty.")
        return
    if messagebox.askyesno("Confirm Clear", "Delete all tasks?"):
        tasks.clear()
        if save_tasks():
            refresh_tasks()
            show_status("All tasks cleared successfully.")


def clear_completed():
    completed_count = sum(1 for task in tasks if task["completed"])
    if not completed_count:
        show_status("No completed tasks to clear.", "warning")
        return
    if messagebox.askyesno("Clear Completed", "Delete completed tasks?"):
        tasks[:] = [task for task in tasks if not task["completed"]]
        if save_tasks():
            refresh_tasks()
            show_status("Completed tasks cleared successfully.")


def refresh_tasks(*args):
    for widget in cards_frame.winfo_children():
        widget.destroy()

    query = search_var.get().strip().lower()
    selected_filter = current_filter.get()
    visible_indexes = []

    for index, task in enumerate(tasks):
        if query and query not in task["name"].lower():
            continue
        if selected_filter == "Pending" and task["completed"]:
            continue
        if selected_filter == "Completed" and not task["completed"]:
            continue
        visible_indexes.append(index)

    if not visible_indexes:
        empty_label = tk.Label(
            cards_frame,
            text="No tasks match this view.",
            font=("Segoe UI", 11),
            bg=COLORS["background"],
            fg=COLORS["muted"],
        )
        empty_label.pack(pady=40)
    else:
        for index in visible_indexes:
            create_task_card(index)

    remaining = sum(not task["completed"] for task in tasks)
    summary_label.config(
        text=f"{remaining} pending  /  {len(tasks)} total"
    )
    cards_canvas.configure(scrollregion=cards_canvas.bbox("all"))


def create_task_card(index):
    task = tasks[index]
    is_overdue = due_status(task) == "Overdue"
    fill = "#FFF7ED" if is_overdue else COLORS["surface"]
    card = tk.Frame(
        cards_frame,
        bg=fill,
        highlightbackground=COLORS["border"],
        highlightthickness=1,
    )
    card.pack(fill="x", pady=(0, 8), padx=2, ipady=4)

    complete_var = tk.BooleanVar(value=task["completed"])
    checkbox = tk.Checkbutton(
        card,
        variable=complete_var,
        command=lambda i=index: toggle_task(i),
        bg=fill,
        activebackground=fill,
        highlightthickness=0,
        bd=0,
        cursor="hand2",
    )
    checkbox.grid(row=0, column=0, rowspan=2, padx=(12, 8))

    name_color = COLORS["muted"] if task["completed"] else COLORS["text"]
    name_font = ("Segoe UI", 11, "overstrike" if task["completed"] else "normal")
    tk.Label(
        card,
        text=task["name"],
        font=name_font,
        fg=name_color,
        bg=fill,
        anchor="w",
    ).grid(row=0, column=1, sticky="w", pady=(10, 1))

    status = due_status(task)
    detail_parts = []
    if status:
        detail_parts.append(status)
    if task["due"] and status == "Completed":
        detail_parts.append("Due " + datetime.strptime(task["due"], "%d.%m.%Y").strftime("%d.%m.%Y"))
    detail = "  •  ".join(detail_parts) if detail_parts else "No due date"
    detail_color = COLORS["danger"] if is_overdue else COLORS["muted"]

    tk.Label(
        card,
        text=detail,
        font=("Segoe UI", 9),
        fg=detail_color,
        bg=fill,
        anchor="w",
    ).grid(row=1, column=1, sticky="w", pady=(0, 10))

    priority = task["priority"]
    tk.Label(
        card,
        text=priority.upper(),
        font=("Segoe UI", 8, "bold"),
        fg="white",
        bg=PRIORITY_COLORS[priority],
        padx=8,
        pady=4,
    ).grid(row=0, column=2, rowspan=2, padx=(14, 10))

    tk.Button(
        card,
        text="Delete",
        command=lambda i=index: delete_task(i),
        font=("Segoe UI", 8, "bold"),
        bg=fill,
        fg=COLORS["danger"],
        activebackground="#FEE2E2",
        activeforeground=COLORS["danger"],
        relief="flat",
        cursor="hand2",
        bd=0,
        padx=5,
    ).grid(row=0, column=3, rowspan=2, padx=(0, 12))
    card.columnconfigure(1, weight=1)


def center_window(window, width, height):
    window.update_idletasks()
    x_position = (window.winfo_screenwidth() - width) // 2
    y_position = (window.winfo_screenheight() - height) // 2
    window.geometry(f"{width}x{height}+{x_position}+{y_position}")


tasks = []
load_tasks()

root = tk.Tk()
root.title("My To-Do List")
root.configure(bg=COLORS["background"])
root.resizable(True, True)
root.minsize(760, 640)
center_window(root, 860, 720)

header = tk.Frame(root, bg=COLORS["background"])
header.pack(fill="x", padx=36, pady=(24, 14))

title_block = tk.Frame(header, bg=COLORS["background"])
title_block.pack(side="left")
tk.Label(
    title_block,
    text="My To-Do List",
    font=("Segoe UI", 24, "bold"),
    bg=COLORS["background"],
    fg=COLORS["text"],
).pack(anchor="w")
tk.Label(
    title_block,
    text="Plan today. Finish with focus.",
    font=("Segoe UI", 10),
    bg=COLORS["background"],
    fg=COLORS["muted"],
).pack(anchor="w", pady=(2, 0))

summary_label = tk.Label(
    header,
    font=("Segoe UI", 10),
    bg=COLORS["background"],
    fg=COLORS["muted"],
)
summary_label.pack(side="right", pady=(10, 0))

composer = tk.Frame(root, bg=COLORS["surface"], highlightbackground=COLORS["border"], highlightthickness=1)
composer.pack(fill="x", padx=36, pady=(0, 14))

task_entry = tk.Entry(composer, font=("Segoe UI", 11), relief="flat", bd=0)
task_entry.grid(row=0, column=0, sticky="ew", padx=(16, 8), pady=14, ipady=9)

tk.Label(composer, text="Priority", bg=COLORS["surface"], fg=COLORS["muted"], font=("Segoe UI", 9)).grid(
    row=0, column=1, padx=(4, 2), pady=14
)
priority_var = tk.StringVar(value="Medium")
priority_menu = tk.OptionMenu(composer, priority_var, "High", "Medium", "Low")
priority_menu.configure(
    font=("Segoe UI", 10),
    bg=COLORS["surface"],
    fg=COLORS["text"],
    relief="solid",
    bd=1,
    highlightthickness=0,
    cursor="hand2",
)
priority_menu.grid(row=0, column=2, padx=(0, 10), pady=14, ipady=5)

tk.Label(composer, text="Due", bg=COLORS["surface"], fg=COLORS["muted"], font=("Segoe UI", 9)).grid(
    row=0, column=3, padx=(2, 2), pady=14
)
due_entry = tk.Entry(composer, width=12, font=("Segoe UI", 10), relief="solid", bd=1)
due_entry.grid(row=0, column=4, padx=(0, 10), pady=14, ipady=7)

add_button = tk.Button(
    composer,
    text="+  Add Task",
    command=add_task,
    font=("Segoe UI", 10, "bold"),
    bg=COLORS["primary"],
    fg="white",
    activebackground=COLORS["primary_dark"],
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    padx=16,
)
add_button.grid(row=0, column=5, padx=(0, 14), pady=14, ipady=7)
composer.columnconfigure(0, weight=1)
task_entry.bind("<Return>", add_task)

toolbar = tk.Frame(root, bg=COLORS["background"])
toolbar.pack(fill="x", padx=36, pady=(0, 10))

search_var = tk.StringVar()
search_entry = tk.Entry(
    toolbar,
    textvariable=search_var,
    font=("Segoe UI", 10),
    relief="solid",
    bd=1,
)
search_entry.pack(side="left", fill="x", expand=True, ipady=7, padx=(0, 12))
search_var.trace_add("write", refresh_tasks)

current_filter = tk.StringVar(value="All")
for filter_name in ("All", "Pending", "Completed"):
    button = tk.Radiobutton(
        toolbar,
        text=filter_name,
        variable=current_filter,
        value=filter_name,
        command=refresh_tasks,
        indicatoron=False,
        font=("Segoe UI", 9, "bold"),
        bg=COLORS["surface"],
        fg=COLORS["text"],
        selectcolor="#DBEAFE",
        activebackground="#DBEAFE",
        relief="solid",
        bd=1,
        cursor="hand2",
        padx=10,
        pady=7,
    )
    button.pack(side="left", padx=(0, 5))

list_container = tk.Frame(root, bg=COLORS["background"])
list_container.pack(fill="both", expand=True, padx=36, pady=(0, 8))

cards_canvas = tk.Canvas(list_container, bg=COLORS["background"], highlightthickness=0)
cards_scrollbar = tk.Scrollbar(list_container, orient="vertical", command=cards_canvas.yview)
cards_canvas.configure(yscrollcommand=cards_scrollbar.set)
cards_scrollbar.pack(side="right", fill="y")
cards_canvas.pack(side="left", fill="both", expand=True)

cards_frame = tk.Frame(cards_canvas, bg=COLORS["background"])
cards_window = cards_canvas.create_window((0, 0), window=cards_frame, anchor="nw")
cards_frame.bind("<Configure>", lambda event: cards_canvas.configure(scrollregion=cards_canvas.bbox("all")))
cards_canvas.bind("<Configure>", lambda event: cards_canvas.itemconfigure(cards_window, width=event.width))
cards_canvas.bind_all("<MouseWheel>", lambda event: cards_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units"))

footer = tk.Frame(root, bg=COLORS["background"])
footer.pack(fill="x", padx=36, pady=(0, 14))

status_label = tk.Label(
    footer,
    text="Ready",
    font=("Segoe UI", 9),
    bg=COLORS["background"],
    fg=COLORS["success"],
)
status_label.pack(side="left")

tk.Button(
    footer,
    text="Clear Completed",
    command=clear_completed,
    font=("Segoe UI", 9, "bold"),
    bg=COLORS["background"],
    fg=COLORS["warning"],
    activebackground="#FEF3C7",
    relief="flat",
    cursor="hand2",
    padx=8,
).pack(side="right", padx=(5, 0))

tk.Button(
    footer,
    text="Clear All",
    command=clear_tasks,
    font=("Segoe UI", 9, "bold"),
    bg=COLORS["background"],
    fg=COLORS["danger"],
    activebackground="#FEE2E2",
    relief="flat",
    cursor="hand2",
    padx=8,
).pack(side="right")

refresh_tasks()
task_entry.focus()
root.mainloop()
