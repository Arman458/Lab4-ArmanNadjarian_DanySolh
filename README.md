# Lab4-ArmanNadjarian_DanySolh
A project combining Tkinter and PyQt documented implementations

School Management System
Overview

This project is a School Management System implemented using Python, with two separate graphical user interfaces (GUIs):

    Tkinter: Developed by Dany Sloh.
    PyQt5: Developed by Arman Nadjarian.

Each interface allows users to:

    Add and manage students, instructors, and courses.
    Register students for courses and assign instructors to courses.
    Save and load data using separate SQLite databases.

Requirements

Make sure that both Tkinter and PyQt5 libraries are installed, along with SQLite3, which comes pre-installed with Python.
Running the Tkinter Interface

The Tkinter interfac provides a GUI for managing students, instructors, and courses using its own SQLite database.
Features of the Tkinter Interface:

    Add Student: Input student details (name, age, email) and add them to the database.
    Add Instructor: Similarly, input instructor details and add them.
    Add Course: Provide the course ID and name, then add the course.
    Register Student for Course: Select a student and a course from dropdown lists to register the student.
    Assign Instructor to Course: Choose an instructor and a course to assign them.
    View and Search Records: Display all records (students, instructors, courses) in a table, and search through the records using filters.


The Tkinter interface uses an SQLite database which stores information about students, instructors, and courses in separate tables.


The PyQt5 interfaceoffers a similar set of functionalities using a different GUI framework.
Features of the PyQt5 Interface:

    Add Student: Fill in student details using the form and submit to save them to the database.
    Add Instructor: Similarly, fill in instructor details and submit to save.
    Add Course: Add courses by providing the course ID and name.
    Register Student for Course: Register students for courses using dropdown menus to select students and courses.
    Assign Instructor to Course: Assign instructors to courses using dropdown menus.
    View and Search Records: Display and search through all students, instructors, and courses.

Database for PyQt:

The PyQt5 interface uses its own SQLite database to store students, instructors, and courses in separate tables and tracks student registrations for courses.
