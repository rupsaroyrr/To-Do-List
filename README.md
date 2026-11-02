# To-Do List Application

A simple desktop To-Do List mini-project developed using Python and Tkinter for MCA 1st-year students.

## Features

- Add a task using the input field or the Enter key
- View all tasks in a scrollable list
- Delete a selected task
- Clear all tasks after confirmation
- Automatically save tasks to `tasks.txt`
- Automatically load saved tasks at startup
- Display warning, success, and error messages

## Requirements

- Python 3
- Tkinter

Tkinter is included with standard Python installations. When installing Python on Windows, select the option to install Tcl/Tk and IDLE if it is not already available.

## Run in VS Code

1. Install Python from https://www.python.org/downloads/.
2. Open the project folder in VS Code.
3. Open `todo_list.py`.
4. Select Python as the interpreter if prompted.
5. Run the file using the Run button, or enter this command in the terminal:

   ```powershell
   python todo_list.py
   ```

## Run in IDLE

1. Open `todo_list.py` in Python IDLE.
2. Select **Run > Run Module**.
3. Press `F5` if required.

## Application Usage

1. Type a task in the input field.
2. Press Enter or click **Add Task**.
3. Select a task from the list.
4. Click **Delete Selected Task** to remove it.
5. Click **Clear All Tasks** to remove every task after confirmation.

Task changes are saved automatically.

## How the Features Work

- **Adding a task:** The `add_task()` function reads and trims the text entered in the Entry widget. Empty input produces a warning.
- **Displaying tasks:** The Listbox stores and displays tasks, while the Scrollbar allows long lists to be viewed easily.
- **Deleting a task:** The `delete_task()` function checks whether an item is selected and then removes it.
- **Clearing tasks:** The `clear_tasks()` function asks the user for confirmation before deleting every item.
- **Saving tasks:** The `save_tasks()` function writes each Listbox item to `tasks.txt`.
- **Loading tasks:** The `load_tasks()` function reads saved lines and adds them to the Listbox when the application starts.
- **File handling:** The program catches file and encoding errors and displays an error dialog instead of crashing unexpectedly.

## Python Concepts Used

- Variables and strings
- Functions
- Lists and tuples
- `for` loops
- File handling
- `try` and `except` blocks
- Event handling
- Function parameters
- Dictionary data for status colors

## Tkinter Concepts Used

- `Tk` for the main window
- `Label` for headings and status messages
- `Entry` for task input
- `Button` for application actions
- `Frame` for layout grouping
- `Listbox` for displaying tasks
- `Scrollbar` for list navigation
- `messagebox` for warnings, errors, and confirmations
- `bind()` for Enter-key support

## Project Abstract

This project is a desktop-based To-Do List Application developed using Python and Tkinter. It provides basic task-management operations such as adding, viewing, deleting, and clearing tasks. Tasks are automatically stored in a text file and loaded when the application starts. The graphical interface uses standard Tkinter widgets and is designed to be simple, readable, and beginner-friendly.

## Objectives

- Understand Python GUI programming.
- Use Tkinter widgets to create a desktop application.
- Implement basic text-file storage.
- Apply input validation and confirmation dialogs.
- Create a user-friendly task-management application.

