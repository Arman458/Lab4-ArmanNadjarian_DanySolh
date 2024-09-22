import tkinter as tk
from tkinter import ttk, messagebox
import json
import re


class Person:
    def __init__(self, name, age, email):
        self.name = name
        self.age = age
        self._email = email

    def introduce(self):
        return f"Hello, my name is {self.name} and I am {self.age} years old."

class Student(Person):
    def __init__(self, name, age, email, student_id):
        super().__init__(name, age, email)
        self.student_id = student_id
        self.registered_courses = []

    def register_course(self, course):
        self.registered_courses.append(course)

class Instructor(Person):
    def __init__(self, name, age, email, instructor_id):
        super().__init__(name, age, email)
        self.instructor_id = instructor_id
        self.assigned_courses = []

    def assign_course(self, course):
        self.assigned_courses.append(course)

class Course:
    def __init__(self, course_id, course_name, instructor=None):
        self.course_id = course_id
        self.course_name = course_name
        self.instructor = instructor
        self.enrolled_students = []

    def add_student(self, student):
        self.enrolled_students.append(student)


def save_data():
    data = {
        "students": [{"name": s.name, "age": s.age, "email": s._email, "id": s.student_id} for s in students],
        "instructors": [{"name": i.name, "age": i.age, "email": i._email, "id": i.instructor_id} for i in instructors],
        "courses": [{"id": c.course_id, "name": c.course_name, "instructor": c.instructor.name if c.instructor else None, 
                     "students": [s.name for s in c.enrolled_students]} for c in courses]
    }
    with open("school_data.json", "w") as f:
        json.dump(data, f)

def load_data():
    global students, instructors, courses
    try:
        with open("school_data.json", "r") as f:
            data = json.load(f)
            students.clear()
            instructors.clear()
            courses.clear()

            for s in data["students"]:
                student = Student(s["name"], s["age"], s["email"], s["id"])
                students.append(student)

            for i in data["instructors"]:
                instructor = Instructor(i["name"], i["age"], i["email"], i["id"])
                instructors.append(instructor)

            for c in data["courses"]:
                instructor = next((i for i in instructors if i.name == c["instructor"]), None)
                course = Course(c["id"], c["name"], instructor)
                for s_name in c["students"]:
                    student = next((s for s in students if s.name == s_name), None)
                    if student:
                        course.add_student(student)
                courses.append(course)
    except FileNotFoundError:
        pass


def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

def is_valid_age(age):
    return age.isdigit() and int(age) >= 0


root = tk.Tk()
root.title("School Management System")
root.geometry("800x600")

students = []
instructors = []
courses = []

def update_comboboxes():
    student_combobox['values'] = [s.name for s in students]
    instructor_combobox['values'] = [i.name for i in instructors]
    course_combobox['values'] = [c.course_name for c in courses]

def add_student():
    student_name = student_name_entry.get()
    student_age = student_age_entry.get()
    student_email = student_email_entry.get()
    student_id = student_id_entry.get()
    
    if not is_valid_age(student_age):
        messagebox.showerror("Invalid Age", "Please enter a valid non-negative age.")
        return
    
    if not is_valid_email(student_email):
        messagebox.showerror("Invalid Email", "Please enter a valid email address.")
        return

    student = Student(student_name, int(student_age), student_email, student_id)
    students.append(student)
    update_comboboxes()
    messagebox.showinfo("Success", f"Student {student_name} added successfully!")
    save_data()

def add_instructor():
    instructor_name = instructor_name_entry.get()
    instructor_age = instructor_age_entry.get()
    instructor_email = instructor_email_entry.get()
    instructor_id = instructor_id_entry.get()
    
    if not is_valid_age(instructor_age):
        messagebox.showerror("Invalid Age", "Please enter a valid non-negative age.")
        return
    
    if not is_valid_email(instructor_email):
        messagebox.showerror("Invalid Email", "Please enter a valid email address.")
        return

    instructor = Instructor(instructor_name, int(instructor_age), instructor_email, instructor_id)
    instructors.append(instructor)
    update_comboboxes()
    messagebox.showinfo("Success", f"Instructor {instructor_name} added successfully!")
    save_data()

def add_course():
    course_name = course_name_entry.get()
    course_id = course_id_entry.get()

    course = Course(course_id, course_name)
    courses.append(course)
    update_comboboxes()
    messagebox.showinfo("Success", f"Course {course_name} added successfully!")
    save_data()

def register_student_for_course():
    selected_student = student_combobox.get()
    selected_course = course_combobox.get()

    for course in courses:
        if course.course_name == selected_course:
            for student in students:
                if student.name == selected_student:
                    course.add_student(student)
                    student.register_course(course)
                    messagebox.showinfo("Success", f"Student {student.name} registered for {course.course_name}!")
                    save_data()
                    return

def assign_instructor_to_course():
    selected_instructor = instructor_combobox.get()
    selected_course = course_combobox.get()

    for course in courses:
        if course.course_name == selected_course:
            for instructor in instructors:
                if instructor.name == selected_instructor:
                    course.instructor = instructor
                    instructor.assign_course(course)
                    messagebox.showinfo("Success", f"Instructor {instructor.name} assigned to {course.course_name} with students {[s.name for s in course.enrolled_students]}!")
                    save_data()
                    return

def display_all_records():
    for row in tree.get_children():
        tree.delete(row)

    for student in students:
        tree.insert("", "end", values=(student.name, student.student_id, student.age, student._email, "Student"))

    for instructor in instructors:
        tree.insert("", "end", values=(instructor.name, instructor.instructor_id, instructor.age, instructor._email, "Instructor"))

    for course in courses:
        enrolled_students = ', '.join([student.name for student in course.enrolled_students]) or "None"
        instructor_name = course.instructor.name if course.instructor else "None"
        tree.insert("", "end", values=(course.course_name, course.course_id, "Enrolled Students", enrolled_students, "Course"))
        tree.insert("", "end", values=(course.course_name, course.course_id, "Instructor", instructor_name, "Course"))

def delete_record():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select a record to delete.")
        return

    values = tree.item(selected_item, 'values')
    
    if values[4] == "Student":
        students[:] = [s for s in students if s.student_id != values[1]]
    elif values[4] == "Instructor":
        instructors[:] = [i for i in instructors if i.instructor_id != values[1]]
    elif values[4] == "Course":
        courses[:] = [c for c in courses if c.course_id != values[1]]

    tree.delete(selected_item)
    save_data()
    messagebox.showinfo("Success", "Record deleted successfully.")

def edit_record():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select a record to edit.")
        return

    values = tree.item(selected_item, 'values')
    
    if values[4] == "Student":
        for student in students:
            if student.student_id == values[1]:
                student_name_entry.delete(0, tk.END)
                student_name_entry.insert(0, student.name)
                student_age_entry.delete(0, tk.END)
                student_age_entry.insert(0, student.age)
                student_email_entry.delete(0, tk.END)
                student_email_entry.insert(0, student._email)
                student_id_entry.delete(0, tk.END)
                student_id_entry.insert(0, student.student_id)
                students.remove(student)
                break
    elif values[4] == "Instructor":
        for instructor in instructors:
            if instructor.instructor_id == values[1]:
                instructor_name_entry.delete(0, tk.END)
                instructor_name_entry.insert(0, instructor.name)
                instructor_age_entry.delete(0, tk.END)
                instructor_age_entry.insert(0, instructor.age)
                instructor_email_entry.delete(0, tk.END)
                instructor_email_entry.insert(0, instructor._email)
                instructor_id_entry.delete(0, tk.END)
                instructor_id_entry.insert(0, instructor.instructor_id)
                instructors.remove(instructor)
                break
    elif values[4] == "Course":
        for course in courses:
            if course.course_id == values[1]:
                course_name_entry.delete(0, tk.END)
                course_name_entry.insert(0, course.course_name)
                course_id_entry.delete(0, tk.END)
                course_id_entry.insert(0, course.course_id)
                courses.remove(course)
                break
    messagebox.showinfo("Info", "Edit the fields and click 'Add' to save changes.")

def search_records():
    query = search_entry.get().lower()
    for row in tree.get_children():
        tree.delete(row)

    for student in students:
        if query in student.name.lower() or query in student.student_id:
            tree.insert("", "end", values=(student.name, student.student_id, student.age, student._email, "Student"))

    for instructor in instructors:
        if query in instructor.name.lower() or query in instructor.instructor_id:
            tree.insert("", "end", values=(instructor.name, instructor.instructor_id, instructor.age, instructor._email, "Instructor"))

    for course in courses:
        if query in course.course_name.lower() or query in course.course_id:
            tree.insert("", "end", values=(course.course_name, course.course_id, "N/A", course.instructor.name if course.instructor else "None", "Course"))

form_frame = tk.Frame(root)
form_frame.pack(pady=10)

tk.Label(form_frame, text="Student Name:").grid(row=0, column=0)
student_name_entry = tk.Entry(form_frame)
student_name_entry.grid(row=0, column=1)

tk.Label(form_frame, text="Student Age:").grid(row=1, column=0)
student_age_entry = tk.Entry(form_frame)
student_age_entry.grid(row=1, column=1)

tk.Label(form_frame, text="Student Email:").grid(row=2, column=0)
student_email_entry = tk.Entry(form_frame)
student_email_entry.grid(row=2, column=1)

tk.Label(form_frame, text="Student ID:").grid(row=3, column=0)
student_id_entry = tk.Entry(form_frame)
student_id_entry.grid(row=3, column=1)

tk.Label(form_frame, text="Instructor Name:").grid(row=4, column=0)
instructor_name_entry = tk.Entry(form_frame)
instructor_name_entry.grid(row=4, column=1)

tk.Label(form_frame, text="Instructor Age:").grid(row=5, column=0)
instructor_age_entry = tk.Entry(form_frame)
instructor_age_entry.grid(row=5, column=1)

tk.Label(form_frame, text="Instructor Email:").grid(row=6, column=0)
instructor_email_entry = tk.Entry(form_frame)
instructor_email_entry.grid(row=6, column=1)

tk.Label(form_frame, text="Instructor ID:").grid(row=7, column=0)
instructor_id_entry = tk.Entry(form_frame)
instructor_id_entry.grid(row=7, column=1)

tk.Label(form_frame, text="Course Name:").grid(row=8, column=0)
course_name_entry = tk.Entry(form_frame)
course_name_entry.grid(row=8, column=1)

tk.Label(form_frame, text="Course ID:").grid(row=9, column=0)
course_id_entry = tk.Entry(form_frame)
course_id_entry.grid(row=9, column=1)

tk.Label(form_frame, text="Select Student:").grid(row=10, column=0)
student_combobox = ttk.Combobox(form_frame)
student_combobox.grid(row=10, column=1)

tk.Label(form_frame, text="Select Instructor:").grid(row=11, column=0)
instructor_combobox = ttk.Combobox(form_frame)
instructor_combobox.grid(row=11, column=1)

tk.Label(form_frame, text="Select Course:").grid(row=12, column=0)
course_combobox = ttk.Combobox(form_frame)
course_combobox.grid(row=12, column=1)

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

tk.Button(button_frame, text="Add Student", command=add_student).grid(row=0, column=0, padx=5)
tk.Button(button_frame, text="Add Instructor", command=add_instructor).grid(row=0, column=1, padx=5)
tk.Button(button_frame, text="Add Course", command=add_course).grid(row=0, column=2, padx=5)
tk.Button(button_frame, text="Register Student for Course", command=register_student_for_course).grid(row=1, column=0, padx=5)
tk.Button(button_frame, text="Assign Instructor to Course", command=assign_instructor_to_course).grid(row=1, column=1, padx=5)
tk.Button(button_frame, text="Display All Records", command=display_all_records).grid(row=1, column=2, padx=5)

columns = ("Name", "ID", "Age", "Email", "Type")
tree = ttk.Treeview(root, columns=columns, show="headings")
tree.heading("Name", text="Name")
tree.heading("ID", text="ID")
tree.heading("Age", text="Age")
tree.heading("Email", text="Email")
tree.heading("Type", text="Type")
tree.pack(pady=10)

tk.Label(root, text="Search by Name/ID/Course:").pack(pady=5)
search_entry = tk.Entry(root)
search_entry.pack(pady=5)
tk.Button(root, text="Search", command=search_records).pack(pady=5)


tk.Button(button_frame, text="Delete Record", command=delete_record).grid(row=2, column=0, padx=5)
tk.Button(button_frame, text="Edit Record", command=edit_record).grid(row=2, column=1, padx=5)


tk.Button(button_frame, text="Save Data", command=lambda: [save_data(), messagebox.showinfo("Success", "Data saved!")]).grid(row=3, column=0, padx=5)
tk.Button(button_frame, text="Load Data", command=lambda: [load_data(), update_comboboxes(), display_all_records(), messagebox.showinfo("Success", "Data loaded!")]).grid(row=3, column=1, padx=5)


load_data()
update_comboboxes()

root.mainloop()
