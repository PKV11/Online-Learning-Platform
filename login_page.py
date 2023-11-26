import streamlit as st
from database import create_connection
# Streamlit UI for user login
def user_login():
    st.title("User Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    account_type = st.selectbox("Select User Role", ["student", "instructor", "administrator"])

    if st.button("Login"):
        user = check_credentials(username, password, account_type)
        if user:
             # Clear the current page (login page)
            st.empty()
            '''if user['Account_Type'] == 'student':
                student_dashboard(user)
            elif user['Account_Type'] == 'instructor':
                instructor_dashboard(user)
            elif user['Account_Type'] == 'administrator':
                admin_dashboard(user)'''
            st.session_state.is_logged_in = True
            st.session_state.user_type = user['Account_Type']
            st.session_state.user = user
        else:
            st.error("Login failed. Please check your credentials.")

# Function to check user credentials
def check_credentials(username, password, account_type):
    db = create_connection()
    cursor = db.cursor(dictionary=True)
    if account_type == 'student':
        cursor.execute("SELECT U.User_ID,U.Username, U.Password, A.Account_Type FROM User U INNER JOIN Account A ON U.User_ID = A.User_ID WHERE U.Username = %s", (username,))
    elif account_type == 'administrator':
        cursor.execute("SELECT U.Admin_ID,U.Admin_Name, U.Password, A.Account_Type FROM Admin U INNER JOIN Account A ON U.Admin_ID = A.Admin_ID WHERE U.Admin_Name = %s", (username,))
    elif account_type == 'instructor':
        cursor.execute("SELECT U.Instructor_ID,U.Instructor_Name, U.Password, A.Account_Type FROM Instructor U INNER JOIN Account A ON U.Instructor_ID = A.Instructor_ID WHERE U.Instructor_Name = %s", (username,))
    user = cursor.fetchone()
    db.close()
    if user and user['Password'] == password and user['Account_Type'] == account_type:
        return user
    return None
