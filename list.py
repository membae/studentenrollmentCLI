import sqlite3
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


def list_student_courses():
    student_id = int(input("Enter student ID: "))
    
    conn = sqlite3.connect('student_enrollment.db')
    cursor = conn.cursor()
    
    # Verify if the student exists
    cursor.execute('SELECT * FROM students WHERE id = ?', (student_id,))
    student = cursor.fetchone()
    if not student:
        print("Error: Student ID does not exist.")
        conn.close()
        return

    cursor.execute('''
        SELECT courses.id, courses.title, instructors.name 
        FROM enrollments 
        JOIN courses ON enrollments.course_id = courses.id
        JOIN instructors ON courses.instructor_id = instructors.id
        WHERE enrollments.student_id = ?
    ''', (student_id,))
    courses = cursor.fetchall()
    
    if courses:
        print(f"Courses for student {student[1]}:")
        for course in courses:
            print(f"Course ID: {course[0]}, Title: {course[1]}, Instructor: {course[2]}")
    else:
        print(f"Student {student[1]} is not enrolled in any courses.")
    
    conn.close()

