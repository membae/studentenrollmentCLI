import sqlite3
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

