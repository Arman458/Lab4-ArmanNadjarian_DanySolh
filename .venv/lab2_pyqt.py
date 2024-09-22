import sys
import json
import csv
import sqlite3
import re
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QComboBox,QMessageBox, QTableWidget, QTableWidgetItem, QFileDialog, QHeaderView, QDialog, QGridLayout, QHBoxLayout)
from PyQt5.QtGui import QIcon  



def init_db():
    """
    Initializes the SQLite database by creating necessary tables if they do not already exist.

    **docstring** 
    """
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            email TEXT NOT NULL UNIQUE,
            student_id TEXT NOT NULL UNIQUE
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS instructors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            email TEXT NOT NULL UNIQUE,
            instructor_id TEXT NOT NULL UNIQUE
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_id TEXT NOT NULL UNIQUE,
            course_name TEXT NOT NULL,
            instructor_id INTEGER,
            FOREIGN KEY (instructor_id) REFERENCES instructors(id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS enrollments (
            student_id INTEGER,
            course_id INTEGER,
            FOREIGN KEY (student_id) REFERENCES students(id),
            FOREIGN KEY (course_id) REFERENCES courses(id)
        )
    ''')
    conn.commit()
    conn.close()

def add_student_to_db(name, age, email, student_id):
    """
    Adds a new student to the database.

    **Sphinx-style documentation**

    :param name: The student's full name.
    :type name: str
    :param age: The student's age, must be a positive integer.
    :type age: int
    :param email: The student's email address.
    :type email: str
    :param student_id: A unique identifier for the student.
    :type student_id: str
    :raises sqlite3.IntegrityError: If the student ID or email is already in use.
    :return: True if the student is added successfully, False if there's an IntegrityError.
    :rtype: bool
    """
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO students (name, age, email, student_id)
            VALUES (?, ?, ?, ?)
        ''', (name, age, email, student_id))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return False
    conn.close()
    return True

def add_instructor_to_db(name, age, email, instructor_id):
    """
    **Sphinx-style documentation**
    Adds a new instructor to the database.

    :param name: The instructor's full name.
    :type name: str
    :param age: The instructor's age, must be a positive integer.
    :type age: int
    :param email: The instructor's email address.
    :type email: str
    :param instructor_id: A unique identifier for the instructor.
    :type instructor_id: str
    :raises sqlite3.IntegrityError: If the instructor ID or email is already in use.
    :return: True if the instructor is added successfully, False if there's an IntegrityError.
    :rtype: bool
    """
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO instructors (name, age, email, instructor_id)
            VALUES (?, ?, ?, ?)
        ''', (name, age, email, instructor_id))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return False
    conn.close()
    return True


def add_course_to_db(course_id, course_name):
    """
    **Sphinx-style documentation**
    Adds a new course to the database.

    :param course_id: The unique ID for the course.
    :type course_id: str
    :param course_name: The name of the course.
    :type course_name: str
    :raises sqlite3.IntegrityError: If the course ID already exists.
    :return: True if the course is added successfully, False if there's an IntegrityError.
    :rtype: bool
    """
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO courses (course_id, course_name)
            VALUES (?, ?)
        ''', (course_id, course_name))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return False
    conn.close()
    return True

def fetch_all_students():
    """
    Fetches all students from the database.

    **Sphinx-style documentation** 

    :return: A list of student records, where each record contains:
        - ID (int)
        - Name (str)
        - Age (int)
        - Email (str)
        - Student ID (str)
    :rtype: list
    """
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM students')
    students = cursor.fetchall()
    conn.close()
    return students

def update_student_in_db(old_student_id, new_student_id, new_name, new_age, new_email):
    """
    **Sphinx-style documentation** 
    Updates an existing student's details in the database, including the ID.

    :param old_student_id: The current student ID.
    :type old_student_id: str
    :param new_student_id: The updated student ID.
    :type new_student_id: str
    :param new_name: The updated student name.
    :type new_name: str
    :param new_age: The updated student age.
    :type new_age: int
    :param new_email: The updated student email address.
    :type new_email: str
    :raises sqlite3.IntegrityError: If the new student ID or email is not unique.
    :return: None
    """
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''
            UPDATE students
            SET student_id=?, name=?, age=?, email=?
            WHERE student_id=?
        ''', (new_student_id, new_name, new_age, new_email, old_student_id))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return False
    conn.close()
    return True


def delete_student_from_db(student_id):
    """
    Deletes a student from the database using the provided student ID.

     **regular docstring** 
    """
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM students WHERE student_id=?', (student_id,))
    conn.commit()
    conn.close()


def update_instructor_in_db(old_instructor_id, new_instructor_id, new_name, new_age, new_email):
    """
    Updates an existing instructor's details in the database, including the ID.

    **Sphinx-style documentation** 
    :param old_instructor_id: The current instructor ID.
    :type old_instructor_id: str
    :param new_instructor_id: The updated instructor ID.
    :type new_instructor_id: str
    :param new_name: The updated instructor name.
    :type new_name: str
    :param new_age: The updated instructor age.
    :type new_age: int
    :param new_email: The updated instructor email address.
    :type new_email: str
    :raises sqlite3.IntegrityError: If the new instructor ID or email is not unique.
    :return: None
    """
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''
            UPDATE instructors
            SET instructor_id=?, name=?, age=?, email=?
            WHERE instructor_id=?
        ''', (new_instructor_id, new_name, new_age, new_email, old_instructor_id))
        conn.commit()
    except sqlite3.IntegrityError as e:
        raise sqlite3.IntegrityError(f"Update failed: {str(e)}")
    finally:
        conn.close()

def fetch_all_instructors():
    """
    Fetches all instructors from the database.

    **Sphinx-style documentation** 

    :return: A list of instructor records, where each record contains:
        - ID (int)
        - Name (str)
        - Age (int)
        - Email (str)
        - Instructor ID (str)
    :rtype: list
    """
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM instructors')
    instructors = cursor.fetchall()
    conn.close()
    return instructors


def delete_instructor_from_db(instructor_id):
    """
    **docsting documentation**
    Deletes an instructor from the database based on the provided instructor ID.
    """
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM instructors WHERE instructor_id=?', (instructor_id,))
    conn.commit()
    conn.close()



def update_course_in_db(old_course_id, new_course_id, new_name):
    """
    Updates the course's details in the database, including the course ID.

    **Sphinx-style documentation**

    :param old_course_id: The current course ID.
    :type old_course_id: str
    :param new_course_id: The updated course ID.
    :type new_course_id: str
    :param new_name: The updated course name.
    :type new_name: str
    :raises sqlite3.IntegrityError: If the new course ID already exists in the database.
    :return: True if the update was successful, False if there was an IntegrityError.
    :rtype: bool
    """
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''
            UPDATE courses
            SET course_id=?, course_name=?
            WHERE course_id=?
        ''', (new_course_id, new_name, old_course_id))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False
    finally:
        conn.close()



def fetch_all_courses():
    """
    Fetches all courses from the database.

    **Sphinx-style documentation**

    :return: A list of course records, where each record contains:
        - ID (int)
        - Course ID (str)
        - Course Name (str)
        - Instructor ID (int, nullable)
    :rtype: list
    """
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM courses')
    courses = cursor.fetchall()
    conn.close()
    return courses


def delete_course_from_db(course_id):
    """
    **docstring documentation**
    Deletes a course from the database using the provided course ID.
    """
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM courses WHERE course_id=?', (course_id,))
    conn.commit()
    conn.close()

def assign_instructor_to_course(instructor_id, course_id):
    """
    Assigns an instructor to a course.

     **Sphinx-style documentation**

    :param instructor_id: The unique identifier of the instructor to assign.
    :type instructor_id: str
    :param course_id: The unique identifier of the course to which the instructor is assigned.
    :type course_id: str
    :raises sqlite3.IntegrityError: If there's an issue with the instructor or course ID.
    :return: True if the instructor is assigned successfully, False if an IntegrityError occurs.
    :rtype: bool
    """
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''
            UPDATE courses
            SET instructor_id = (
                SELECT id FROM instructors WHERE instructor_id=?
            )
            WHERE course_id = ?
        ''', (instructor_id, course_id))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return False
    conn.close()
    return True


def enroll_student_in_course(student_id, course_id):
    """
    Enrolls a student in a course by adding a record to the enrollments table.

    **Sphinx-style documentation** 

    :param student_id: The unique identifier of the student to enroll.
    :type student_id: str
    :param course_id: The unique identifier of the course.
    :type course_id: str
    :raises sqlite3.IntegrityError: If the student is already enrolled in the course.
    :return: True if the student was successfully enrolled, False otherwise.
    :rtype: bool
    """
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO enrollments (student_id, course_id)
            VALUES (
                (SELECT id FROM students WHERE student_id=?),
                (SELECT id FROM courses WHERE course_id=?)
            )
        ''', (student_id, course_id))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return False
    conn.close()
    return True

def is_valid_email(email):
    """
    **docstring**
    Validates if the given email is in the correct format 
    """
    return re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email)

def is_valid_age(age):
    """
    **docstring**
    Validates if the given age is a positive integer.
    """
    return age.isdigit() and int(age) >= 0

def save_data_to_json():
    """
    Saves all data (students, instructors, and courses) into a JSON file.

    **Docstring**
    """
    data = {
        'students': fetch_all_students(),
        'instructors': fetch_all_instructors(),
        'courses': fetch_all_courses()
    }
    filename, _ = QFileDialog.getSaveFileName(None, "Save Data", "", "JSON Files (*.json)")
    if filename:
        with open(filename, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        QMessageBox.information(None, "Success", "Data saved to JSON file.")

def load_data_from_json():
    """
    Loads data from a JSON file into the application.
    **docstring** 
    """
    filename, _ = QFileDialog.getOpenFileName(None, "Open Data", "", "JSON Files (*.json)")
    if filename:
        with open(filename, 'r') as json_file:
            data = json.load(json_file)
        QMessageBox.information(None, "Success", "Data loaded from JSON file.")

def export_to_csv():
    """
    Exports student, instructor, and course data into a CSV file.
    **docsting** 
    """
    students = fetch_all_students()
    instructors = fetch_all_instructors()
    courses = fetch_all_courses()

    path, _ = QFileDialog.getSaveFileName(None, "Export CSV", "", "CSV Files (*.csv)")
    if path:
        with open(path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Type", "Name", "ID", "Age", "Email/Course ID"])
            for student in students:
                writer.writerow(["Student", student[1], student[4], student[2], student[3]])
            for instructor in instructors:
                writer.writerow(["Instructor", instructor[1], instructor[4], instructor[2], instructor[3]])
            for course in courses:
                instructor_name = "None" if course[3] is None else f"Instructor ID: {course[3]}"
                writer.writerow(["Course", course[2], course[1], "N/A", instructor_name])
        QMessageBox.information(None, "Success", "Data exported to CSV file.")

def backup_database():
    """
    Creates a backup of the database file.

    **docstring** 
    """
    conn = sqlite3.connect('school.db')
    backup_file, _ = QFileDialog.getSaveFileName(None, "Backup Database", "", "SQLite Database (*.db)")
    if backup_file:
        with open(backup_file, 'wb') as f:
            for line in conn.iterdump():
                f.write(f'{line}\n'.encode())
        QMessageBox.information(None, "Backup", "Database backup successful.")
    conn.close()

class SchoolManagementSystem(QWidget):
    """
    Main window for the School Management System application.

    - Defines the GUI for adding students, instructors, and courses.
    - Allows managing registrations and assignments.

    **docstring** 
    """

    def __init__(self):
        """
        Initializes the SchoolManagementSystem application.

        **docstring**
        """
        super().__init__()
        self.initUI()

    def initUI(self):
        """
        Sets up the layout and UI components for the main window of the application.

        This method creates input fields for adding students, instructors, and courses, configures buttons for the fucntions (like registering students, assigning instructors), 
        and sets up the layout for navigating the application's features.

        Components:
        - Input fields for students (name, age, email, ID)
        - Buttons for adding students, instructors, and courses
        - Input fields for instructors (name, age, email, ID)
        - Buttons for registering students and assigning instructors
        - Input fields for courses (course name, course ID)
        - Buttons for exporting data, saving data, loading data, and backing up the database
        - Dropdown menus for student and course selection
        - A table widget to display the list of students, instructors, and courses.
        """
        self.setWindowTitle("School Management System")
        self.setGeometry(100, 100, 600, 800)

        main_layout = QVBoxLayout()

        main_layout.addWidget(QLabel("Add Student"))
        self.student_name_input = QLineEdit()
        self.student_name_input.setPlaceholderText("Enter student name")
        main_layout.addWidget(self.student_name_input)

        self.student_age_input = QLineEdit()
        self.student_age_input.setPlaceholderText("Enter student age")
        main_layout.addWidget(self.student_age_input)

        self.student_email_input = QLineEdit()
        self.student_email_input.setPlaceholderText("Enter student email")
        main_layout.addWidget(self.student_email_input)

        self.student_id_input = QLineEdit()
        self.student_id_input.setPlaceholderText("Enter student ID")
        main_layout.addWidget(self.student_id_input)

        self.add_student_btn = QPushButton("Add Student")
        self.add_student_btn.clicked.connect(self.add_student)
        main_layout.addWidget(self.add_student_btn)

        main_layout.addWidget(QLabel("Add Instructor"))
        self.instructor_name_input = QLineEdit()
        self.instructor_name_input.setPlaceholderText("Enter instructor name")
        main_layout.addWidget(self.instructor_name_input)

        self.instructor_age_input = QLineEdit()
        self.instructor_age_input.setPlaceholderText("Enter instructor age")
        main_layout.addWidget(self.instructor_age_input)

        self.instructor_email_input = QLineEdit()
        self.instructor_email_input.setPlaceholderText("Enter instructor email")
        main_layout.addWidget(self.instructor_email_input)

        self.instructor_id_input = QLineEdit()
        self.instructor_id_input.setPlaceholderText("Enter instructor ID")
        main_layout.addWidget(self.instructor_id_input)

        self.add_instructor_btn = QPushButton("Add Instructor")
        self.add_instructor_btn.clicked.connect(self.add_instructor)
        main_layout.addWidget(self.add_instructor_btn)

        main_layout.addWidget(QLabel("Add Course"))
        self.course_name_input = QLineEdit()
        self.course_name_input.setPlaceholderText("Enter course name")
        main_layout.addWidget(self.course_name_input)

        self.course_id_input = QLineEdit()
        self.course_id_input.setPlaceholderText("Enter course ID")
        main_layout.addWidget(self.course_id_input)

        self.add_course_btn = QPushButton("Add Course")
        self.add_course_btn.clicked.connect(self.add_course)
        main_layout.addWidget(self.add_course_btn)

        main_layout.addWidget(QLabel("Register Student for Course"))
        self.student_dropdown = QComboBox()
        main_layout.addWidget(self.student_dropdown)

        self.course_dropdown = QComboBox()
        main_layout.addWidget(self.course_dropdown)

        self.register_student_btn = QPushButton("Register Student")
        self.register_student_btn.clicked.connect(self.register_student)
        main_layout.addWidget(self.register_student_btn)

        main_layout.addWidget(QLabel("Assign Instructor to Course"))
        self.instructor_dropdown = QComboBox()
        main_layout.addWidget(self.instructor_dropdown)

        self.course_assign_dropdown = QComboBox()
        main_layout.addWidget(self.course_assign_dropdown)

        self.assign_instructor_btn = QPushButton("Assign Instructor")
        self.assign_instructor_btn.clicked.connect(self.assign_instructor)
        main_layout.addWidget(self.assign_instructor_btn)

        search_layout = QVBoxLayout()
        search_layout.addWidget(QLabel("Search:"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by name, ID, or course")
        self.search_input.textChanged.connect(self.search_records)
        search_layout.addWidget(self.search_input)
        main_layout.addLayout(search_layout)

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(7)
        self.table_widget.setHorizontalHeaderLabels(["Name", "ID", "Age", "Email", "Type", "Edit", "Delete"])
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        main_layout.addWidget(self.table_widget)

        self.export_btn = QPushButton("Export to CSV")
        self.export_btn.clicked.connect(export_to_csv)
        main_layout.addWidget(self.export_btn)

        self.save_data_btn = QPushButton("Save Data")
        self.save_data_btn.clicked.connect(save_data_to_json)
        main_layout.addWidget(self.save_data_btn)

        self.load_data_btn = QPushButton("Load Data")
        self.load_data_btn.clicked.connect(load_data_from_json)
        main_layout.addWidget(self.load_data_btn)

        self.backup_btn = QPushButton("Backup Database")
        self.backup_btn.clicked.connect(backup_database)
        main_layout.addWidget(self.backup_btn)

        self.setLayout(main_layout)
        self.update_dropdowns()
        self.display_all_records()

    def update_dropdowns(self):
        """
        Updates the student, instructor, and course dropdown menus with the latest data from the database.
        **docstring** 
        """
        self.course_dropdown.clear()
        self.course_dropdown.addItem("Select Course")
        self.course_assign_dropdown.clear()
        self.course_assign_dropdown.addItem("Select Course")

        courses = fetch_all_courses()
        for course in courses:
            self.course_dropdown.addItem(f"{course[1]} - {course[2]}")
            self.course_assign_dropdown.addItem(f"{course[1]} - {course[2]}")

        self.student_dropdown.clear()
        self.student_dropdown.addItem("Select Student")
        students = fetch_all_students()
        for student in students:
            self.student_dropdown.addItem(f"{student[4]} - {student[1]}")

        self.instructor_dropdown.clear()
        self.instructor_dropdown.addItem("Select Instructor")
        instructors = fetch_all_instructors()
        for instructor in instructors:
            self.instructor_dropdown.addItem(f"{instructor[4]} - {instructor[1]}")

    def add_student(self):
        """
        Adds a new student to the database.

        **Sphinx-style documentation**

        :param name: The student's full name.
        :type name: str
        :param age: The student's age, must be a positive integer.
        :type age: int
        :param email: The student's email address.
        :type email: str
        :param student_id: A unique identifier for the student.
        :type student_id: str

        :raises sqlite3.IntegrityError: If the student ID or email is already in use.

        :return: True if the student is added successfully, False if there's an IntegrityError.
        :rtype: bool
        """
        name = self.student_name_input.text().strip()
        age = self.student_age_input.text().strip()
        email = self.student_email_input.text().strip()
        student_id = self.student_id_input.text().strip()

        if not name or not is_valid_age(age) or not is_valid_email(email) or not student_id:
            QMessageBox.warning(self, "Input Error", "Please fill all student fields correctly.")
            return

        if add_student_to_db(name, int(age), email, student_id):
            QMessageBox.information(self, "Success", f"Student {name} added successfully!")
            self.update_dropdowns()
            self.display_all_records()
            self.student_name_input.clear()
            self.student_age_input.clear()
            self.student_email_input.clear()
            self.student_id_input.clear()
        else:
            QMessageBox.warning(self, "Error", "Could not add student. Email or Student ID may already be in use.")

    def add_instructor(self):
        """
        Adds an instructor using the input data provided in the GUI.

        This method retrieves input data for the instructor (name, age, email, and instructor ID), validates it, and adds the instructor to the database if the data is valid.
        It also updates the dropdowns and table view after successfully adding the instructor.

        If the input fields are invalid, it shows a warning message to the user.

        **docstring**
        """
        name = self.instructor_name_input.text().strip()
        age = self.instructor_age_input.text().strip()
        email = self.instructor_email_input.text().strip()
        instructor_id = self.instructor_id_input.text().strip()

        if not name or not is_valid_age(age) or not is_valid_email(email) or not instructor_id:
            QMessageBox.warning(self, "Input Error", "Please fill all instructor fields correctly.")
            return

        if add_instructor_to_db(name, int(age), email, instructor_id):
            QMessageBox.information(self, "Success", f"Instructor {name} added successfully!")
            self.update_dropdowns()
            self.display_all_records()
            self.instructor_name_input.clear()
            self.instructor_age_input.clear()
            self.instructor_email_input.clear()
            self.instructor_id_input.clear()
        else:
            QMessageBox.warning(self, "Error", "Could not add instructor. Email or Instructor ID may already be in use.")

    def add_course(self):
        """
        Adds a course using the input data provided in the GUI.

        This method retrieves input data for the course (course name and course ID),validates them to ensure both fields are filled, and then adds the course to the database if the data is valid.

        If the input fields are invalid (e.g., missing course name or ID), it displaysa warning message to the user.

        **docstring**
        """
        course_name = self.course_name_input.text().strip()
        course_id = self.course_id_input.text().strip()

        if not course_name or not course_id:
            QMessageBox.warning(self, "Input Error", "Please fill all course fields correctly.")
            return

        if add_course_to_db(course_id, course_name):
            QMessageBox.information(self, "Success", f"Course {course_name} added successfully!")
            self.update_dropdowns()
            self.display_all_records()
            self.course_name_input.clear()
            self.course_id_input.clear()
        else:
            QMessageBox.warning(self, "Error", "Could not add course. Course ID may already be in use.")

    def register_student(self):
        """
        Registers a selected student for a selected course.

        This method retrieves the selected student and course from the dropdown menus,validates that both have been selected, and enrolls the student in the selected course.
        If no student or course is selected, it shows a warning message to the user.

        Updates the table view after a successful registration.
        
        **docstring**
        """
        selected_student = self.student_dropdown.currentText()
        selected_course = self.course_dropdown.currentText()

        if selected_student == "Select Student" or selected_course == "Select Course":
            QMessageBox.warning(self, "Input Error", "Please select both a student and a course.")
            return

        student_id = selected_student.split(" - ")[0]
        course_id = selected_course.split(" - ")[0]

        if enroll_student_in_course(student_id, course_id):
            QMessageBox.information(self, "Success", f"Student {selected_student} registered for {selected_course}!")
            self.display_all_records()
        else:
            QMessageBox.warning(self, "Error", "Could not register student. They might already be enrolled in this course.")

    def assign_instructor(self):
        """
        Assigns an instructor to a selected course.

        This method retrieves the selected instructor and course from the dropdown menus, validates that both have been selected, and assigns the instructor to the course.
        If no instructor or course is selected, it shows a warning message to the user.

        Updates the table view after successfully assigning the instructor.

        **docstring**
        """
        selected_instructor = self.instructor_dropdown.currentText()
        selected_course = self.course_assign_dropdown.currentText()

        if selected_instructor == "Select Instructor" or selected_course == "Select Course":
            QMessageBox.warning(self, "Input Error", "Please select both an instructor and a course.")
            return

        instructor_id = selected_instructor.split(" - ")[0]
        course_id = selected_course.split(" - ")[0]

        if assign_instructor_to_course(instructor_id, course_id):
            QMessageBox.information(self, "Success", f"Instructor {selected_instructor} assigned to {selected_course}!")
            self.display_all_records()
        else:
            QMessageBox.warning(self, "Error", "Could not assign instructor. Please check the selected IDs.")

    def display_all_records(self):
        """
        Displays all student, instructor, and course records in the table widget.

        This method retrieves data from the database for students, instructors, and courses, and populates the table widget with the retrieved data. 
        It also adds options to edit and delete each record, updating the UI to reflect the current state of the database.

        The table displays the following:
        - Student records with name, ID, age, email, and options for editing/deleting.
        - Instructor records with name, ID, age, email, and options for editing/deleting.
        - Course records with course name, course ID, assigned instructor, and options for editing/deleting.

        **docstring**
        """
        self.table_widget.setRowCount(0)

        students = fetch_all_students()
        for student in students:
            row_position = self.table_widget.rowCount()
            self.table_widget.insertRow(row_position)
            self.table_widget.setItem(row_position, 0, QTableWidgetItem(student[1]))  
            self.table_widget.setItem(row_position, 1, QTableWidgetItem(student[4])) 
            self.table_widget.setItem(row_position, 2, QTableWidgetItem(str(student[2])))  
            self.table_widget.setItem(row_position, 3, QTableWidgetItem(student[3]))  
            self.table_widget.setItem(row_position, 4, QTableWidgetItem("Student"))  
            self.table_widget.setCellWidget(row_position, 5, self.create_edit_button("Student", student))
            self.table_widget.setCellWidget(row_position, 6, self.create_delete_button("Student", student))

        instructors = fetch_all_instructors()
        for instructor in instructors:
            row_position = self.table_widget.rowCount()
            self.table_widget.insertRow(row_position)
            self.table_widget.setItem(row_position, 0, QTableWidgetItem(instructor[1])) 
            self.table_widget.setItem(row_position, 1, QTableWidgetItem(instructor[4]))  
            self.table_widget.setItem(row_position, 2, QTableWidgetItem(str(instructor[2])))  
            self.table_widget.setItem(row_position, 3, QTableWidgetItem(instructor[3]))  
            self.table_widget.setItem(row_position, 4, QTableWidgetItem("Instructor"))  
            self.table_widget.setCellWidget(row_position, 5, self.create_edit_button("Instructor", instructor))
            self.table_widget.setCellWidget(row_position, 6, self.create_delete_button("Instructor", instructor))

        courses = fetch_all_courses()
        for course in courses:
            row_position = self.table_widget.rowCount()
            self.table_widget.insertRow(row_position)
            self.table_widget.setItem(row_position, 0, QTableWidgetItem(course[2]))  
            self.table_widget.setItem(row_position, 1, QTableWidgetItem(course[1]))  
            self.table_widget.setItem(row_position, 2, QTableWidgetItem("N/A"))  
            instructor_name = "None" if course[3] is None else f"Instructor ID: {course[3]}"
            self.table_widget.setItem(row_position, 3, QTableWidgetItem(instructor_name))  
            self.table_widget.setItem(row_position, 4, QTableWidgetItem("Course")) 
            self.table_widget.setCellWidget(row_position, 5, self.create_edit_button("Course", course))
            self.table_widget.setCellWidget(row_position, 6, self.create_delete_button("Course", course))

    def create_edit_button(self, record_type, record):
        """
        **Sphinx-style documentation** 
        Creates an edit button for a wow in the table, allowing editing of records
        :param record_type: it specifies thr type of the record (Student, Instructor, or Course)
        :type record_type: str
        :param record: The record details to be edited.
        :type record: tuple
        :return: A QPushButton widget for editing the record.
        :rtype: QPushButton
        """
        edit_button = QPushButton("Edit")
        edit_button.clicked.connect(lambda: self.edit_record(record_type, record))
        return edit_button

    def create_delete_button(self, record_type, record):
        """
        **Sphinx-style documentation** 
        Creates a delete button for a table row, allowing deletion of records.

        :param record_type: Type of the record (Student, Instructor, or Course).
        :type record_type: str
        :param record: The record details to be deleted.
        :type record: tuple
        :return: A QPushButton widget for deleting the record.
        :rtype: QPushButton
        """
        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(lambda: self.delete_record(record_type, record))
        return delete_button

    def edit_record(self, record_type, record):
        """
        **Sphinx-style documentation** 
        Opens an edit dialog based on the record type.

        :param record_type: Type of the record (Student, Instructor, or Course).
        :type record_type: str
        :param record: The record details to be edited.
        :type record: tuple
        :return: None
        """
        if record_type == "Student":
            self.edit_student(record)
        elif record_type == "Instructor":
            self.edit_instructor(record)
        elif record_type == "Course":
            self.edit_course(record)

    def delete_record(self, record_type, record):
        """
        **Sphinx-style documentation** 
        Deletes a record based on its type and updates the table.

        :param record_type: Type of the record (Student, Instructor, or Course).
        :type record_type: str
        :param record: The record details to be deleted.
        :type record: tuple
        :return: None
        """
        if record_type == "Student":
            self.delete_student(record)
        elif record_type == "Instructor":
            self.delete_instructor(record)
        elif record_type == "Course":
            self.delete_course(record)

    def edit_student(self, student):
        """
        **Sphinx-style documentation** 
        Opens the edit dialog for a student and updates the database after validation

        :param student: The student record to edit.
        :type student: tuple
        :return: None
        """
        dialog = EditDialog("Student", student)
        if dialog.exec_():
            new_student_id, new_name, new_age, new_email = dialog.get_inputs()
            if not new_name or not is_valid_age(new_age) or not is_valid_email(new_email):
                QMessageBox.warning(self, "Input Error", "Please provide valid data.")
                return
            update_student_in_db(student[4], new_student_id, new_name, int(new_age), new_email)
            QMessageBox.information(self, "Success", "Student updated successfully.")
            self.update_dropdowns()
            self.display_all_records()

    def delete_student(self, student):
        """
        **Sphinx-style documentation** 
        Deletes the student record from the database after confirmation.

        :param student: The student record to delete.
        :type student: tuple
        :return: None
        """
        reply = QMessageBox.question(self, 'Confirm Delete',
                                     f"Are you sure you want to delete student {student[1]}?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            delete_student_from_db(student[4])
            QMessageBox.information(self, "Success", "Student deleted successfully.")
            self.update_dropdowns()
            self.display_all_records()

    def edit_instructor(self, instructor):
        """
        **Sphinx-style documentation** 
        Opens the edit dialog for an instructor and updates the database.

        :param instructor: The instructor record to edit.
        :type instructor: tuple
        :return: None
        """
        dialog = EditDialog("Instructor", instructor)
        if dialog.exec_():
            new_instructor_id, new_name, new_age, new_email = dialog.get_inputs()
            if not new_name or not is_valid_age(new_age) or not is_valid_email(new_email):
                QMessageBox.warning(self, "Input Error", "Please provide valid data.")
                return
            update_instructor_in_db(instructor[4], new_instructor_id, new_name, int(new_age), new_email)
            QMessageBox.information(self, "Success", "Instructor updated successfully.")
            self.update_dropdowns()
            self.display_all_records()

    def delete_instructor(self, instructor):
        """
        **Sphinx-style documentation** 
        Deletes the instructor record from the database after user confirmation.

        :param instructor: The instructor record to delete.
        :type instructor: tuple
        :return: None
        """
        reply = QMessageBox.question(self, 'Confirm Delete',
                                     f"Are you sure you want to delete instructor {instructor[1]}?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            delete_instructor_from_db(instructor[4])
            QMessageBox.information(self, "Success", "Instructor deleted successfully.")
            self.update_dropdowns()
            self.display_all_records()

    def edit_course(self, course):
        """
        **Sphinx-style documentation**
        Opens the edit dialog for a course and updates the database.

        :param course: The course record to edit.
        :type course: tuple
        :return: None
        """
        dialog = EditDialog("Course", course)
        if dialog.exec_():
            new_course_id = dialog.get_course_id()  # Get new course ID
            new_course_name = dialog.get_course_name()  # Get new course name

            if not new_course_name or not new_course_id:
                QMessageBox.warning(self, "Input Error", "Please provide valid course data.")
                return
            
            if update_course_in_db(course[1], new_course_id, new_course_name):
                QMessageBox.information(self, "Success", "Course updated successfully.")
                self.update_dropdowns()
                self.display_all_records()
            else:
                QMessageBox.warning(self, "Error", "Could not update course. Course ID may already be in use.")


    def delete_course(self, course):
        """
        **Sphinx-style documentation** 
        Deletes the course record from the database after user confirmation.

        :param course: The course record to delete.
        :type course: tuple
        :return: None
        """
        reply = QMessageBox.question(self, 'Confirm Delete',
                                     f"Are you sure you want to delete course {course[2]}?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            delete_course_from_db(course[1])
            QMessageBox.information(self, "Success", "Course deleted successfully.")
            self.update_dropdowns()
            self.display_all_records()

    def search_records(self):
        """
        **docstring**
        Searches for students, instructors, or courses based on the input query.

        Compares the query with student names, student IDs, instructor names, instructor IDs, and course names to filter and display matching records in the table widget.

        """
        query = self.search_input.text().lower()
        self.table_widget.setRowCount(0)

        students = fetch_all_students()
        instructors = fetch_all_instructors()
        courses = fetch_all_courses()

        for student in students:
            if query in student[1].lower() or query in student[4].lower():
                row_position = self.table_widget.rowCount()
                self.table_widget.insertRow(row_position)
                self.table_widget.setItem(row_position, 0, QTableWidgetItem(student[1]))
                self.table_widget.setItem(row_position, 1, QTableWidgetItem(student[4]))
                self.table_widget.setItem(row_position, 2, QTableWidgetItem(str(student[2])))
                self.table_widget.setItem(row_position, 3, QTableWidgetItem(student[3]))
                self.table_widget.setItem(row_position, 4, QTableWidgetItem("Student"))
                self.table_widget.setCellWidget(row_position, 5, self.create_edit_button("Student", student))
                self.table_widget.setCellWidget(row_position, 6, self.create_delete_button("Student", student))

        for instructor in instructors:
            if query in instructor[1].lower() or query in instructor[4].lower():
                row_position = self.table_widget.rowCount()
                self.table_widget.insertRow(row_position)
                self.table_widget.setItem(row_position, 0, QTableWidgetItem(instructor[1]))
                self.table_widget.setItem(row_position, 1, QTableWidgetItem(instructor[4]))
                self.table_widget.setItem(row_position, 2, QTableWidgetItem(str(instructor[2])))
                self.table_widget.setItem(row_position, 3, QTableWidgetItem(instructor[3]))
                self.table_widget.setItem(row_position, 4, QTableWidgetItem("Instructor"))
                self.table_widget.setCellWidget(row_position, 5, self.create_edit_button("Instructor", instructor))
                self.table_widget.setCellWidget(row_position, 6, self.create_delete_button("Instructor", instructor))

        for course in courses:
            if query in course[2].lower() or query in course[1].lower():
                row_position = self.table_widget.rowCount()
                self.table_widget.insertRow(row_position)
                self.table_widget.setItem(row_position, 0, QTableWidgetItem(course[2]))
                self.table_widget.setItem(row_position, 1, QTableWidgetItem(course[1]))
                self.table_widget.setItem(row_position, 2, QTableWidgetItem("N/A"))
                instructor_name = "None" if course[3] is None else f"Instructor ID: {course[3]}"
                self.table_widget.setItem(row_position, 3, QTableWidgetItem(instructor_name))
                self.table_widget.setItem(row_position, 4, QTableWidgetItem("Course"))
                self.table_widget.setCellWidget(row_position, 5, self.create_edit_button("Course", course))
                self.table_widget.setCellWidget(row_position, 6, self.create_delete_button("Course", course))
class EditDialog(QDialog):
    """
    A dialog for editing student, instructor, or course records.

    This dialog presents input fields for updating student, instructor, or course data.
    **docsting**
    """
    def __init__(self, record_type, record):
        """
        **sphinx**
        Initializes the edit dialog with the record type and its data.

        :param record_type: Specifies whether the record is a Student, Instructor, or Course.
        :type record_type: str
        :param record: The data of the record being edited.
        :type record: tuple
        """
        super().__init__()
        self.record_type = record_type
        self.record = record
        self.setWindowTitle(f"Edit {record_type}")
        self.setWindowIcon(QIcon()) 

        self.layout = QGridLayout(self)

        if record_type in ["Student", "Instructor"]:
            self.id_input = QLineEdit()
            self.name_input = QLineEdit()
            self.age_input = QLineEdit()
            self.email_input = QLineEdit()

            self.id_input.setText(record[4])
            self.name_input.setText(record[1])
            self.age_input.setText(str(record[2]))
            self.email_input.setText(record[3])

            self.layout.addWidget(QLabel("ID:"), 0, 0)
            self.layout.addWidget(self.id_input, 0, 1)
            self.layout.addWidget(QLabel("Name:"), 1, 0)
            self.layout.addWidget(self.name_input, 1, 1)
            self.layout.addWidget(QLabel("Age:"), 2, 0)
            self.layout.addWidget(self.age_input, 2, 1)
            self.layout.addWidget(QLabel("Email:"), 3, 0)
            self.layout.addWidget(self.email_input, 3, 1)

        
        elif record_type == "Course":
            self.course_id_input = QLineEdit()
            self.course_name_input = QLineEdit()

            self.course_id_input.setText(record[1])  
            self.course_name_input.setText(record[2])

            self.layout.addWidget(QLabel("Course ID:"), 0, 0)
            self.layout.addWidget(self.course_id_input, 0, 1)
            self.layout.addWidget(QLabel("Course Name:"), 1, 0)
            self.layout.addWidget(self.course_name_input, 1, 1)

        self.ok_button = QPushButton("OK")
        self.cancel_button = QPushButton("Cancel")
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)

        self.layout.addLayout(button_layout, 4, 0, 1, 2)

    def get_inputs(self):
        """
        **Sphinx-style documentation**
        Retrieves the inputs entered in the dialog.

        :return: a tuple having name, age, and email for students or instructors, or the course name for courses.
        :rtype: tuple[str, str, str] or str
        """
        if self.record_type in ["Student", "Instructor"]:
            return self.id_input.text().strip(), self.name_input.text().strip(), self.age_input.text().strip(), self.email_input.text().strip()
        elif self.record_type == "Course":
            return self.course_id_input.text().strip(), self.course_name_input.text().strip()
        
    def get_course_id(self):
        """
        Retrieves the course ID entered in the dialog.

        :return: The course ID.
        :rtype: str
        """
        return self.course_id_input.text().strip()
    
    def get_course_name(self):
        """
        **regular docstring** 
        Retrieves the course name entered in the dialog.

        :return: The course name.
        :rtype: str
        """
        return self.course_name_input.text().strip()

if __name__ == '__main__':
    init_db()
    app = QApplication(sys.argv)
    window = SchoolManagementSystem()
    window.show()
    sys.exit(app.exec_())
