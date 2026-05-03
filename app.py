from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from datetime import date

app = Flask(__name__)
app.config["SECRET_KEY"] = "dev-key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///student_course_manager.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Student(db.Model):
    __tablename__ = "Students"

    student_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    enrollment_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.current_timestamp())

    enrollments = db.relationship("Enrollment", back_populates="student", cascade="all, delete-orphan")


class Instructor(db.Model):
    __tablename__ = "Instructors"

    instructor_id = db.Column(db.Integer, primary_key=True)
    instructor_name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    hire_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.current_timestamp())

    courses = db.relationship("Course", back_populates="instructor")


class Course(db.Model):
    __tablename__ = "Courses"

    course_id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(100), nullable=False)
    credits = db.Column(db.Integer, nullable=False)
    instructor_id = db.Column(db.Integer, db.ForeignKey("Instructors.instructor_id"), nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.current_timestamp())

    instructor = db.relationship("Instructor", back_populates="courses")
    enrollments = db.relationship("Enrollment", back_populates="course", cascade="all, delete-orphan")


class Enrollment(db.Model):
    __tablename__ = "Enrollments"

    enrollment_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("Students.student_id"), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("Courses.course_id"), nullable=False)
    grade = db.Column(db.Numeric(5, 2), nullable=True)
    enrollment_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.current_timestamp())

    student = db.relationship("Student", back_populates="enrollments")
    course = db.relationship("Course", back_populates="enrollments")

    __table_args__ = (
        db.UniqueConstraint("student_id", "course_id", name="unique_student_course"),
    )


def parse_date(value):
    return date.fromisoformat(value)


def validate_student(first_name, last_name, email, enrollment_date):
    if not first_name.strip():
        return "First name is required."
    if not last_name.strip():
        return "Last name is required."
    if not email.strip() or "@" not in email:
        return "A valid email is required."
    if not enrollment_date:
        return "Enrollment date is required."
    return None


def validate_course(course_name, credits):
    if not course_name.strip():
        return "Course name is required."
    try:
        credits = int(credits)
        if credits <= 0:
            return "Credits must be greater than 0."
    except ValueError:
        return "Credits must be a number."
    return None


@app.route("/")
def dashboard():
    total_students = db.session.query(func.count(Student.student_id)).scalar()
    total_courses = db.session.query(func.count(Course.course_id)).scalar()
    total_instructors = db.session.query(func.count(Instructor.instructor_id)).scalar()
    total_enrollments = db.session.query(func.count(Enrollment.enrollment_id)).scalar()
    average_grade = db.session.query(func.avg(Enrollment.grade)).scalar()

    course_stats = (
        db.session.query(
            Course.course_name,
            func.count(Enrollment.enrollment_id).label("student_count"),
            func.avg(Enrollment.grade).label("avg_grade")
        )
        .outerjoin(Enrollment)
        .group_by(Course.course_id)
        .all()
    )

    return render_template(
        "dashboard.html",
        total_students=total_students,
        total_courses=total_courses,
        total_instructors=total_instructors,
        total_enrollments=total_enrollments,
        average_grade=average_grade,
        course_stats=course_stats
    )


@app.route("/students")
def students():
    all_students = Student.query.order_by(Student.last_name).all()
    return render_template("students.html", students=all_students)


@app.route("/students/add", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        error = validate_student(
            request.form["first_name"],
            request.form["last_name"],
            request.form["email"],
            request.form["enrollment_date"]
        )

        if error:
            flash(error, "danger")
            return redirect(url_for("add_student"))

        student = Student(
            first_name=request.form["first_name"],
            last_name=request.form["last_name"],
            email=request.form["email"],
            enrollment_date=parse_date(request.form["enrollment_date"])
        )

        db.session.add(student)
        db.session.commit()
        flash("Student added successfully.", "success")
        return redirect(url_for("students"))

    return render_template("student_form.html", student=None)


@app.route("/students/<int:student_id>/edit", methods=["GET", "POST"])
def edit_student(student_id):
    student = Student.query.get_or_404(student_id)

    if request.method == "POST":
        error = validate_student(
            request.form["first_name"],
            request.form["last_name"],
            request.form["email"],
            request.form["enrollment_date"]
        )

        if error:
            flash(error, "danger")
            return redirect(url_for("edit_student", student_id=student_id))

        student.first_name = request.form["first_name"]
        student.last_name = request.form["last_name"]
        student.email = request.form["email"]
        student.enrollment_date = parse_date(request.form["enrollment_date"])

        db.session.commit()
        flash("Student updated successfully.", "success")
        return redirect(url_for("students"))

    return render_template("student_form.html", student=student)


@app.route("/students/<int:student_id>/delete", methods=["POST"])
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    flash("Student deleted successfully.", "success")
    return redirect(url_for("students"))


@app.route("/courses")
def courses():
    all_courses = Course.query.order_by(Course.course_name).all()
    return render_template("courses.html", courses=all_courses)


@app.route("/courses/add", methods=["GET", "POST"])
def add_course():
    instructors = Instructor.query.order_by(Instructor.instructor_name).all()

    if request.method == "POST":
        error = validate_course(request.form["course_name"], request.form["credits"])

        if error:
            flash(error, "danger")
            return redirect(url_for("add_course"))

        course = Course(
            course_name=request.form["course_name"],
            credits=int(request.form["credits"]),
            instructor_id=int(request.form["instructor_id"])
        )

        db.session.add(course)
        db.session.commit()
        flash("Course added successfully.", "success")
        return redirect(url_for("courses"))

    return render_template("course_form.html", course=None, instructors=instructors)


@app.route("/enrollments")
def enrollments():
    all_enrollments = Enrollment.query.order_by(Enrollment.enrollment_date.desc()).all()
    return render_template("enrollments.html", enrollments=all_enrollments)


@app.route("/enrollments/add", methods=["GET", "POST"])
def add_enrollment():
    students = Student.query.order_by(Student.last_name).all()
    courses = Course.query.order_by(Course.course_name).all()

    if request.method == "POST":
        student_id = int(request.form["student_id"])
        course_id = int(request.form["course_id"])
        grade = request.form["grade"]

        existing = Enrollment.query.filter_by(student_id=student_id, course_id=course_id).first()
        if existing:
            flash("This student is already enrolled in that course.", "danger")
            return redirect(url_for("add_enrollment"))

        if grade:
            grade = float(grade)
            if grade < 0 or grade > 100:
                flash("Grade must be between 0 and 100.", "danger")
                return redirect(url_for("add_enrollment"))
        else:
            grade = None

        # Transaction logic:
        # The enrollment is created only if all validation passes.
        try:
            enrollment = Enrollment(
                student_id=student_id,
                course_id=course_id,
                grade=grade,
                enrollment_date=parse_date(request.form["enrollment_date"])
            )

            db.session.add(enrollment)
            db.session.commit()
            flash("Enrollment added successfully.", "success")

        except Exception:
            db.session.rollback()
            flash("Enrollment could not be created. Transaction was rolled back.", "danger")

        return redirect(url_for("enrollments"))

    return render_template(
        "enrollment_form.html",
        students=students,
        courses=courses
    )


if __name__ == "__main__":
    app.run(debug=True)