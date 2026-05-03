from app import app, db, Student, Instructor, Course, Enrollment
from datetime import date

with app.app_context():
    db.drop_all()
    db.create_all()

    students = [
        Student(first_name="Clark", last_name="Kent", email="superman@gmail.com", enrollment_date=date(2024, 1, 10)),
        Student(first_name="Bruce", last_name="Wayne", email="batman@gmail.com", enrollment_date=date(2024, 2, 11)),
        Student(first_name="Diana", last_name="Wonder", email="wonderwoman@gmail.com", enrollment_date=date(2024, 3, 12)),
        Student(first_name="John", last_name="Jones", email="manhunter@gmail.com", enrollment_date=date(2024, 4, 13)),
        Student(first_name="Hal", last_name="Jordan", email="greenlantern@gmail.com", enrollment_date=date(2024, 5, 14)),
    ]

    instructors = [
        Instructor(instructor_name="Dr. Doom", department="Math", hire_date=date(2020, 6, 15)),
        Instructor(instructor_name="Dr. Manhattan", department="History", hire_date=date(2020, 7, 16)),
        Instructor(instructor_name="Dr. Strange", department="Biology", hire_date=date(2020, 8, 17)),
        Instructor(instructor_name="Dr. Richards", department="Physics", hire_date=date(2020, 9, 18)),
        Instructor(instructor_name="Dr. Stark", department="Engineering", hire_date=date(2020, 10, 19)),
    ]

    db.session.add_all(students)
    db.session.add_all(instructors)
    db.session.commit()

    courses = [
        Course(course_name="Calculus III", credits=3, instructor_id=1),
        Course(course_name="World History", credits=4, instructor_id=2),
        Course(course_name="Biology III", credits=3, instructor_id=3),
        Course(course_name="Physics III", credits=3, instructor_id=4),
        Course(course_name="Advanced Design", credits=4, instructor_id=5),
    ]

    db.session.add_all(courses)
    db.session.commit()

    enrollments = [
        Enrollment(student_id=1, course_id=1, grade=92.5, enrollment_date=date(2024, 1, 15)),
        Enrollment(student_id=2, course_id=2, grade=90.0, enrollment_date=date(2024, 2, 16)),
        Enrollment(student_id=3, course_id=3, grade=80.0, enrollment_date=date(2024, 3, 17)),
        Enrollment(student_id=4, course_id=4, grade=85.5, enrollment_date=date(2024, 4, 18)),
        Enrollment(student_id=5, course_id=5, grade=75.0, enrollment_date=date(2024, 5, 19)),
    ]

    db.session.add_all(enrollments)
    db.session.commit()

    print("Database initialized successfully.")