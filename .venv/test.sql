BEGIN TRANSACTION;
CREATE TABLE courses (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        course_id TEXT NOT NULL UNIQUE,
                        course_name TEXT NOT NULL,
                        instructor_id INTEGER,
                        FOREIGN KEY(instructor_id) REFERENCES instructors(id)
                    );
CREATE TABLE instructors (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        age INTEGER NOT NULL CHECK(age >= 0),
                        email TEXT NOT NULL UNIQUE
                    );
CREATE TABLE registrations (
                        student_id INTEGER,
                        course_id INTEGER,
                        PRIMARY KEY (student_id, course_id),
                        FOREIGN KEY(student_id) REFERENCES students(id),
                        FOREIGN KEY(course_id) REFERENCES courses(id)
                    );
CREATE TABLE students (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        age INTEGER NOT NULL CHECK(age >= 0),
                        email TEXT NOT NULL UNIQUE
                    );
INSERT INTO "students" VALUES(1,'x',1,'x@gmail.com');
INSERT INTO "students" VALUES(2,'xsdsw',121,'X@gmail.com');
DELETE FROM "sqlite_sequence";
INSERT INTO "sqlite_sequence" VALUES('students',2);
COMMIT;
