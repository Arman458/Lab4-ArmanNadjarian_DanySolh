import sys
import json
import csv
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QComboBox, QMessageBox, QTableWidget, QTableWidgetItem, QFileDialog

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



def is_valid_email(email):
    return "@" in email and "." in email

def is_valid_age(age):
    return age.isdigit() and int(age) >= 0

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
                for s_name in c.get("students", []):
                    student = next((s for s in students if s.name == s_name), None)
                    if student:
                        course.add_student(student)
                courses.append(course)
    except FileNotFoundError:
        pass


def export_to_csv():
    path, _ = QFileDialog.getSaveFileName(None, "Export CSV", "", "CSV Files (*.csv)")
    if path:
        with open(path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Type", "Name", "ID", "Age", "Email"])
            for student in students:
                writer.writerow(["Student", student.name, student.student_id, student.age, student._email])
            for instructor in instructors:
                writer.writerow(["Instructor", instructor.name, instructor.instructor_id, instructor.age, instructor._email])
            for course in courses:
                writer.writerow(["Course", course.course_name, course.course_id, "N/A", course.instructor.name if course.instructor else "None"])
        QMessageBox.information(None, "Success", "Data exported successfully!")



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
        self.export_btn = QPushButton("Export to CSV")
        self.register_student_btn.clicked.connect(self.register_student)
        self.assign_instructor_btn.clicked.connect(self.assign_instructor)
        self.export_btn.clicked.connect(export_to_csv)

        
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(5)
        self.table_widget.setHorizontalHeaderLabels(["Name", "ID", "Age", "Email", "Type"])

        
        self.display_records_btn = QPushButton("Display All Records")
        self.display_records_btn.clicked.connect(self.display_all_records)
        self.edit_record_btn = QPushButton("Edit Selected Record")
        self.edit_record_btn.clicked.connect(self.edit_record)
        self.delete_record_btn = QPushButton("Delete Selected Record")
        self.delete_record_btn.clicked.connect(self.delete_record)

       
        self.search_label = QLabel("Search by Name/ID/Course:")
        self.search_input = QLineEdit()
        self.search_btn = QPushButton("Search")
        self.search_btn.clicked.connect(self.search_records)

       
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

        layout.addWidget(self.student_dropdown)
        layout.addWidget(self.course_dropdown)
        layout.addWidget(self.register_student_btn)

        layout.addWidget(self.instructor_dropdown)
        layout.addWidget(self.assign_instructor_btn)

        layout.addWidget(self.table_widget)
        layout.addWidget(self.display_records_btn)
        layout.addWidget(self.edit_record_btn)
        layout.addWidget(self.delete_record_btn)
        layout.addWidget(self.export_btn)

        layout.addWidget(self.search_label)
        layout.addWidget(self.search_input)
        layout.addWidget(self.search_btn)

        self.setLayout(layout)

    def update_dropdowns(self):
        self.course_dropdown.clear()
        self.student_dropdown.clear()
        self.instructor_dropdown.clear()

        self.course_dropdown.addItem("Select Course")
        self.student_dropdown.addItem("Select Student")
        self.instructor_dropdown.addItem("Select Instructor")

        for course in courses:
            self.course_dropdown.addItem(course.course_name)
        for student in students:
            self.student_dropdown.addItem(student.name)
        for instructor in instructors:
            self.instructor_dropdown.addItem(instructor.name)

    def add_student(self):
        name = self.student_name_input.text()
        age = self.student_age_input.text()
        email = self.student_email_input.text()
        student_id = self.student_id_input.text()

        if not name or not is_valid_age(age) or not is_valid_email(email):
            QMessageBox.warning(self, "Input Error", "Invalid input! Make sure all fields are filled correctly.")
            return

        student = Student(name, int(age), email, student_id)
        students.append(student)
        self.update_dropdowns()
        self.clear_student_form()
        QMessageBox.information(self, "Success", f"Student {name} added successfully!")
        save_data()

    def add_instructor(self):
        name = self.instructor_name_input.text()
        age = self.instructor_age_input.text()
        email = self.instructor_email_input.text()
        instructor_id = self.instructor_id_input.text()

        if not name or not is_valid_age(age) or not is_valid_email(email):
            QMessageBox.warning(self, "Input Error", "Invalid input! Make sure all fields are filled correctly.")
            return

        instructor = Instructor(name, int(age), email, instructor_id)
        instructors.append(instructor)
        self.update_dropdowns()
        self.clear_instructor_form()
        QMessageBox.information(self, "Success", f"Instructor {name} added successfully!")
        save_data()

    def add_course(self):
        course_name = self.course_name_input.text()
        course_id = self.course_id_input.text()

        if not course_name or not course_id:
            QMessageBox.warning(self, "Input Error", "Invalid input! Make sure all fields are filled.")
            return

        course = Course(course_id, course_name)
        courses.append(course)
        self.update_dropdowns()
        self.clear_course_form()
        QMessageBox.information(self, "Success", f"Course {course_name} added successfully!")
        save_data()

    def register_student(self):
        selected_student = self.student_dropdown.currentText()
        selected_course = self.course_dropdown.currentText()

        if selected_student == "Select Student" or selected_course == "Select Course":
            QMessageBox.warning(self, "Input Error", "Please select both a student and a course.")
            return

        for student in students:
            if student.name == selected_student:
                for course in courses:
                    if course.course_name == selected_course:
                        course.add_student(student)
                        student.register_course(course)
                        QMessageBox.information(self, "Success", f"Student {student.name} registered for {course.course_name}!")
                        save_data()
                        return

    def assign_instructor(self):
        selected_instructor = self.instructor_dropdown.currentText()
        selected_course = self.course_dropdown.currentText()

        if selected_instructor == "Select Instructor" or selected_course == "Select Course":
            QMessageBox.warning(self, "Input Error", "Please select both an instructor and a course.")
            return

        for instructor in instructors:
            if instructor.name == selected_instructor:
                for course in courses:
                    if course.course_name == selected_course:
                        course.instructor = instructor
                        instructor.assign_course(course)
                        QMessageBox.information(self, "Success", f"Instructor {instructor.name} assigned to {course.course_name}!")
                        save_data()
                        return

    

    def display_all_records(self):
        
        self.table_widget.setRowCount(0)

        
        for student in students:
            row_position = self.table_widget.rowCount()
            self.table_widget.insertRow(row_position)
            self.table_widget.setItem(row_position, 0, QTableWidgetItem(student.name))
            self.table_widget.setItem(row_position, 1, QTableWidgetItem(student.student_id))
            self.table_widget.setItem(row_position, 2, QTableWidgetItem(str(student.age)))
            self.table_widget.setItem(row_position, 3, QTableWidgetItem(student._email))
            self.table_widget.setItem(row_position, 4, QTableWidgetItem("Student"))

        
        for instructor in instructors:
            row_position = self.table_widget.rowCount()
            self.table_widget.insertRow(row_position)
            self.table_widget.setItem(row_position, 0, QTableWidgetItem(instructor.name))
            self.table_widget.setItem(row_position, 1, QTableWidgetItem(instructor.instructor_id))
            self.table_widget.setItem(row_position, 2, QTableWidgetItem(str(instructor.age)))
            self.table_widget.setItem(row_position, 3, QTableWidgetItem(instructor._email))
            self.table_widget.setItem(row_position, 4, QTableWidgetItem("Instructor"))

        
        for course in courses:
            row_position = self.table_widget.rowCount()

            
            enrolled_students = ', '.join([student.name for student in course.enrolled_students]) or "None"
        
            instructor_name = course.instructor.name if course.instructor else "None"

          
            self.table_widget.insertRow(row_position)
            self.table_widget.setItem(row_position, 0, QTableWidgetItem(course.course_name))
            self.table_widget.setItem(row_position, 1, QTableWidgetItem(course.course_id))
            self.table_widget.setItem(row_position, 2, QTableWidgetItem("N/A"))  
            self.table_widget.setItem(row_position, 3, QTableWidgetItem(instructor_name))
            self.table_widget.setItem(row_position, 4, QTableWidgetItem("Course"))

           
            row_position = self.table_widget.rowCount()
            self.table_widget.insertRow(row_position)
            self.table_widget.setItem(row_position, 0, QTableWidgetItem(f"Enrolled Students: {enrolled_students}"))
            self.table_widget.setItem(row_position, 1, QTableWidgetItem(""))  
            self.table_widget.setItem(row_position, 2, QTableWidgetItem("")) 
            self.table_widget.setItem(row_position, 3, QTableWidgetItem(""))  
            self.table_widget.setItem(row_position, 4, QTableWidgetItem(""))  


    def edit_record(self):
        selected_item = self.table_widget.currentRow()
        if selected_item != -1:
            record_type = self.table_widget.item(selected_item, 4).text()

            if record_type == "Student":
                student_name = self.table_widget.item(selected_item, 0).text()
                self.student_name_input.setText(student_name)
                for student in students:
                    if student.name == student_name:
                        students.remove(student)
                        break
            elif record_type == "Instructor":
                instructor_name = self.table_widget.item(selected_item, 0).text()
                self.instructor_name_input.setText(instructor_name)
                for instructor in instructors:
                    if instructor.name == instructor_name:
                        instructors.remove(instructor)
                        break
            elif record_type == "Course":
                course_name = self.table_widget.item(selected_item, 0).text()
                self.course_name_input.setText(course_name)
                for course in courses:
                    if course.course_name == course_name:
                        courses.remove(course)
                        break
            QMessageBox.information(self, "Info", "You can edit the details now and re-add the record.")

    def delete_record(self):
        selected_item = self.table_widget.currentRow()
        if selected_item != -1:
            record_type = self.table_widget.item(selected_item, 4).text()

            if record_type == "Student":
                student_name = self.table_widget.item(selected_item, 0).text()
                for student in students:
                    if student.name == student_name:
                        students.remove(student)
                        break
            elif record_type == "Instructor":
                instructor_name = self.table_widget.item(selected_item, 0).text()
                for instructor in instructors:
                    if instructor.name == instructor_name:
                        instructors.remove(instructor)
                        break
            elif record_type == "Course":
                course_name = self.table_widget.item(selected_item, 0).text()
                for course in courses:
                    if course.course_name == course_name:
                        courses.remove(course)
                        break
            self.table_widget.removeRow(selected_item)
            save_data()
            QMessageBox.information(self, "Success", "Record deleted successfully!")

    def search_records(self):
        query = self.search_input.text().lower()
        self.table_widget.setRowCount(0)

        for student in students:
            if query in student.name.lower() or query in student.student_id:
                row_position = self.table_widget.rowCount()
                self.table_widget.insertRow(row_position)
                self.table_widget.setItem(row_position, 0, QTableWidgetItem(student.name))
                self.table_widget.setItem(row_position, 1, QTableWidgetItem(student.student_id))
                self.table_widget.setItem(row_position, 2, QTableWidgetItem(str(student.age)))
                self.table_widget.setItem(row_position, 3, QTableWidgetItem(student._email))
                self.table_widget.setItem(row_position, 4, QTableWidgetItem("Student"))

        for instructor in instructors:
            if query in instructor.name.lower() or query in instructor.instructor_id:
                row_position = self.table_widget.rowCount()
                self.table_widget.insertRow(row_position)
                self.table_widget.setItem(row_position, 0, QTableWidgetItem(instructor.name))
                self.table_widget.setItem(row_position, 1, QTableWidgetItem(instructor.instructor_id))
                self.table_widget.setItem(row_position, 2, QTableWidgetItem(str(instructor.age)))
                self.table_widget.setItem(row_position, 3, QTableWidgetItem(instructor._email))
                self.table_widget.setItem(row_position, 4, QTableWidgetItem("Instructor"))

        for course in courses:
            if query in course.course_name.lower() or query in course.course_id:
                row_position = self.table_widget.rowCount()
                self.table_widget.insertRow(row_position)
                self.table_widget.setItem(row_position, 0, QTableWidgetItem(course.course_name))
                self.table_widget.setItem(row_position, 1, QTableWidgetItem(course.course_id))
                self.table_widget.setItem(row_position, 2, QTableWidgetItem("N/A"))
                self.table_widget.setItem(row_position, 3, QTableWidgetItem(course.instructor.name if course.instructor else "None"))
                self.table_widget.setItem(row_position, 4, QTableWidgetItem("Course"))

    def clear_student_form(self):
        self.student_name_input.clear()
        self.student_age_input.clear()
        self.student_email_input.clear()
        self.student_id_input.clear()

    def clear_instructor_form(self):
        self.instructor_name_input.clear()
        self.instructor_age_input.clear()
        self.instructor_email_input.clear()
        self.instructor_id_input.clear()

    def clear_course_form(self):
        self.course_name_input.clear()
        self.course_id_input.clear()

if __name__ == '__main__':
    students = []
    instructors = []
    courses = []
    load_data()

    app = QApplication(sys.argv)
    window = SchoolManagementSystem()
    window.show()
    sys.exit(app.exec_())
