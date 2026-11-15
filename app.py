
import json
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "student-management-secret"

DATA_FILE = Path(__file__).resolve().parent / "students.json"


def load_students():
    if not DATA_FILE.exists():
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data.get("students", [])
    except (json.JSONDecodeError, OSError):
        return []


def save_students(students):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump({"students": students}, file, indent=4)


@app.route("/")
def index():
    students = load_students()
    search = request.args.get("search", "").strip().lower()

    if search:
        students = [
            s for s in students
            if search in s["id"].lower()
            or search in s["name"].lower()
            or search in s["course"].lower()
            or search in s["email"].lower()
        ]

    return render_template(
        "index.html",
        students=students,
        search=request.args.get("search", "")
    )


@app.route("/add", methods=["POST"])
def add_student():
    students = load_students()

    student_id = request.form.get("student_id", "").strip()
    name = request.form.get("name", "").strip()
    age = request.form.get("age", "").strip()
    course = request.form.get("course", "").strip()
    email = request.form.get("email", "").strip()

    if not all([student_id, name, age, course, email]):
        flash("All fields are required!", "danger")
    elif any(s["id"] == student_id for s in students):
        flash("Student ID already exists!", "danger")
    elif not age.isdigit() or int(age) <= 0:
        flash("Please enter a valid age!", "danger")
    else:
        students.append({
            "id": student_id,
            "name": name,
            "age": int(age),
            "course": course,
            "email": email
        })
        save_students(students)
        flash("Student added successfully!", "success")

    return redirect(url_for("index"))


@app.route("/update/<student_id>", methods=["POST"])
def update_student(student_id):
    students = load_students()

    for student in students:
        if student["id"] == student_id:
            name = request.form.get("name", "").strip()
            age = request.form.get("age", "").strip()
            course = request.form.get("course", "").strip()
            email = request.form.get("email", "").strip()

            if not all([name, age, course, email]):
                flash("All fields are required!", "danger")
            elif not age.isdigit() or int(age) <= 0:
                flash("Please enter a valid age!", "danger")
            else:
                student.update({
                    "name": name,
                    "age": int(age),
                    "course": course,
                    "email": email
                })
                save_students(students)
                flash("Student updated successfully!", "success")
            break
    else:
        flash("Student not found!", "danger")

    return redirect(url_for("index"))


@app.route("/delete/<student_id>", methods=["POST"])
def delete_student(student_id):
    students = load_students()
    updated = [s for s in students if s["id"] != student_id]

    if len(updated) == len(students):
        flash("Student not found!", "danger")
    else:
        save_students(updated)
        flash("Student deleted successfully!", "success")

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=3001, debug=True)
