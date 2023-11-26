import streamlit as st
import mysql.connector
from database import create_connection

# Function to fetch all instructors
def fetch_all_instructors():
    db = create_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Instructor INNER JOIN Account ON Instructor.Instructor_ID = Account.Instructor_ID WHERE Account_Type = 'instructor'")
    instructors = cursor.fetchall()
    db.close()
    return instructors

# Function to fetch all Students
def fetch_users():
    db = create_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT User_ID, Username FROM User")
    users = cursor.fetchall()
    db.close()
    return users

# Function to fetch all courses
def fetch_courses():
    db = create_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Course")
    courses = cursor.fetchall()
    db.close()
    return courses

def add_instructor(username, password):
    db = create_connection()
    cursor = db.cursor()
    
    # Insert into User table
    cursor.execute("INSERT INTO  Instructor (Instructor_Name, Password) VALUES (%s, %s)", (username, password))
    id = cursor.lastrowid
    
    # Insert into Account table with Account_Type 'instructor'
    cursor.execute("INSERT INTO Account (Account_Type,Instructor_ID) VALUES ('instructor',%s)", (id,))
    
    db.commit()
    cursor.close()
    db.close()

def fetch_all_instructors_with_course_count():
    db = create_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT Instructor.*, GetCourseCountForInstructor(Instructor.Instructor_ID) AS Course_Count
        FROM Instructor
        INNER JOIN Account ON Instructor.Instructor_ID = Account.Instructor_ID
        WHERE Account.Account_Type = 'instructor'
    """)
    instructors = cursor.fetchall()
    db.close()
    return instructors

# Function to fetch pending courses for approval
def fetch_pending_courses():
    db = create_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
    SELECT Course.*
    FROM Course
    JOIN Content ON Course.Course_ID = Content.Course_ID
    WHERE Content.Approval_Status = 'Pending'
""")

    pending_courses = cursor.fetchall()
    db.close()
    return pending_courses

# Function to approve a pending course
def approve_course(course_id, admin_id):
    db = create_connection()
    cursor = db.cursor()
    cursor.execute("UPDATE Content SET Approval_Status = 'Approved' WHERE Course_ID = %s", (course_id,))
    cursor.execute("UPDATE Content SET Admin_ID = %s WHERE Course_ID = %s", (admin_id,course_id))

    db.commit()
    cursor.close()
    db.close()

def reject_course(course_id):
    db = create_connection()
    cursor = db.cursor()

    try:
        # Delete the corresponding content entry from the Content table
        cursor.execute("DELETE FROM Content WHERE Course_ID = %s", (course_id,))

        # Delete the course entry from the Course table
        cursor.execute("DELETE FROM Course WHERE Course_ID = %s", (course_id,))

        # Commit the changes
        db.commit()
        st.success("Course rejected successfully.")

    except mysql.connector.Error as err:
        db.rollback()
        st.error(f"Error: {err}")

    finally:
        cursor.close()
        db.close()

# Function to fetch all support requests
def fetch_all_support_requests():
    db = create_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Support")
    support_requests = cursor.fetchall()
    db.close()
    return support_requests

# Function to send a reply to a support request
def send_support_reply(support_id, admin_id, reply_text):
    db = create_connection()
    cursor = db.cursor()
    cursor.execute(cursor.execute("UPDATE Support SET Admin_ID = %s, Reply = %s WHERE Support_No = %s", (admin_id, reply_text, support_id)))
    db.commit()
    cursor.close()
    db.close()

    # Function to delete a resolved support entry
def delete_support_entry(support_id):
    db = create_connection()
    cursor = db.cursor()
    cursor.execute("DELETE FROM Support WHERE Support_No = %s", (support_id,))
    db.commit()
    cursor.close()
    db.close()

# Function to fetch the number of students
def fetch_student_count():
    db = create_connection()
    cursor = db.cursor(dictionary=True)  # Set dictionary=True to fetch results as dictionaries
    cursor.execute("SELECT COUNT(*) AS student_count FROM Account WHERE Account_Type = 'student'")
    student_count = cursor.fetchone()
    if student_count:
        student_count = student_count['student_count']
    else:
        student_count = 0  # Set default value if no count is returned
    db.close()
    return student_count

# Function to fetch the number of instructors
def fetch_instructor_count():
    db = create_connection()
    cursor = db.cursor(dictionary=True)  
    cursor.execute("SELECT COUNT(*) AS instructor_count FROM Account WHERE Account_Type = 'instructor'")
    instructor_count = cursor.fetchone()
    if instructor_count:
        instructor_count = instructor_count['instructor_count']
    else:
        instructor_count = 0  
    db.close()
    return instructor_count



def admin_dashboard(user):
    st.title("Admin Dashboard")
    st.write(f"Welcome, {user['Admin_Name']}! You are logged in as an administrator.")

        # List the number of students
    with st.expander("Number of Students", expanded=False):
        student_count = fetch_student_count()
        st.write(f"Total number of students: {student_count}")

    # List the number of instructors
    with st.expander("Number of Instructors", expanded=False):
        instructor_count = fetch_instructor_count()
        st.write(f"Total number of instructors: {instructor_count}")

    # Display instructors and their course counts
    with st.expander("Instructors and Their Course Counts", expanded=False):
        instructors = fetch_all_instructors_with_course_count()
        for instructor in instructors:
            st.write(f"Instructor Name: {instructor['Instructor_Name']}")
            st.write(f"Number of Courses: {instructor['Course_Count']}")
            st.write("----------------------------")


     # Add new instructor form
    with st.expander("Add New Instructor", expanded=False):
        new_instructor_username = st.text_input("Instructor Name")
        new_instructor_password = st.text_input("Instructor Passcode", type="password")
        
        if st.button("Add Instructor"):
            add_instructor(new_instructor_username, new_instructor_password)
            st.success("Instructor added successfully.")

    admin_id = user['Admin_ID']
    # List pending courses for approval
    with st.expander("Pending Courses for Approval", expanded=False):
        pending_courses = fetch_pending_courses()
        for course in pending_courses:
            st.write(f"Course ID: {course['Course_ID']}, Course Name: {course['course_name']}")
            
            # Buttons for approval and rejection
            col1, col2 = st.columns(2)
            
            if col1.button(f"Approve {course['course_name']}"):
                approve_course(course['Course_ID'], admin_id)
                st.success(f"Course '{course['course_name']}' approved successfully.")

            if col2.button(f"Reject {course['course_name']}"):
                reject_course(course['Course_ID'])
                st.write(f"Course '{course['course_name']}' rejected and deleted successfully.")
        
    # List all support requests
    with st.expander("All Support Req", expanded=False):
        support_requests = fetch_all_support_requests()
        for request in support_requests:
            st.write(f"Support ID: {request['Support_No']}, User ID: {request['User_ID']}, Request: {request['Request']}")
            reply_text = st.text_area(f"Reply to Support ID {request['Support_No']}:")

            if st.button(f"Send Reply to User {request['User_ID']}", key=f"reply_button_{request['Support_No']}"):
                send_support_reply(request['Support_No'], user['Admin_ID'], reply_text)
                st.success("Reply sent successfully.")
                delete_support_entry(request['Support_No'])
                st.info("Support request has been resolved.")
