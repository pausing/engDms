import sqlite3
import smtplib
import schedule
import time
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from tkinter import Tk, Label, Entry, Button, Listbox, END, Scrollbar, VERTICAL

# Database setup
def init_db():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            title TEXT,
            due_date TEXT,
            email TEXT
        )"""
    )
    conn.commit()
    conn.close()

# Add a new task
def add_task(title, due_date, email):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (title, due_date, email) VALUES (?, ?, ?)", (title, due_date, email))
    conn.commit()
    conn.close()
    refresh_tasks()

# Send email reminder
def send_email(to_address, subject, body):
    from_address = "your_email@gmail.com"
    password = "your_password"

    msg = MIMEMultipart()
    msg["From"] = from_address
    msg["To"] = to_address
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(from_address, password)
        server.send_message(msg)
        server.quit()
        print(f"Reminder sent to {to_address}")
    except Exception as e:
        print(f"Error sending email: {e}")

# Check for tasks due soon
def check_reminders():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("SELECT title, due_date, email FROM tasks")
    tasks = cursor.fetchall()
    conn.close()

    now = datetime.now()
    for task in tasks:
        task_title, due_date, email = task
        due = datetime.strptime(due_date, "%Y-%m-%d %H:%M")
        if due <= now:
            send_email(email, f"Reminder: {task_title}", f"The task '{task_title}' is due!")

# Schedule task reminders to run periodically
schedule.every(1).minutes.do(check_reminders)

# GUI Setup
def refresh_tasks():
    task_list.delete(0, END)
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("SELECT title, due_date FROM tasks")
    tasks = cursor.fetchall()
    conn.close()
    for task in tasks:
        task_list.insert(END, f"{task[0]} - {task[1]}")

def submit_task():
    title = title_entry.get()
    due_date = due_date_entry.get()
    email = email_entry.get()
    if title and due_date and email:
        add_task(title, due_date, email)

# Initialize the GUI
app = Tk()
app.title("To-Do List with Email Reminders")

Label(app, text="Task Title").grid(row=0, column=0)
title_entry = Entry(app)
title_entry.grid(row=0, column=1)

Label(app, text="Due Date (YYYY-MM-DD HH:MM)").grid(row=1, column=0)
due_date_entry = Entry(app)
due_date_entry.grid(row=1, column=1)

Label(app, text="Email").grid(row=2, column=0)
email_entry = Entry(app)
email_entry.grid(row=2, column=1)

Button(app, text="Add Task", command=submit_task).grid(row=3, column=0, columnspan=2)

task_list = Listbox(app, height=10, width=50)
task_list.grid(row=4, column=0, columnspan=2)

scrollbar = Scrollbar(app, orient=VERTICAL)
scrollbar.grid(row=4, column=2, sticky="ns")
task_list.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=task_list.yview)

# Initialize database and refresh tasks
init_db()
refresh_tasks()

# Run the reminder checks in a background thread
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

import threading
threading.Thread(target=run_scheduler, daemon=True).start()

# Run the GUI
app.mainloop()
