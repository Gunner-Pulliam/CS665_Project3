# CS665_Project3: Student Course Manager

## Project Requirements
In this project, you will develop a functional full-stack application using Python. You will use your previously designed database for this project. Your goal is to build a robust backend and a user-friendly frontend that allows users to interact with this data effectively while maintaining strict data integrity

## Project Description
Student Course Manager is a full-stack Python web application that allows users to manage students, courses, and enrollments. The application is intended for a school or college that needs a simple way to track students, course enrollment, and grades.

## Instructions
**1. Clone the repository OR Download**

Use: git clone YOUR_REPOSITORY_URL

**OR** download reposotory as a Zip and extract it

Then open a command terminal and change to the directory: cd CS665_Project3

**2. Create a virtual environment**

In command terminal: python -m venv venv

**3. Activate the virtual environment**

In command terminal: venv\Scripts\activate

**4. Install dependencies**

In command terminal: pip install -r requirements.txt

**5. Setup the database**

In command terminal: python init_db.py

**6. Run the app**

In command terminal: python app.py

**7. Open the website**

open the application in a browser using the provided link

# Normalization Report

## Original Functional Dependencies

### Students
- student_id → first_name, last_name, email, enrollment_date, created_at
- email → student_id, first_name, last_name, enrollment_date

### Instructors
- instructor_id → instructor_name, department, hire_date, created_at

### Courses
- course_id → course_name, credits, instructor_id, created_at
- instructor_id → instructor_name, department, hire_date

### Enrollments
- enrollment_id → student_id, course_id, grade, enrollment_date, created_at
- student_id, course_id → enrollment_id, grade, enrollment_date

## Anomaly Identification

The original design was mostly normalized because students, instructors, courses, and enrollments were stored in separate tables. However, there were still potential issues.

### Update Anomaly
If a derived value such as grade_status is stored in the Enrollments table, then changing a grade would also require updating grade_status. If this is not updated correctly, the data could become inconsistent.

### Insertion Anomaly
If course and instructor information were stored together in one large table, a new instructor could not be added unless they were already assigned to a course.

### Deletion Anomaly
If a student enrollment were deleted from a combined table, important course or instructor information could accidentally be lost if that was the only row containing the data.

## Decomposition Steps

The database was decomposed into four tables:

1. Students stores only student-specific information.
2. Instructors stores only instructor-specific information.
3. Courses stores course-specific information and references the instructor teaching the course.
4. Enrollments resolves the many-to-many relationship between Students and Courses.

The derived grade_status field was removed because it can be calculated from the grade value instead of being stored.

## Final Relational Schema

Students(student_id, first_name, last_name, email, enrollment_date, created_at)

Instructors(instructor_id, instructor_name, department, hire_date, created_at)

Courses(course_id, course_name, credits, instructor_id, created_at)

Enrollments(enrollment_id, student_id, course_id, grade, enrollment_date, created_at)

## 3NF Explanation

Each table is in 3rd Normal Form because every non-key attribute depends only on the primary key, the whole key, and nothing but the key. There are no repeating groups, no partial dependencies, and no transitive dependencies. The many-to-many relationship between students and courses is properly handled by the Enrollments table.

# AI Log


