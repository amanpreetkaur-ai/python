import tkinter as tk
from tkinter import messagebox
import mysql.connector
from datetime import date

# ---------- Database Connection ----------
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="aman2808",  
        database="attendance_db"
    )

# ---------- Database Setup ----------
def setup_database():
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            roll_no VARCHAR(50),
            course VARCHAR(50),
            branch VARCHAR(50)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INT AUTO_INCREMENT PRIMARY KEY,
            student_id INT,
            date DATE,
            status ENUM('Present','Absent'),
            FOREIGN KEY (student_id) REFERENCES students(id)
        )
    """)  

    conn.commit()
    conn.close()

# ---------- Main Application ----------
class AttendanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Attendance Manager")
        self.root.geometry("400x300")

        tk.Label(root, text="Attendance Manager", font=("Arial", 18, "bold")).pack(pady=40)
        tk.Button(root, text="Start", font=("Arial", 14), width=12, command=self.open_course_window).pack(pady=10)
        tk.Button(root, text="View Attendance Report", font=("Arial", 14), width=22, command=self.open_report_window).pack(pady=10)

    # ---------- Course Selection ----------
    def open_course_window(self):
        self.course_window = tk.Toplevel(self.root)
        self.course_window.title("Select Course")
        self.course_window.geometry("400x400")

        tk.Label(self.course_window, text="Select Course", font=("Arial", 16, "bold")).pack(pady=10)

        courses = ["B.Tech", "BCA", "BBA", "B.Com"]
        for course in courses:
            tk.Button(self.course_window, text=course, width=20,
                      command=lambda c=course: self.open_branch_window(c)).pack(pady=5)

    # ---------- Branch Selection ----------
    def open_branch_window(self, course):
        self.branch_window = tk.Toplevel(self.root)
        self.branch_window.title(f"{course} Branches")
        self.branch_window.geometry("400x400")

        tk.Label(self.branch_window, text=f"{course} Branches", font=("Arial", 16, "bold")).pack(pady=10)

        if course == "B.Tech":
            branches = ["CSE", "DS", "Civil", "ECE", "Mechanical"]
        else:
            branches = ["General"]

        for branch in branches:
            frame = tk.Frame(self.branch_window)
            frame.pack(pady=5)

            tk.Label(frame, text=branch, font=("Arial", 12, "bold")).pack(side=tk.LEFT, padx=10)

            tk.Button(frame, text="Add Student", command=lambda c=course, b=branch: self.add_student_window(c, b)).pack(side=tk.LEFT, padx=5)
            tk.Button(frame, text="Show Students", command=lambda c=course, b=branch: self.show_students_window(c, b)).pack(side=tk.LEFT, padx=5)

    # ---------- Add Student ----------
    def add_student_window(self, course, branch):
        win = tk.Toplevel(self.root)
        win.title("Add Student")
        win.geometry("400x300")

        tk.Label(win, text=f"Add Student - {course} {branch}", font=("Arial", 14, "bold")).pack(pady=10)

        tk.Label(win, text="Name:").pack()
        name_entry = tk.Entry(win)
        name_entry.pack()

        tk.Label(win, text="Roll No:").pack()
        roll_entry = tk.Entry(win)
        roll_entry.pack()

        def save_student():
            name = name_entry.get()
            roll = roll_entry.get()
            if not name or not roll:
                messagebox.showerror("Error", "Please fill all fields")
                return

            try:
                conn = connect_db()
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO students (name, roll_no, course, branch) VALUES (%s, %s, %s, %s)",
                    (name, roll, course, branch)
                )
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "Student added successfully!")
                win.destroy()
            except Exception as e:
                messagebox.showerror("Database Error", str(e))

        tk.Button(win, text="Save", command=save_student).pack(pady=10)

    # ---------- Show Students ----------
    def show_students_window(self, course, branch):
        win = tk.Toplevel(self.root)
        win.title(f"{branch} Students")
        win.geometry("600x500")

        tk.Label(win, text=f"{course} - {branch} Students", font=("Arial", 16, "bold")).pack(pady=10)

        conn = connect_db()
        cur = conn.cursor()
        cur.execute("SELECT id, name, roll_no FROM students WHERE course=%s AND branch=%s", (course, branch))
        students = cur.fetchall()
        conn.close()

        if not students:
            tk.Label(win, text="No students found.", font=("Arial", 12)).pack()
            return

        for sid, name, roll in students:
            frame = tk.Frame(win)
            frame.pack(pady=5)

            tk.Label(frame, text=f"{name} ({roll})", width=25, anchor="w").pack(side=tk.LEFT, padx=10)

            status_label = tk.Label(frame, text="Not Marked", fg="gray")
            status_label.pack(side=tk.LEFT, padx=10)

            tk.Button(frame, text="Present", bg="lightgreen",
                      command=lambda s=sid, l=status_label: self.mark_attendance(s, "Present", l)).pack(side=tk.LEFT, padx=5)
            tk.Button(frame, text="Absent", bg="lightcoral",
                      command=lambda s=sid, l=status_label: self.mark_attendance(s, "Absent", l)).pack(side=tk.LEFT, padx=5)

    # ---------- Mark Attendance ----------
    def mark_attendance(self, student_id, status, label_widget):
        today = date.today()

        try:
            conn = connect_db()
            cur = conn.cursor()

            cur.execute("SELECT id FROM attendance WHERE student_id=%s AND date=%s", (student_id, today))
            record = cur.fetchone()

            if record:
                cur.execute("UPDATE attendance SET status=%s WHERE student_id=%s AND date=%s",
                            (status, student_id, today))
            else:
                cur.execute("INSERT INTO attendance (student_id, date, status) VALUES (%s, %s, %s)",
                            (student_id, today, status))

            conn.commit()
            conn.close()

            label_widget.config(
                text=f"{status} ({today})",
                fg="green" if status == "Present" else "red",
                font=("Arial", 10, "bold")
            )

            messagebox.showinfo("Marked", f"{status} marked for {today}")

        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    # ---------- View Attendance Report ----------
    def open_report_window(self):
        win = tk.Toplevel(self.root)
        win.title("Attendance Report")
        win.geometry("500x400")

        tk.Label(win, text="View Attendance by Date", font=("Arial", 16, "bold")).pack(pady=10)
        tk.Label(win, text="Enter Date (YYYY-MM-DD):").pack()

        date_entry = tk.Entry(win)
        date_entry.pack(pady=5)

        result_frame = tk.Frame(win)
        result_frame.pack(pady=10)

        def search_attendance():
            for widget in result_frame.winfo_children():
                widget.destroy()

            selected_date = date_entry.get().strip()
            if not selected_date:
                messagebox.showerror("Error", "Please enter a date (YYYY-MM-DD)")
                return

            try:
                conn = connect_db()
                cur = conn.cursor()
                cur.execute("""
                    SELECT s.name, s.roll_no, s.course, s.branch, a.status
                    FROM attendance a
                    JOIN students s ON a.student_id = s.id
                    WHERE a.date = %s
                """, (selected_date,))
                records = cur.fetchall()
                conn.close()

                if not records:
                    tk.Label(result_frame, text="No attendance found for this date.", fg="gray").pack()
                else:
                    for (name, roll, course, branch, status) in records:
                        tk.Label(result_frame, text=f"{name} ({roll}) - {course} {branch} - {status}",
                                 fg="green" if status == "Present" else "red").pack(anchor="w")

            except Exception as e:
                messagebox.showerror("Database Error", str(e))

        tk.Button(win, text="Search", command=search_attendance).pack(pady=10)

# ---------- Run App ----------
if __name__ == "__main__":
    setup_database()
    root = tk.Tk()
    app = AttendanceApp(root)
    root.mainloop()
