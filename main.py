
import json
import os

FILE_NAME = "students.json"


def load_students():
    if not os.path.exists(FILE_NAME):
        return []

    try:
        with open(FILE_NAME, "r") as file:
            data = json.load(file)
            return data.get("students", [])
    except (json.JSONDecodeError, OSError):
        return []


def save_students(students):
    with open(FILE_NAME, "w") as file:
        json.dump({"students": students}, file, indent=4)


def add_student():
    students = load_students()

    student_id = input("Enter Student ID: ").strip()

    if not student_id:
        print("Student ID cannot be empty.")
        return

    if any(s["id"] == student_id for s in students):
        print("Student ID already exists!")
        return

    name = input("Enter Student Name: ").strip()
    age = input("Enter Age: ").strip()
    course = input("Enter Course: ").strip()
    email = input("Enter Email: ").strip()

    if not all([name, age, course, email]):
        print("All fields are required.")
        return

    if not age.isdigit() or int(age) <= 0:
        print("Enter a valid age.")
        return

    students.append({
        "id": student_id,
        "name": name,
        "age": int(age),
        "course": course,
        "email": email
    })

    save_students(students)
    print("Student added successfully!")


def view_students():
    students = load_students()

    if not students:
        print("No students found.")
        return

    print("\n========== STUDENT RECORDS ==========")

    for student in students:
        print(
            f"\nID: {student['id']}"
            f"\nName: {student['name']}"
            f"\nAge: {student['age']}"
            f"\nCourse: {student['course']}"
            f"\nEmail: {student['email']}"
        )


def search_student():
    students = load_students()
    student_id = input("Enter Student ID to search: ").strip()

    for student in students:
        if student["id"] == student_id:
            print("\nStudent Found!")
            print(student)
            return

    print("Student not found.")


def update_student():
    students = load_students()
    student_id = input("Enter Student ID to update: ").strip()

    for student in students:
        if student["id"] == student_id:
            name = input(f"New Name [{student['name']}]: ").strip()
            age = input(f"New Age [{student['age']}]: ").strip()
            course = input(f"New Course [{student['course']}]: ").strip()
            email = input(f"New Email [{student['email']}]: ").strip()

            if age and (not age.isdigit() or int(age) <= 0):
                print("Enter a valid age.")
                return

            student["name"] = name or student["name"]
            student["age"] = int(age) if age else student["age"]
            student["course"] = course or student["course"]
            student["email"] = email or student["email"]

            save_students(students)
            print("Student updated successfully!")
            return

    print("Student not found.")


def delete_student():
    students = load_students()
    student_id = input("Enter Student ID to delete: ").strip()

    updated_students = [
        student for student in students
        if student["id"] != student_id
    ]

    if len(updated_students) == len(students):
        print("Student not found.")
        return

    save_students(updated_students)
    print("Student deleted successfully!")


def main():
    while True:
        print("\n===== STUDENT MANAGEMENT SYSTEM =====")
        print("1. Add Student")
        print("2. View Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_student()
        elif choice == "2":
            view_students()
        elif choice == "3":
            search_student()
        elif choice == "4":
            update_student()
        elif choice == "5":
            delete_student()
        elif choice == "6":
            print("Thank you for using Student Management System!")
            break
        else:
            print("Invalid choice! Try again.")


if __name__ == "__main__":
    main()
