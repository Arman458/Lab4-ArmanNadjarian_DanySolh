import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import filedialog
import sqlite3
import shutil
import os


def create_tables():
    with sqlite3.connect('school_management.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id TEXT PRIMARY KEY,
                name TEXT,
                age INTEGER,
                email TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS instructors (
                id TEXT PRIMARY KEY,
                name TEXT,
                age INTEGER,
                email TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS courses (
                id TEXT PRIMARY KEY,
                name TEXT,
                instructor_id TEXT,
                FOREIGN KEY(instructor_id) REFERENCES instructors(id)
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS registrations (
                student_id TEXT,
                course_id TEXT,
                FOREIGN KEY(student_id) REFERENCES students(id),
                FOREIGN KEY(course_id) REFERENCES courses(id)
            )
        ''')
        conn.commit()

create_tables()


def add_student(student_id, name, age, email):
    with sqlite3.connect('school_management.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO students (id, name, age, email) VALUES (?, ?, ?, ?)
        ''', (student_id, name, age, email))
        conn.commit()

def add_instructor(instructor_id, name, age, email):
    with sqlite3.connect('school_management.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO instructors (id, name, age, email) VALUES (?, ?, ?, ?)
        ''', (instructor_id, name, age, email))
        conn.commit()

def add_course(course_id, name, instructor_id):
    with sqlite3.connect('school_management.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO courses (id, name, instructor_id) VALUES (?, ?, ?)
        ''', (course_id, name, instructor_id))
        conn.commit()

def register_student_for_course(student_id, course_id):
    with sqlite3.connect('school_management.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO registrations (student_id, course_id) VALUES (?, ?)
        ''', (student_id, course_id))
        conn.commit()


def get_all_students():
    with sqlite3.connect('school_management.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM students')
        return cursor.fetchall()

def get_all_instructors():
    with sqlite3.connect('school_management.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM instructors')
        return cursor.fetchall()

def get_all_courses():
    with sqlite3.connect('school_management.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM courses')
        return cursor.fetchall()

def get_student_courses(student_id):
    with sqlite3.connect('school_management.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT courses.name FROM courses
            JOIN registrations ON courses.id = registrations.course_id
            WHERE registrations.student_id = ?
        ''', (student_id,))
        return cursor.fetchall()


def delete_student(student_id):
    with sqlite3.connect('school_management.db') as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM students WHERE id = ?', (student_id,))
        conn.commit()

def delete_instructor(instructor_id):
    with sqlite3.connect('school_management.db') as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM instructors WHERE id = ?', (instructor_id,))
        conn.commit()

def delete_course(course_id):
    with sqlite3.connect('school_management.db') as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM courses WHERE id = ?', (course_id,))
        conn.commit()


def update_student(student_id, name, age, email):
    with sqlite3.connect('school_management.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE students SET name = ?, age = ?, email = ? WHERE id = ?
        ''', (name, age, email, student_id))
        conn.commit()

def update_instructor(instructor_id, name, age, email):
    with sqlite3.connect('school_management.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE instructors SET name = ?, age = ?, email = ? WHERE id = ?
        ''', (name, age, email, instructor_id))
        conn.commit()

def update_course(course_id, name, instructor_id):
    with sqlite3.connect('school_management.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE courses SET name = ?, instructor_id = ? WHERE id = ?
        ''', (name, instructor_id, course_id))
        conn.commit()


def backup_database():
    backup_file = filedialog.asksaveasfilename(
        defaultextension=".db",
        filetypes=[("Database Files", "*.db"), ("All Files", "*.*")]
    )
    if backup_file:
        shutil.copy('school_management.db', backup_file)
        messagebox.showinfo("Backup", f"Database backup completed successfully!\nSaved to {backup_file}")


def update_comboboxes():
    student_combobox['values'] = [s[1] for s in get_all_students()]
    instructor_combobox['values'] = [i[1] for i in get_all_instructors()]
    course_combobox['values'] = [c[1] for c in get_all_courses()]

def add_student_record():
    student_id = student_id_entry.get()
    name = student_name_entry.get()
    age = student_age_entry.get()
    email = student_email_entry.get()
    add_student(student_id, name, int(age), email)
    update_comboboxes()
    messagebox.showinfo("Success", "Student added successfully!")

def add_instructor_record():
    instructor_id = instructor_id_entry.get()
    name = instructor_name_entry.get()
    age = instructor_age_entry.get()
    email = instructor_email_entry.get()
    add_instructor(instructor_id, name, int(age), email)
    update_comboboxes()
    messagebox.showinfo("Success", "Instructor added successfully!")

def add_course_record():
    course_id = course_id_entry.get()
    name = course_name_entry.get()
    instructor_id = instructor_combobox.get()
    add_course(course_id, name, instructor_id)
    update_comboboxes()
    messagebox.showinfo("Success", "Course added successfully!")

def register_student():
    student_id = student_combobox.get()
    course_id = course_combobox.get()
    register_student_for_course(student_id, course_id)
    messagebox.showinfo("Success", "Student registered for course successfully!")

def delete_record():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select a record to delete.")
        return

    values = tree.item(selected_item, 'values')
    
    if values[4] == "Student":
        delete_student(values[1])
    elif values[4] == "Instructor":
        delete_instructor(values[1])
    elif values[4] == "Course":
        delete_course(values[1])

    tree.delete(selected_item)
    messagebox.showinfo("Success", "Record deleted successfully.")

def edit_record():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select a record to edit.")
        return

    values = tree.item(selected_item, 'values')
    
    if values[4] == "Student":
        student_name_entry.delete(0, tk.END)
        student_name_entry.insert(0, values[0])
        student_id_entry.delete(0, tk.END)
        student_id_entry.insert(0, values[1])
        student_age_entry.delete(0, tk.END)
        student_age_entry.insert(0, values[2])
        student_email_entry.delete(0, tk.END)
        student_email_entry.insert(0, values[3])
        delete_student(values[1])
    elif values[4] == "Instructor":
        instructor_name_entry.delete(0, tk.END)
        instructor_name_entry.insert(0, values[0])
        instructor_id_entry.delete(0, tk.END)
        instructor_id_entry.insert(0, values[1])
        instructor_age_entry.delete(0, tk.END)
        instructor_age_entry.insert(0, values[2])
        instructor_email_entry.delete(0, tk.END)
        instructor_email_entry.insert(0, values[3])
        delete_instructor(values[1])
    elif values[4] == "Course":
        course_name_entry.delete(0, tk.END)
        course_name_entry.insert(0, values[0])
        course_id_entry.delete(0, tk.END)
        course_id_entry.insert(0, values[1])
        delete_course(values[1])
    messagebox.showinfo("Info", "Edit the fields and click 'Add' to save changes.")

def display_all_records():
    for row in tree.get_children():
        tree.delete(row)

    for student in get_all_students():
        tree.insert("", "end", values=(student[1], student[0], student[2], student[3], "Student"))
    
    for instructor in get_all_instructors():
        tree.insert("", "end", values=(instructor[1], instructor[0], instructor[2], instructor[3], "Instructor"))
    
    for course in get_all_courses():
        tree.insert("", "end", values=(course[1], course[0], "", "", "Course"))

root = tk.Tk()
root.title("School Management System")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)


tk.Label(frame, text="Student ID:").grid(row=0, column=0)
student_id_entry = tk.Entry(frame)
student_id_entry.grid(row=0, column=1)

tk.Label(frame, text="Name:").grid(row=1, column=0)
student_name_entry = tk.Entry(frame)
student_name_entry.grid(row=1, column=1)

tk.Label(frame, text="Age:").grid(row=2, column=0)
student_age_entry = tk.Entry(frame)
student_age_entry.grid(row=2, column=1)

tk.Label(frame, text="Email:").grid(row=3, column=0)
student_email_entry = tk.Entry(frame)
student_email_entry.grid(row=3, column=1)

tk.Button(frame, text="Add Student", command=add_student_record).grid(row=4, column=0, columnspan=2)


tk.Label(frame, text="Instructor ID:").grid(row=5, column=0)
instructor_id_entry = tk.Entry(frame)
instructor_id_entry.grid(row=5, column=1)

tk.Label(frame, text="Name:").grid(row=6, column=0)
instructor_name_entry = tk.Entry(frame)
instructor_name_entry.grid(row=6, column=1)

tk.Label(frame, text="Age:").grid(row=7, column=0)
instructor_age_entry = tk.Entry(frame)
instructor_age_entry.grid(row=7, column=1)

tk.Label(frame, text="Email:").grid(row=8, column=0)
instructor_email_entry = tk.Entry(frame)
instructor_email_entry.grid(row=8, column=1)

tk.Button(frame, text="Add Instructor", command=add_instructor_record).grid(row=9, column=0, columnspan=2)


tk.Label(frame, text="Course ID:").grid(row=10, column=0)
course_id_entry = tk.Entry(frame)
course_id_entry.grid(row=10, column=1)

tk.Label(frame, text="Course Name:").grid(row=11, column=0)
course_name_entry = tk.Entry(frame)
course_name_entry.grid(row=11, column=1)

tk.Label(frame, text="Instructor:").grid(row=12, column=0)
instructor_combobox = ttk.Combobox(frame)
instructor_combobox.grid(row=12, column=1)

tk.Button(frame, text="Add Course", command=add_course_record).grid(row=13, column=0, columnspan=2)


tk.Label(frame, text="Register Student:").grid(row=14, column=0)
student_combobox = ttk.Combobox(frame)
student_combobox.grid(row=14, column=1)

tk.Label(frame, text="Course:").grid(row=15, column=0)
course_combobox = ttk.Combobox(frame)
course_combobox.grid(row=15, column=1)

tk.Button(frame, text="Register", command=register_student).grid(row=16, column=0, columnspan=2)


columns = ("Name", "ID", "Age", "Email", "Type")
tree = ttk.Treeview(root, columns=columns, show='headings')
tree.heading("Name", text="Name")
tree.heading("ID", text="ID")
tree.heading("Age", text="Age")
tree.heading("Email", text="Email")
tree.heading("Type", text="Type")
tree.pack(padx=10, pady=10)

tk.Button(root, text="Display All Records", command=display_all_records).pack(pady=5)
tk.Button(root, text="Delete Selected Record", command=delete_record).pack(pady=5)
tk.Button(root, text="Edit Selected Record", command=edit_record).pack(pady=5)
tk.Button(root, text="Backup Database", command=backup_database).pack(pady=5)

update_comboboxes()

root.mainloop()
