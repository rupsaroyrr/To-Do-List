import os
import tkinter as tk
from tkinter import messagebox


# Save the task file in the same folder as this Python program.
TASK_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tasks.txt")


def show_status(message, message_type="success"):
    """Display a short message and use a matching color."""
    colors = {
        "success": "#217A3B",
        "warning": "#A66B00",
        "error": "#B3261E",
    }
    status_label.config(text=message, fg=colors.get(message_type, "#217A3B"))


def save_tasks():
    """Save all tasks from the Listbox to a text file."""
    tasks = task_listbox.get(0, tk.END)

    try:
        with open(TASK_FILE, "w", encoding="utf-8") as file:
            for task in tasks:
                file.write(task + "\n")
        return True
    except OSError as error:
        messagebox.showerror(
            "Save Error",
            "Tasks could not be saved.\n\n" + str(error),
        )
        show_status("Could not save tasks.", "error")
        return False


def load_tasks():
    """Load tasks from the text file when the application starts."""
    if not os.path.exists(TASK_FILE):
        return

    try:
        with open(TASK_FILE, "r", encoding="utf-8") as file:
            for line in file:
                task = line.strip()
                if task:
                    task_listbox.insert(tk.END, task)
        show_status("Saved tasks loaded successfully.")
    except (OSError, UnicodeError) as error:
        messagebox.showerror(
            "Load Error",
            "Tasks could not be loaded.\n\n" + str(error),
        )
        show_status("Could not load saved tasks.", "error")


def add_task(event=None):
    """Add the task entered by the user."""
    task = task_entry.get().strip()

    if task == "":
        messagebox.showwarning("Input Warning", "Please enter a task.")
        show_status("Task cannot be empty.", "warning")
        task_entry.focus()
        return

    task_listbox.insert(tk.END, task)
    task_entry.delete(0, tk.END)

    if save_tasks():
        show_status("Task added successfully.")
    task_entry.focus()


def delete_task():
    """Delete the task selected in the Listbox."""
    selected_index = task_listbox.curselection()

    if not selected_index:
        messagebox.showwarning(
            "Selection Warning",
            "Please select a task to delete.",
        )
        show_status("No task selected.", "warning")
        return

    index = selected_index[0]
    task_listbox.delete(index)

    if save_tasks():
        show_status("Task deleted successfully.")


def clear_tasks():
    """Ask for confirmation and then delete all tasks."""
    if task_listbox.size() == 0:
        messagebox.showinfo("Clear Tasks", "The task list is already empty.")
        show_status("There are no tasks to clear.", "warning")
        return

    confirmed = messagebox.askyesno(
        "Confirm Clear",
        "Are you sure you want to delete all tasks?",
    )

    if confirmed:
        task_listbox.delete(0, tk.END)
        if save_tasks():
            show_status("All tasks cleared successfully.")


def center_window(window, width, height):
    """Place the application window at the center of the screen."""
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x_position = (screen_width - width) // 2
    y_position = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x_position}+{y_position}")


# Create the main application window.
root = tk.Tk()
root.title("My To-Do List - Mini Project")
root.configure(bg="#EAF0F6")
root.resizable(False, False)

center_window(root, 620, 510)

# Heading.
title_label = tk.Label(
    root,
    text="My To-Do List",
    font=("Segoe UI", 24, "bold"),
    bg="#EAF0F6",
    fg="#234A73",
)
title_label.pack(pady=(20, 15))

# Input area.
input_frame = tk.Frame(root, bg="#EAF0F6")
input_frame.pack(fill="x", padx=35, pady=(0, 12))

task_entry = tk.Entry(
    input_frame,
    font=("Segoe UI", 12),
    relief="solid",
    bd=1,
)
task_entry.pack(side="left", fill="x", expand=True, ipady=7)
task_entry.bind("<Return>", add_task)

add_button = tk.Button(
    input_frame,
    text="Add Task",
    command=add_task,
    font=("Segoe UI", 11, "bold"),
    bg="#2878C7",
    fg="white",
    activebackground="#1F639F",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    padx=12,
)
add_button.pack(side="left", padx=(10, 0), ipady=4)

# Task list area.
list_frame = tk.Frame(root, bg="white", relief="solid", bd=1)
list_frame.pack(fill="both", expand=True, padx=35, pady=(0, 12))

scrollbar = tk.Scrollbar(list_frame)
scrollbar.pack(side="right", fill="y")

task_listbox = tk.Listbox(
    list_frame,
    font=("Segoe UI", 12),
    bg="white",
    fg="#333333",
    selectbackground="#2878C7",
    selectforeground="white",
    activestyle="none",
    yscrollcommand=scrollbar.set,
)
task_listbox.pack(fill="both", expand=True, padx=5, pady=5)
scrollbar.config(command=task_listbox.yview)

# Action buttons.
button_frame = tk.Frame(root, bg="#EAF0F6")
button_frame.pack(pady=(0, 8))

delete_button = tk.Button(
    button_frame,
    text="Delete Selected Task",
    command=delete_task,
    font=("Segoe UI", 11, "bold"),
    bg="#E0A21B",
    fg="#FFFFFF",
    activebackground="#B9820B",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    padx=15,
)
delete_button.pack(side="left", padx=5, ipady=5)

clear_button = tk.Button(
    button_frame,
    text="Clear All Tasks",
    command=clear_tasks,
    font=("Segoe UI", 11, "bold"),
    bg="#D84A4A",
    fg="white",
    activebackground="#B93434",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    padx=15,
)
clear_button.pack(side="left", padx=5, ipady=5)

# Status message area.
status_label = tk.Label(
    root,
    text="Ready",
    font=("Segoe UI", 10),
    bg="#EAF0F6",
    fg="#217A3B",
)
status_label.pack(pady=(0, 12))

load_tasks()
task_entry.focus()

root.mainloop()
