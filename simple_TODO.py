import tkinter as tk
from tkinter import ttk
import sqlite3
import hashlib

root = tk.Tk()
root.title("Simple To-Do List")
root.geometry("500x500")
root.resizable(False, False)

# Function to create the tasks and users tables if they don't exist
def create_tables():
    try:
        conn = sqlite3.connect('todo.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT, email TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, task TEXT, completed INTEGER DEFAULT 0)''')
        conn.commit()
        conn.close()

    except:
        pass

# Function to add a new user to the database
def register_user():
    username = username_entry.get()
    password = hashlib.sha256(password_entry.get().encode()).hexdigest()
    email = email_entry.get()
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute(f"INSERT INTO users (username, password, email) VALUES ('{username}', '{password}', '{email}')")
    conn.commit()
    conn.close()
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    show_login()

# Function to authenticate a user
def authenticate_user():
    username = username_login_entry.get()
    password = hashlib.sha256(password_login_entry.get().encode()).hexdigest()
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute(f"SELECT * FROM users WHERE username='{username}' AND password='{password}'")
    user = c.fetchone()
    conn.close()
    if user:
        current_user.set(user[0])
        show_tasks()
    else:
        login_error_label.config(text="Invalid username or password")

# Function to add a task to the database
def add_task():
    task = task_entry.get()
    user_id = current_user.get()
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute(f"INSERT INTO tasks (user_id, task) VALUES ({user_id}, '{task}')")
    conn.commit()
    conn.close()
    task_entry.delete(0, tk.END)
    view_tasks()

# Function to display the list of tasks
def view_tasks():
    user_id = current_user.get()
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute(f"SELECT * FROM tasks WHERE user_id={user_id}")
    tasks = c.fetchall()
    task_list.delete(*task_list.get_children())
    for task in tasks:
        if task[3] == 0:
            task_list.insert("", tk.END, text=task[2])
        else:
            task_list.insert("", tk.END, text=task[2], tags=('completed',))
    conn.close()

# Function to mark a task as completed
def complete_task():
    selected_task = task_list.item(task_list.selection())['text']
    user_id = current_user.get()
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute(f"UPDATE tasks SET completed=1 WHERE user_id={user_id} AND task='{selected_task}'")
    conn.commit()
    conn.close()
    view_tasks()

# Function to delete a task
def delete_task():
    selected_task = task_list.item(task_list.selection())['text']
    user_id = current_user.get()
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute(f"DELETE FROM tasks WHERE user_id={user_id} AND task='{selected_task}'")
    conn.commit()
    conn.close()
    view_tasks()

# Create the users and tasks tables if they don't exist
create_tables()

# Global variable to store the current user ID
current_user = tk.IntVar()

# Style for the treeview
style = ttk.Style()
style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 11)) # Modify the font of the body
style.configure("mystyle.Treeview.Heading", font=('Calibri', 13,'bold')) # Modify the font of the headings
style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})]) # Remove the borders
style.configure("mystyle.Treeview", background="#E1E1E1", foreground="black", fieldbackground="#E1E1E1")

# Create the sign-up form
def show_register():
    login_frame.pack_forget()
    register_frame.pack()

    global username_entry, password_entry, email_entry

    # Create the registration form widgets
    ttk.Label(register_frame, text="Username:").grid(row=0, column=0, padx=5, pady=5)
    username_entry = ttk.Entry(register_frame)
    username_entry.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(register_frame, text="Password:").grid(row=1, column=0, padx=5, pady=5)
    password_entry = ttk.Entry(register_frame, show="*")
    password_entry.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(register_frame, text="Email:").grid(row=2, column=0, padx=5, pady=5)
    email_entry = ttk.Entry(register_frame)
    email_entry.grid(row=2, column=1, padx=5, pady=5)

    ttk.Button(register_frame, text="Register", command=register_user).grid(row=3, column=1, padx=5, pady=5)

# Create the login form
def show_login():
    register_frame.pack_forget()
    login_frame.pack()

    global username_login_entry, password_login_entry, login_error_label

    # Create the login form widgets
    ttk.Label(login_frame, text="Username:").grid(row=0, column=0, padx=5, pady=5)
    username_login_entry = ttk.Entry(login_frame)
    username_login_entry.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(login_frame, text="Password:").grid(row=1, column=0, padx=5, pady=5)
    password_login_entry = ttk.Entry(login_frame, show="*")
    password_login_entry.grid(row=1, column=1, padx=5, pady=5)

    ttk.Button(login_frame, text="Login", command=authenticate_user).grid(row=2, column=1, padx=5, pady=5)

    ttk.Button(login_frame, text="Register", command=show_register).grid(row=2, column=0, padx=5, pady=5)

    login_error_label = ttk.Label(login_frame, text="", foreground="red")
    login_error_label.grid(row=3, column=1, padx=5, pady=5)

# Create the tasks form
def show_tasks():
    register_frame.pack_forget()
    login_frame.pack_forget()
    tasks_frame.pack()

    global task_entry, task_list

    # Create the tasks form widgets
    ttk.Label(tasks_frame, text="To-Do List", font=("Calibri", 16, "bold")).grid(row=0, column=0, padx=5, pady=5)

    task_entry = ttk.Entry(tasks_frame)
    task_entry.grid(row=1, column=0, padx=5, pady=5)

    ttk.Button(tasks_frame, text="Add Task", command=add_task).grid(row=1, column=1, padx=5, pady=5)

    task_list = ttk.Treeview(tasks_frame, columns=('task'), style="mystyle.Treeview")
    task_list.heading('#0', text='Task')
    task_list.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    task_list.tag_configure('completed', background='#7FFF7F')

    ttk.Button(tasks_frame, text="Complete Task", command=complete_task).grid(row=3, column=0, padx=5, pady=5)
    ttk.Button(tasks_frame, text="Delete Task", command=delete_task).grid(row=3, column=1, padx=5, pady=5)

    view_tasks()

# Create the frames
login_frame = ttk.Frame(root)
register_frame = ttk.Frame(root)
tasks_frame = ttk.Frame(root)

# Show the login form by default
show_login()

root.mainloop()