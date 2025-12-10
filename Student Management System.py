import json
import os

class Student:
    def __init__(self, student_id, name, grade):
        self.student_id = student_id
        self.name = name
        self.grade = grade

    def to_dict(self):
        return {
            "id": self.student_id,
            "name": self.name,
            "grade": self.grade
        }

class StudentManager:
    FILE_NAME = "students.json"

    def __init__(self):
        self.students = []
        self.load_data()

    # Load data from file
    def load_data(self):
        if os.path.exists(self.FILE_NAME):
            with open(self.FILE_NAME, "r") as file:
                try:
                    data = json.load(file)
                    for item in data:
                        self.students.append(
                            Student(item["id"], item["name"], item["grade"])
                        )
                except json.JSONDecodeError:
                    self.students = []

    # Save data to file
    def save_data(self):
        with open(self.FILE_NAME, "w") as file:
            json.dump([s.to_dict() for s in self.students], file, indent=4)

    # Add a student
    def add_student(self, student):
        # Validation: unique ID
        for s in self.students:
            if s.student_id == student.student_id:
                print("Error: Student ID already exists")
                return
        self.students.append(student)
        self.save_data()
        print("Student added successfully")

    # Update a student
    def update_student(self, student_id, new_name, new_grade):
        for s in self.students:
            if s.student_id == student_id:
                s.name = new_name
                s.grade = new_grade
                self.save_data()
                print("Student updated successfully")
                return
        print("Student not found")

    # Delete a student
    def delete_student(self, student_id):
        for s in self.students:
            if s.student_id == student_id:
                self.students.remove(s)
                self.save_data()
                print("Student deleted successfully")
                return
        print("Student not found")

    # List all students in table format
    def list_students(self):
        if not self.students:
            print("No records found.")
            return

        print("\n----- Student Records -----")
        print("{:<10} {:<20} {:<10}".format("ID", "Name", "Grade"))
        print("-----------------------------------------------")
        for s in self.students:
            print("{:<10} {:<20} {:<10}".format(s.student_id, s.name, s.grade))
        print("-----------------------------------------------")

def main():
    manager = StudentManager()

    while True:
        print("\n===== Student Management System =====")
        print("1. Add Student")
        print("2. Update Student")
        print("3. Delete Student")
        print("4. List Students")
        print("5. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            student_id = input("Enter ID: ")
            name = input("Enter Name: ")
            grade = input("Enter Grade: ")
            manager.add_student(Student(student_id, name, grade))

        elif choice == "2":
            student_id = input("Enter ID to update: ")
            new_name = input("Enter new name: ")
            new_grade = input("Enter new grade: ")
            manager.update_student(student_id, new_name, new_grade)

        elif choice == "3":
            student_id = input("Enter ID to delete: ")
            manager.delete_student(student_id)

        elif choice == "4":
            manager.list_students()

        elif choice == "5":
            print("Exiting program...")
            break

        else:
            print("Invalid choice.Try again.")


if __name__ == "__main__":
    main()
