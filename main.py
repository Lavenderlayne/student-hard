import sqlite3

DB_NAME = "university.db"

def create_tables():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.executescript("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            major TEXT
        );

        CREATE TABLE IF NOT EXISTS courses (
            course_id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_name TEXT NOT NULL,
            instructor TEXT
        );

        CREATE TABLE IF NOT EXISTS enrollment (
            student_id INTEGER,
            course_id INTEGER,
            PRIMARY KEY (student_id, course_id),
            FOREIGN KEY (student_id) REFERENCES students(id),
            FOREIGN KEY (course_id) REFERENCES courses(course_id)
        );
        """)
        print("✅ Tables created successfully.")

def add_student():
    name = input("Student name: ")
    age = int(input("Age: "))
    major = input("Major: ")
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("INSERT INTO students (name, age, major) VALUES (?, ?, ?)", (name, age, major))
        print("✅ Student added.")

def add_course():
    name = input("Course name: ")
    instructor = input("Instructor: ")
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("INSERT INTO courses (course_name, instructor) VALUES (?, ?)", (name, instructor))
        print("✅ Course added.")

def enroll_student():
    view_students()
    student_id = int(input("Enter student ID: "))
    view_courses()
    course_id = int(input("Enter course ID: "))
    with sqlite3.connect(DB_NAME) as conn:
        try:
            conn.execute("INSERT INTO enrollment (student_id, course_id) VALUES (?, ?)", (student_id, course_id))
            print("✅ Enrolled successfully.")
        except sqlite3.IntegrityError:
            print("⚠️ Student already enrolled in this course.")

def view_students():
    with sqlite3.connect(DB_NAME) as conn:
        rows = conn.execute("SELECT * FROM students").fetchall()
        print("\n🧑 Students:")
        for row in rows:
            print(row)

def view_courses():
    with sqlite3.connect(DB_NAME) as conn:
        rows = conn.execute("SELECT * FROM courses").fetchall()
        print("\n📚 Courses:")
        for row in rows:
            print(row)

def view_students_in_course():
    view_courses()
    course_id = int(input("Enter course ID to list students: "))
    with sqlite3.connect(DB_NAME) as conn:
        rows = conn.execute("""
            SELECT s.id, s.name, s.major FROM students s
            JOIN enrollment e ON s.id = e.student_id
            WHERE e.course_id = ?
        """, (course_id,)).fetchall()
        print(f"\n👥 Students enrolled in course {course_id}:")
        for row in rows:
            print(row)

def main():
    create_tables()
    while True:
        print("\n📘 Menu:")
        print("1. Add Student")
        print("2. Add Course")
        print("3. Enroll Student in Course")
        print("4. View All Students")
        print("5. View All Courses")
        print("6. View Students in a Course")
        print("0. Exit")
        choice = input("Choose an option: ")
        match choice:
            case "1": add_student()
            case "2": add_course()
            case "3": enroll_student()
            case "4": view_students()
            case "5": view_courses()
            case "6": view_students_in_course()
            case "0": break
            case _: print("❌ Invalid choice.")

if __name__ == "__main__":
    main()
