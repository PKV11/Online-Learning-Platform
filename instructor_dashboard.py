import streamlit as st
import mysql.connector
from database import create_connection

# Function to fetch courses for a specific instructor
def fetch_instructor_courses(instructor_id):
    db = create_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Course WHERE Instructor_ID = %s", (instructor_id,))
    courses = cursor.fetchall()
    db.close()
    return courses

# Function to fetch tests for a specific instructor
def fetch_instructor_tests(instructor_id):
    db = create_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Test WHERE User_ID IN (SELECT Instructor_ID FROM Account WHERE Account_Type = 'instructor' AND Instructor_ID = %s)", (instructor_id,))
    tests = cursor.fetchall()
    db.close()
    return tests

# Function to add a new course
def add_course(course_name, instructor_id, content_details):
    db = create_connection()
    cursor = db.cursor(dictionary=True)
    
    # Insert course details
    cursor.execute("INSERT INTO Course (Course_Name, Instructor_ID) VALUES (%s, %s)", (course_name, instructor_id))
    course_id = cursor.lastrowid

    # Insert content details
    cursor.execute("INSERT INTO Content (Content_Details, Course_ID, Admin_ID, Approval_Status) VALUES (%s, %s, 2, 'Pending')", (content_details, course_id,))
    
    db.commit()
    cursor.close()
    db.close()


# Function to check if the instructor is assigned to the course
def is_instructor_assigned_to_course(course_id, instructor_id):
    db = create_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) AS count FROM Course WHERE Course_ID = %s AND Instructor_ID = %s", (course_id, instructor_id))
    result = cursor.fetchone()
    db.close()
    return result['count'] > 0

# Function to add a test by instructor
def add_test(course_id, instructor_id, test_details, is_final_test):
    db = create_connection()
    cursor = db.cursor()
    if not is_instructor_assigned_to_course(course_id, instructor_id):
        return None

    cursor.execute("""
        INSERT INTO Test (User_ID, Course_ID, Test_Details, Instructor_ID, Test_Status, final_test)
        VALUES (5, %s, %s, %s, 'Available', %s)
    """, (course_id, test_details, instructor_id, is_final_test))
    
    test_id = cursor.lastrowid

    cursor.execute("""
        INSERT INTO Evaluation (Test_ID, Instructor_ID, User_ID, Test_Grade)
        VALUES (%s, %s, 5, NULL)
    """, (test_id, instructor_id))

    db.commit()
    cursor.close()
    db.close()
    return test_id  

# Modify the function to fetch pending tests for evaluation based on submitted responses
def fetch_pending_tests_for_evaluation(instructor_id):
    db = create_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT Evaluation.Test_ID, Evaluation.User_ID 
        FROM Evaluation 
        INNER JOIN Test ON Evaluation.Test_ID = Test.Test_ID 
        WHERE Evaluation.Instructor_ID = %s 
        AND Evaluation.Test_Grade IS NULL 
        AND Test.Test_Status = 'Completed' 
        AND Evaluation.Test_ID IN (
            SELECT Test_ID 
            FROM Evaluation 
            WHERE Test_Response IS NOT NULL
        )
    """, (instructor_id,))
    pending_tests = cursor.fetchall()
    db.close()
    return pending_tests

from datetime import datetime

# Function to evaluate a test by instructor
def evaluate_test(test_id, user_id, instructor_id, test_grade):
    db = create_connection()
    cursor = db.cursor()
    
    cursor.execute("""
        UPDATE Evaluation SET Test_Grade = %s WHERE Test_ID = %s AND User_ID = %s AND Instructor_ID = %s
    """, (test_grade, test_id, user_id, instructor_id))
    
    db.commit()
    cursor.close()
    db.close()

# Function to add feedback for a specific test
def add_feedback(test_id, feedback_text):
    db = create_connection()
    cursor = db.cursor()
    cursor.execute("INSERT INTO Feedback (Test_ID, Feedback_Text) VALUES (%s, %s)", (test_id, feedback_text))
    db.commit()
    cursor.close()
    db.close()

def get_student_count_for_course(course_id):
    db = create_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("CALL GetStudentCountForCourse(%s)", (course_id,))
    result = cursor.fetchone()
    cursor.close()
    db.close()
    return result['student_count'] if result else 0



def instructor_dashboard(user):
    st.title("Instructor Dashboard")
    st.write(f"Welcome, {user['Instructor_Name']}! You are logged in as an instructor.")

    instructor_id = user['Instructor_ID']

    # List courses assigned to the instructor
    with st.expander("Your Courses", expanded=False):
        courses = fetch_instructor_courses(instructor_id)
        for course in courses:
            # Fetch the student count for each course
            student_count = get_student_count_for_course(course['Course_ID'])
            
            # Display course details along with the student count
            st.write(f"Course ID: {course['Course_ID']}, Course Name: {course['course_name']}, Student Count: {student_count}")


    # List tests assigned by the instructor
    with st.expander("Your Tests", expanded=False):
        tests = fetch_instructor_tests(instructor_id)
        for test in tests:
            st.write(f"Test ID: {test['Test_ID']}, User ID: {test['User_ID']}, Final Test: {test['final_test']}")
    

    # Add a new course
    with st.expander("Add a New Course", expanded=False):
        new_course_name = st.text_input("Enter Course Name:")
        new_course_content = st.text_area("Enter Course Content:")
        if st.button("Add Course"):
            add_course(new_course_name, instructor_id, new_course_content)
            st.success(f"Course '{new_course_name}' added successfully. Pending approval from admin.")

    # Add a new test
    with st.expander("Add New Test", expanded=False):
        course_id = st.text_input("Course ID")
        test_details = st.text_area("Test Details")
        is_final_test = st.checkbox("Is this the Final Test?")

        if st.button("Add Test"):
            test_id = add_test(course_id, instructor_id, test_details, is_final_test)
            if test_id == None:
                st.warning(f"Please choose a valid course ID")
            else:
                st.success(f"Test added successfully. Test ID: {test_id}")

    # Check for pending test evaluations for the instructor & providing feedback for evaluated tests
    pending_tests = fetch_pending_tests_for_evaluation(instructor_id)
    if pending_tests:
        with st.expander("Pending Evaluations", expanded=True):
            for test in pending_tests:
                st.write(f"Test ID: {test['Test_ID']}, User ID: {test['User_ID']}")
                test_grade = st.text_input("Test Grade")
                feedback_text = st.text_area("Feedback")
                if st.button(f"Evaluate Test ID {test['Test_ID']}"):
                    evaluate_test(test['Test_ID'], test['User_ID'], instructor_id, test_grade)
                    if feedback_text:
                        add_feedback(test['Test_ID'], feedback_text)
                    st.success("Test evaluated and feedback provided successfully.")
    else:
        st.write("No pending tests for evaluation.")
    
