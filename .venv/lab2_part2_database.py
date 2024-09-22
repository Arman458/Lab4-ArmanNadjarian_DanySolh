import sqlite3
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QComboBox, QMessageBox, QTableWidget, QTableWidgetItem, QFileDialog

def connect_db():
    return sqlite3.connect('school_management.db')

def create_tables():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS students (
                        student_id TEXT PRIMARY KEY,
                        name TEXT NOT NULL,
                        age INTEGER NOT NULL CHECK(age >= 0),
                        email TEXT NOT NULL
                    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS instructors (
                        instructor_id TEXT PRIMARY KEY,
                        name TEXT NOT NULL,
                        age INTEGER NOT NULL CHECK(age >= 0),
                        email TEXT NOT NULL
                    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS courses (
                        course_id TEXT PRIMARY KEY,
                        course_name TEXT NOT NULL,
                        instructor_id TEXT,
                        FOREIGN KEY(instructor_id) REFERENCES instructors(instructor_id)
                    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS registrations (
                        student_id TEXT,
                        course_id TEXT,
                        FOREIGN KEY(student_id) REFERENCES students(student_id),
                        FOREIGN KEY(course_id) REFERENCES courses(course_id)
                    )''')
    conn.commit()
    conn.close()

create_tables()

def add_student_to_db(student_id, name, age, email):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO students (student_id, name, age, email) VALUES (?, ?, ?, ?)', (student_id, name, age, email))
    conn.commit()
    conn.close()

def add_instructor_to_db(instructor_id, name, age, email):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO instructors (instructor_id, name, age, email) VALUES (?, ?, ?, ?)', (instructor_id, name, age, email))
    conn.commit()
    conn.close()

def add_course_to_db(course_id, course_name, instructor_id=None):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO courses (course_id, course_name, instructor_id) VALUES (?, ?, ?)', (course_id, course_name, instructor_id))
    conn.commit()
    conn.close()

def register_student_for_course(student_id, course_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO registrations (student_id, course_id) VALUES (?, ?)', (student_id, course_id))
    conn.commit()
    conn.close()

def assign_instructor_to_course(course_id, instructor_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE courses SET instructor_id = ? WHERE course_id = ?', (instructor_id, course_id))
    conn.commit()
    conn.close()

def get_all_students():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT student_id, name FROM students')
    students = cursor.fetchall()
    conn.close()
    return students

def get_all_instructors():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT instructor_id, name FROM instructors')
    instructors = cursor.fetchall()
    conn.close()
    return instructors

def get_all_courses():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT course_id, course_name FROM courses')
    courses = cursor.fetchall()
    conn.close()
    return courses

def get_all_records():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT student_id, name, age, email FROM students')
    students = cursor.fetchall()
    cursor.execute('SELECT instructor_id, name, age, email FROM instructors')
    instructors = cursor.fetchall()
    cursor.execute('''SELECT c.course_id, c.course_name, i.name AS instructor_name, GROUP_CONCAT(s.name, ', ') AS student_names
                      FROM courses c
                      LEFT JOIN registrations r ON c.course_id = r.course_id
                      LEFT JOIN students s ON r.student_id = s.student_id
                      LEFT JOIN instructors i ON c.instructor_id = i.instructor_id
                      GROUP BY c.course_id''')
    courses = cursor.fetchall()
    conn.close()
    return students, instructors, courses

class SchoolManagementSystem(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("School Management System")
        self.setGeometry(100, 100, 800, 600)
        layout = QVBoxLayout()

        self.student_name_label = QLabel("Student Name:")
        self.student_name_input = QLineEdit()
        self.student_age_label = QLabel("Student Age:")
        self.student_age_input = QLineEdit()
        self.student_email_label = QLabel("Student Email:")
        self.student_email_input = QLineEdit()
        self.student_id_label = QLabel("Student ID:")
        self.student_id_input = QLineEdit()
        self.add_student_btn = QPushButton("Add Student")
        self.add_student_btn.clicked.connect(self.add_student)

        self.instructor_name_label = QLabel("Instructor Name:")
        self.instructor_name_input = QLineEdit()
        self.instructor_age_label = QLabel("Instructor Age:")
        self.instructor_age_input = QLineEdit()
        self.instructor_email_label = QLabel("Instructor Email:")
        self.instructor_email_input = QLineEdit()
        self.instructor_id_label = QLabel("Instructor ID:")
        self.instructor_id_input = QLineEdit()
        self.add_instructor_btn = QPushButton("Add Instructor")
        self.add_instructor_btn.clicked.connect(self.add_instructor)

        self.course_name_label = QLabel("Course Name:")
        self.course_name_input = QLineEdit()
        self.course_id_label = QLabel("Course ID:")
        self.course_id_input = QLineEdit()
        self.add_course_btn = QPushButton("Add Course")
        self.add_course_btn.clicked.connect(self.add_course)

        self.course_dropdown = QComboBox()
        self.student_dropdown = QComboBox()
        self.instructor_dropdown = QComboBox()
        self.update_dropdowns()

        self.register_student_btn = QPushButton("Register Student for Course")
        self.assign_instructor_btn = QPushButton("Assign Instructor to Course")
        self.register_student_btn.clicked.connect(self.register_student)
        self.assign_instructor_btn.clicked.connect(self.assign_instructor)

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(5)
        self.table_widget.setHorizontalHeaderLabels(["Name", "ID", "Age", "Email", "Type"])

        self.display_records_btn = QPushButton("Display All Records")
        self.display_records_btn.clicked.connect(self.display_all_records)

        self.backup_btn = QPushButton("Backup Database")
        self.backup_btn.clicked.connect(self.backup_database)

        layout.addWidget(self.student_name_label)
        layout.addWidget(self.student_name_input)
        layout.addWidget(self.student_age_label)
        layout.addWidget(self.student_age_input)
        layout.addWidget(self.student_email_label)
        layout.addWidget(self.student_email_input)
        layout.addWidget(self.student_id_label)
        layout.addWidget(self.student_id_input)
        layout.addWidget(self.add_student_btn)

        layout.addWidget(self.instructor_name_label)
        layout.addWidget(self.instructor_name_input)
        layout.addWidget(self.instructor_age_label)
        layout.addWidget(self.instructor_age_input)
        layout.addWidget(self.instructor_email_label)
        layout.addWidget(self.instructor_email_input)
        layout.addWidget(self.instructor_id_label)
        layout.addWidget(self.instructor_id_input)
        layout.addWidget(self.add_instructor_btn)

        layout.addWidget(self.course_name_label)
        layout.addWidget(self.course_name_input)
        layout.addWidget(self.course_id_label)
        layout.addWidget(self.course_id_input)
        layout.addWidget(self.add_course_btn)

        layout.addWidget(self.course_dropdown)
        layout.addWidget(self.student_dropdown)
        layout.addWidget(self.register_student_btn)

        layout.addWidget(self.instructor_dropdown)
        layout.addWidget(self.assign_instructor_btn)

        layout.addWidget(self.table_widget)
        layout.addWidget(self.display_records_btn)

        layout.addWidget(self.backup_btn)

        self.setLayout(layout)

    def update_dropdowns(self):
        self.course_dropdown.clear()
        self.student_dropdown.clear()
        self.instructor_dropdown.clear()
        self.course_dropdown.addItem("Select Course")
        self.student_dropdown.addItem("Select Student")
        self.instructor_dropdown.addItem("Select Instructor")
        for course in get_all_courses():
            self.course_dropdown.addItem(course[1])
        for student in get_all_students():
            self.student_dropdown.addItem(student[1])
        for instructor in get_all_instructors():
            self.instructor_dropdown.addItem(instructor[1])

    def add_student(self):
        name = self.student_name_input.text().strip()
        age = self.student_age_input.text().strip()
        email = self.student_email_input.text().strip()
        student_id = self.student_id_input.text().strip()

        if not name or not student_id or not email or not age:
            QMessageBox.warning(self, "Input Error", "All fields must be filled.")
            return

        try:
            age = int(age)
            if age < 0:
                raise ValueError("Age cannot be negative.")
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter a valid non-negative integer for age.")
            return

        if '@' not in email or '.' not in email:
            QMessageBox.warning(self, "Input Error", "Please enter a valid email address.")
            return

        add_student_to_db(student_id, name, age, email)
        self.update_dropdowns()
        QMessageBox.information(self, "Success", f"Student {name} added successfully!")

    def add_instructor(self):
        name = self.instructor_name_input.text().strip()
        age = self.instructor_age_input.text().strip()
        email = self.instructor_email_input.text().strip()
        instructor_id = self.instructor_id_input.text().strip()

        if not name or not instructor_id or not email or not age:
            QMessageBox.warning(self, "Input Error", "All fields must be filled.")
            return

        try:
            age = int(age)
            if age < 0:
                raise ValueError("Age cannot be negative.")
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter a valid non-negative integer for age.")
            return

        if '@' not in email or '.' not in email:
            QMessageBox.warning(self, "Input Error", "Please enter a valid email address.")
            return

        add_instructor_to_db(instructor_id, name, age, email)
        self.update_dropdowns()
        QMessageBox.information(self, "Success", f"Instructor {name} added successfully!")

    def add_course(self):
        course_name = self.course_name_input.text().strip()
        course_id = self.course_id_input.text().strip()

        if not course_name or not course_id:
            QMessageBox.warning(self, "Input Error", "Both course name and course ID must be filled.")
            return

        add_course_to_db(course_id, course_name)
        self.update_dropdowns()
        QMessageBox.information(self, "Success", f"Course {course_name} added successfully!")

    def register_student(self):
        selected_student = self.student_dropdown.currentText()
        selected_course = self.course_dropdown.currentText()

        if selected_student == "Select Student" or selected_course == "Select Course":
            QMessageBox.warning(self, "Input Error", "Please select both a student and a course.")
            return

        student = next(s for s in get_all_students() if s[1] == selected_student)
        course = next(c for c in get_all_courses() if c[1] == selected_course)
        register_student_for_course(student[0], course[0])
        QMessageBox.information(self, "Success", f"Student {selected_student} registered for {selected_course}!")

    def assign_instructor(self):
        selected_instructor = self.instructor_dropdown.currentText()
        selected_course = self.course_dropdown.currentText()

        if selected_instructor == "Select Instructor" or selected_course == "Select Course":
            QMessageBox.warning(self, "Input Error", "Please select both an instructor and a course.")
            return

        instructor = next(i for i in get_all_instructors() if i[1] == selected_instructor)
        course = next(c for c in get_all_courses() if c[1] == selected_course)
        assign_instructor_to_course(course[0], instructor[0])
        QMessageBox.information(self, "Success", f"Instructor {selected_instructor} assigned to {selected_course}!")

    def display_all_records(self):
        self.table_widget.setRowCount(0)
        students, instructors, courses = get_all_records()

        for student in students:
            row_position = self.table_widget.rowCount()
            self.table_widget.insertRow(row_position)
            self.table_widget.setItem(row_position, 0, QTableWidgetItem(student[1]))
            self.table_widget.setItem(row_position, 1, QTableWidgetItem(student[0]))
            self.table_widget.setItem(row_position, 2, QTableWidgetItem(str(student[2])))
            self.table_widget.setItem(row_position, 3, QTableWidgetItem(student[3]))
            self.table_widget.setItem(row_position, 4, QTableWidgetItem("Student"))

        for instructor in instructors:
            row_position = self.table_widget.rowCount()
            self.table_widget.insertRow(row_position)
            self.table_widget.setItem(row_position, 0, QTableWidgetItem(instructor[1]))
            self.table_widget.setItem(row_position, 1, QTableWidgetItem(instructor[0]))
            self.table_widget.setItem(row_position, 2, QTableWidgetItem(str(instructor[2])))
            self.table_widget.setItem(row_position, 3, QTableWidgetItem(instructor[3]))
            self.table_widget.setItem(row_position, 4, QTableWidgetItem("Instructor"))

        for course in courses:
            row_position = self.table_widget.rowCount()
            self.table_widget.insertRow(row_position)
            self.table_widget.setItem(row_position, 0, QTableWidgetItem(course[1]))
            self.table_widget.setItem(row_position, 1, QTableWidgetItem(course[0]))
            self.table_widget.setItem(row_position, 2, QTableWidgetItem(course[3]))
            self.table_widget.setItem(row_position, 3, QTableWidgetItem(course[2] if course[2] else "None"))
            self.table_widget.setItem(row_position, 4, QTableWidgetItem("Course"))

    def backup_database(self):
        options = QFileDialog.Options()
        backup_file, _ = QFileDialog.getSaveFileName(self, "Save Database Backup", "", "SQLite Database Files (*.db);;All Files (*)", options=options)
        if backup_file:
            try:
                conn = connect_db()
                backup_conn = sqlite3.connect(backup_file)
                with backup_conn:
                    conn.backup(backup_conn)
                backup_conn.close()
                conn.close()
                QMessageBox.information(self, "Success", f"Database backed up to {backup_file} successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred while backing up the database: {str(e)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SchoolManagementSystem()
    window.show()
    sys.exit(app.exec_())
