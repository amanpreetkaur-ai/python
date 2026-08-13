Project Title

Student Attendance Management System

Project Description

This project is a GUI-based Student Attendance Management System developed using Python Tkinter for the graphical user interface and MySQL for database management. The system is designed to simplify the process of maintaining student records and managing daily attendance.

The application allows the user to select a course such as B.Tech, BCA, BBA, or B.Com, followed by the corresponding branch. Students can be added to the database with their name and roll number, and existing students can be displayed for attendance marking.

For each student, the user can mark their attendance as Present or Absent. The system automatically records the current date and stores the attendance information in the MySQL database. If attendance for the same student has already been marked on that date, the system updates the existing record instead of creating a duplicate entry.

The application also provides an Attendance Report feature, where the user can enter a specific date in YYYY-MM-DD format and retrieve the attendance records for that day. The report displays the student's name, roll number, course, branch, and attendance status.

The project uses a relational database structure, where student information and attendance records are maintained in separate tables and connected using a foreign key. This helps maintain organized and consistent attendance data.

Main Features
Course Selection
B.Tech
BCA
BBA
B.Com
Branch Selection
B.Tech branches include CSE, DS, Civil, ECE, and Mechanical.
Other courses currently use a General branch.
Student Management
Add new students.
Store student name, roll number, course, and branch.
View students according to their course and branch.
Attendance Management
Mark students as Present or Absent.
Automatically record the current date.
Update attendance if it has already been marked for that day.
Prevent duplicate attendance records for the same student and date.
Attendance Reports
Search attendance using a specific date.
Display student details along with attendance status.
Color-coded status for easier identification.
Database Management
Uses MySQL to store student and attendance information.
Automatically creates the required tables if they do not already exist.
Uses a foreign-key relationship between students and attendance.
Technologies Used
Technology	Purpose
Python	Main programming language
Tkinter	Graphical User Interface
MySQL	Database management
mysql-connector-python	Connecting Python with MySQL
SQL	Creating and managing database records
datetime	Handling attendance dates
Database Structure

Your application uses two main tables:

students

id — Primary key
name — Student name
roll_no — Roll number
course — Course name
branch — Branch name

attendance

id — Primary key
student_id — Foreign key referring to the student
date — Attendance date
status — Present/Absent

The relationship can be represented as:

Students → Attendance

One student can have multiple attendance records across different dates.

Working Flow

Start Application → Select Course → Select Branch → Add/View Students → Mark Present/Absent → Store in MySQL → View Attendance Report by Date
