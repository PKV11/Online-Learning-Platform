import streamlit as st
from database import create_connection

# Function to fetch all courses
def fetch_all_courses():
    db = create_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Course")
    courses = cursor.fetchall()
    db.close()
    return courses

def fetch_enrolled_courses_with_status(student_id):
    db = create_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT Course.Course_ID, Course.course_name, Enrollment.course_status
        FROM Course
        INNER JOIN Enrollment ON Course.Course_ID = Enrollment.Course_ID
        WHERE Enrollment.User_ID = %s
    """, (student_id,))
    enrolled_courses = cursor.fetchall()
    db.close()
    return enrolled_courses

# Function to enroll in a course
def enroll_in_course(student_id, course_id):
    db = create_connection()
    cursor = db.cursor()
    cursor.execute("INSERT INTO Enrollment (User_ID, Course_ID) VALUES (%s, %s)", (student_id, course_id))
    db.commit()
    cursor.close()
    db.close()

# Function to enroll in a course
def enroll_in_course(student_id, course_id):
    db = create_connection()
    cursor = db.cursor()
    cursor.execute("INSERT INTO Enrollment (User_ID, Course_ID) VALUES (%s, %s)", (student_id, course_id))
    db.commit()
    cursor.close()
    db.close()

# Function to request support
def request_support(user_id, support_text):
    db = create_connection()
    cursor = db.cursor()
    cursor.execute("INSERT INTO Support (Admin_ID, User_ID, Request, Reply) VALUES (2, %s, %s, '-')", (user_id, support_text))
    db.commit()
    cursor.close()
    db.close()

# Function to submit a test by student
def submit_test(test_id, user_id, test_response):
    db = create_connection()
    cursor = db.cursor()
    
    # Update the Test & Evaluation table with user submission
    cursor.execute("UPDATE Test SET User_ID = %s, Test_Status = 'Completed' WHERE Test_ID = %s", (user_id, test_id))
    cursor.execute("UPDATE Evaluation SET Test_response = %s WHERE Test_ID = %s", (test_response, test_id))
    
    db.commit()
    cursor.close()
    db.close()

# Function to fetch past test grades for a specific student
def fetch_student_test_grades(user_id):
    db = create_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT Test_ID, Test_Grade FROM Evaluation WHERE User_ID = %s", (user_id,))
    past_test_grades = cursor.fetchall()
    db.close()
    return past_test_grades


# Function to fetch evaluation details for a specific test and user
def fetch_evaluation_details(test_id, user_id):
    db = create_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Test WHERE Test_ID = %s AND User_ID = %s", (test_id, user_id))
    evaluation_details = cursor.fetchone()
    db.close()
    return evaluation_details

# Function to fetch tests for a specific course
def fetch_tests_for_student(course_id, user_id):
    db = create_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Test WHERE Course_ID = %s AND Test_Status = 'Available' AND User_ID IS NULL", (course_id,))
    tests = cursor.fetchall()
    
    # Filter tests that haven't been taken by the current user
    tests_for_user = []
    for test in tests:
        if test['Test_ID'] not in [taken_test['Test_ID'] for taken_test in fetch_completed_tests(user_id)]:
            tests_for_user.append(test)
    
    db.close()
    return tests_for_user

# Function to fetch available tests for a specific user and course
def fetch_available_tests(user_id, course_id):
    db = create_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Test WHERE Course_ID = %s AND User_ID = %s AND Test_Status = 'Available'", (course_id, user_id))
    available_tests = cursor.fetchall()
    db.close()
    return available_tests

# Function to fetch completed tests for a specific user
def fetch_completed_tests(user_id):
    db = create_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Test INNER JOIN Evaluation ON Test.Test_ID = Evaluation.Test_ID "
                   "WHERE Evaluation.User_ID = %s AND Test.Test_Status = 'Completed'", (user_id,))
    completed_tests = cursor.fetchall()
    db.close()
    return completed_tests

# Function to fetch past test grades along with feedback for a specific student
def fetch_student_test_grades_with_feedback(user_id):
    db = create_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT Evaluation.Test_ID, Evaluation.Test_Grade, Feedback.Feedback_Text
        FROM Evaluation
        LEFT JOIN Feedback ON Evaluation.Test_ID = Feedback.Test_ID
        WHERE Evaluation.User_ID = %s
    """, (user_id,))
    past_test_grades_with_feedback = cursor.fetchall()
    db.close()
    return past_test_grades_with_feedback
"""# Function to fetch test result for a specific test and user
def fetch_test_result(test_id, user_id):
    db = create_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Evaluation WHERE Test_ID = %s AND User_ID = %s", (test_id, user_id))
    test_result = cursor.fetchone()
    db.close()
    return test_result"""

# Function to fetch all courses excluding enrolled courses for a student
def fetch_all_courses_exclude_enrolled(student_id):
    db = create_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT * FROM Course WHERE Course_ID NOT IN 
        (SELECT Course_ID FROM Enrollment WHERE User_ID = %s)
    """, (student_id,))
    courses = cursor.fetchall()
    db.close()
    return courses

# Function to fetch feedback for a specific test and user
def fetch_feedback(test_id, user_id):
    db = create_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT Feedback_Text FROM Feedback WHERE Test_ID = %s AND Test_ID IN (SELECT Test_ID FROM Evaluation WHERE User_ID = %s)", (test_id, user_id))
    feedback = cursor.fetchone()
    db.close()
    return feedback

# Function to fetch completed courses with their Certifications
def fetch_completed_courses_with_certificates(student_id):
    db = create_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT Course.Course_ID, Course.course_name
        FROM Course
        INNER JOIN Enrollment ON Course.Course_ID = Enrollment.Course_ID
        WHERE Enrollment.User_ID = %s AND Enrollment.course_status = 'Completed'
    """, (student_id,))
    completed_courses = cursor.fetchall()
    db.close()
    return completed_courses



def student_dashboard(user):
    st.title("Student Dashboard")
    st.write(f"Welcome, {user['Username']}!")

     # Display enrolled courses with their status (Completed or Ongoing)
    with st.expander("Enrolled Courses", expanded=False):
        enrolled_courses_with_status = fetch_enrolled_courses_with_status(user['User_ID'])
        if enrolled_courses_with_status:
            for course in enrolled_courses_with_status:
                if course['course_status'] == 'Completed':
                    st.write(f"Course Name: {course['course_name']} - Status: Completed")
                else:
                    st.write(f"Course Name: {course['course_name']} - Status: Ongoing")
        else:
            st.write("You are not enrolled in any courses.")
    # Display available courses excluding enrolled courses
    with st.expander("Available Courses", expanded=False):
        available_courses = fetch_all_courses_exclude_enrolled(user['User_ID'])
        if not available_courses:
            st.write("You are already enrolled in all available courses.")
        else:
            for course in available_courses:
                st.write(f"Course ID: {course['Course_ID']}, Course Name: {course['course_name']}")
                if st.button(f"Enroll in {course['course_name']}"):
                    # Check if the student is already enrolled
                    already_enrolled = any(ec['Course_ID'] == course['Course_ID'] for ec in enrolled_courses_with_status)

                    if not already_enrolled:
                        enroll_in_course(user['User_ID'], course['Course_ID'])
                        st.success(f"You have successfully enrolled in {course['course_name']}.")
                    else:
                        st.warning(f"You are already enrolled in {course['course_name']}.")


    # View and interact with tests
    with st.expander("Tests", expanded=False):
        enrolled_courses = fetch_enrolled_courses_with_status(user['User_ID'])
        if enrolled_courses:
            for course in enrolled_courses:
                st.subheader(f"Tests for {course['course_name']}")

                # Fetch available tests for the course
                available_tests = fetch_available_tests(user['User_ID'], course['Course_ID'])

                for test in available_tests:
                    st.write(f"Test ID: {test['Test_ID']}, Test Status: {test['Test_Status']}")
                    
                    # Display test details
                    test_details = fetch_evaluation_details(test['Test_ID'], user['User_ID'])
                    st.write(f"Test Details: {test_details['Test_Details']}")
                        
                    # Text area for submitting test response
                    test_response = st.text_area("Your Test Response:", key=f"test_response_{test['Test_ID']}")
                        
                    # Button to submit test
                    if st.button("Submit Test"):
                        submit_test(test['Test_ID'], user['User_ID'], test_response)
                        st.success("Test submitted successfully.")
                            
    # View past test grades with feedback
    with st.expander("Test Grades with Instructor Feedback", expanded=False):
        past_test_grades_with_feedback = fetch_student_test_grades_with_feedback(user['User_ID'])
        if past_test_grades_with_feedback:
            st.write("Your Test Grades with Feedback:")
            for grade in past_test_grades_with_feedback:
                st.write(f"Test ID: {grade['Test_ID']}, Test Grade: {grade['Test_Grade']}")
                if grade['Feedback_Text']:
                    st.write(f"Feedback: {grade['Feedback_Text']}")
                else:
                    st.write("No feedback available for this test.")
        else:
            st.write("You have no past test grades.")

         # Display Certifications earned for completed courses
    with st.expander("Certifications", expanded=False):
        completed_courses_with_certificates = fetch_completed_courses_with_certificates(user['User_ID'])
        if completed_courses_with_certificates:
            st.write("Certificates Earned:")
            for course in completed_courses_with_certificates:
                st.write(f"Certificate of Achievement for successfully clearing the course '{course['course_name']}'")
        else:
            st.write("You haven't completed any courses yet.")

    # Request Support
    with st.expander("Support", expanded=False):
        support_text = st.text_area("Type your support request here:", key="support_text_area")
        if st.button("Submit Request"):
            request_support(user['User_ID'], support_text)
            st.success("Support request submitted successfully.")


