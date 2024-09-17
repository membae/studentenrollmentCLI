import sqlite3

# Database setup
def initialize_db():
    conn = sqlite3.connect('student_enrollment.db')
    cursor = conn.cursor()

    cursor.execute('DROP TABLE IF EXISTS courses')
    
    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS instructors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department TEXT NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            instructor_id INTEGER,
            FOREIGN KEY (instructor_id) REFERENCES instructors(id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS enrollments (
            student_id INTEGER,
            course_id INTEGER,
            PRIMARY KEY (student_id, course_id),
            FOREIGN KEY (student_id) REFERENCES students(id),
            FOREIGN KEY (course_id) REFERENCES courses(id)
        )
    ''')
    
    conn.commit()
    conn.close()

# Add a new student
def add_student():
    name = input("Enter student's name: ")
    email = input("Enter student's email: ")
    
    conn = sqlite3.connect('student_enrollment.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO students (name, email) VALUES (?, ?)
        ''', (name, email))
        conn.commit()
        print(f"Student {name} added successfully!")
    except sqlite3.IntegrityError:
        print("Error: A student with this email already exists.")
    
    conn.close()

# Add a new instructor
def add_instructor():
    name = input("Enter instructor's name: ")
    department = input("Enter instructor's department: ")
    
    conn = sqlite3.connect('student_enrollment.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO instructors (name, department) VALUES (?, ?)
    ''', (name, department))
    
    conn.commit()
    print(f"Instructor {name} added successfully!")
    conn.close()

# Add a new course
def add_course():
    title = input("Enter course title: ")
    description = input("Enter course description: ")
    instructor_id = input("Enter instructor ID for this course: ")

    conn = sqlite3.connect('student_enrollment.db')
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT INTO courses (title, description, instructor_id) VALUES (?, ?, ?)
        ''', (title, description, instructor_id))
        conn.commit()
        print(f"Course {title} added successfully!")
    except sqlite3.IntegrityError:
        print("Error: Instructor ID is invalid.")
    
    conn.close()

# Enroll a student in a course
def enroll_student():
    student_id = int(input("Enter student ID: "))
    course_id = int(input("Enter course ID: "))
    
    conn = sqlite3.connect('student_enrollment.db')
    cursor = conn.cursor()

    # Check if the student exists
    cursor.execute('SELECT id FROM students WHERE id = ?', (student_id,))
    student = cursor.fetchone()
    if not student:
        print("Error: Student ID does not exist.")
        conn.close()
        return
    
    # Check if the course exists
    cursor.execute('SELECT id FROM courses WHERE id = ?', (course_id,))
    course = cursor.fetchone()
    if not course:
        print("Error: Course ID does not exist.")
        conn.close()
        return
    
    # Check if the student is already enrolled in the course
    cursor.execute('''
        SELECT * FROM enrollments WHERE student_id = ? AND course_id = ?
    ''', (student_id, course_id))
    enrollment = cursor.fetchone()
    if enrollment:
        print("Error: Student is already enrolled in this course.")
        conn.close()
        return
    
    # Proceed with enrollment
    try:
        cursor.execute('''
            INSERT INTO enrollments (student_id, course_id) VALUES (?, ?)
        ''', (student_id, course_id))
        conn.commit()
        print("Student enrolled in course successfully!")
    except sqlite3.IntegrityError:
        print("Error: Enrollment already exists.")
    
    conn.close()

# List all students
def list_students():
    conn = sqlite3.connect('student_enrollment.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, name, email FROM students')
    students = cursor.fetchall()
    
    if students:
        print("List of students:")
        for student in students:
            print(f"ID: {student[0]}, Name: {student[1]}, Email: {student[2]}")
    else:
        print("No students found.")
    
    conn.close()

# List all courses
def list_courses():
    conn = sqlite3.connect('student_enrollment.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT courses.id, courses.title, instructors.name 
        FROM courses 
        JOIN instructors ON courses.instructor_id = instructors.id
    ''')
    courses = cursor.fetchall()
    
    if courses:
        print("List of courses:")
        for course in courses:
            print(f"ID: {course[0]}, Title: {course[1]}, Instructor: {course[2]}")
    else:
        print("No courses found.")
    
    conn.close()

# List all instructors
def list_instructors():
    conn = sqlite3.connect('student_enrollment.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, name, department FROM instructors')
    instructors = cursor.fetchall()
    
    if instructors:
        print("List of instructors:")
        for instructor in instructors:
            print(f"ID: {instructor[0]}, Name: {instructor[1]}, Department: {instructor[2]}")
    else:
        print("No instructors found.")
    
    conn.close()

# Main CLI loop
def main():
    initialize_db()
    
    while True:
        print("\nSelect an option:")
        print("1. Add a new student")
        print("2. Add a new instructor")
        print("3. Add a new course")
        print("4. Enroll a student in a course")
        print("5. See a list of all students")
        print("6. See a list of all courses")
        print("7. See a list of all instructors")
        print("8. Exit")
        
        choice = input("Enter your choice (1-8): ")
        
        if choice == '1':
            add_student()
        elif choice == '2':
            add_instructor()
        elif choice == '3':
            add_course()
        elif choice == '4':
            enroll_student()
        elif choice == '5':
            list_students()
        elif choice == '6':
            list_courses()
        elif choice == '7':
            list_instructors()
        elif choice == '8':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 8.")

if __name__ == "__main__":
    main()
