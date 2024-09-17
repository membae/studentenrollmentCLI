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
        print("8. See the list of courses a student is enrolled in")
        print("9. Exit")
        
        choice = input("Enter your choice (1-8): ")
        
        if choice == '1':
            from add import add_student
            add_student()
        elif choice == '2':
            from add import add_instructor
            add_instructor()
        elif choice == '3':
            from add import add_course
            add_course()
        elif choice == '4':
            from add import enroll_student
            enroll_student()
        elif choice == '5':
            from list import list_students
            list_students()
        elif choice == '6':
            from list import list_courses
            list_courses()
        elif choice == '7':
            from list import list_instructors
            list_instructors()
        elif choice == '8':
            from list import list_student_courses
            list_student_courses()
        elif choice == '9':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 8.")

if __name__ == "__main__":
    main()
