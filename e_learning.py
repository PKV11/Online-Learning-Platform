import streamlit as st
import mysql.connector
from login_page import user_login
from register_page import user_registration
from database import create_tables, create_connection
from student_dashboard import student_dashboard
from admin_dashboard import admin_dashboard
from instructor_dashboard import instructor_dashboard
import pandas as pd


# Custom theme
custom_css = """
<style>
body {
    background-color: #f0f0f0;
    font-family: 'Arial', sans-serif;
    color: #333;
}
</style>
"""

# Apply custom theme
st.markdown(custom_css, unsafe_allow_html=True)
# Function to execute SQL queries
def execute_query(query):
    try:
        db = create_connection()  # Establish a connection to your database
        cursor = db.cursor(dictionary=True)
        
        cursor.execute(query)  # Execute the provided query
        result = cursor.fetchall()  # Fetch the result
        
        db.close()  # Close the database connection
        return result  # Return the query result
        
    except mysql.connector.Error as err:
        return f"Error occurred: {err}"  # Display error message if there's an issue

# Main function to create tables
def main():
    st.title("E-Learning")
    db = create_connection()
    create_tables(db)

    # Check if the user is logged in
    is_logged_in = st.session_state.is_logged_in if 'is_logged_in' in st.session_state else False
    if is_logged_in:
        # User is logged in, display the dashboard and logout option
        if st.session_state.user_type == 'student':
            student_dashboard(st.session_state.user)
        elif st.session_state.user_type == 'instructor':
            instructor_dashboard(st.session_state.user)
        elif st.session_state.user_type == 'administrator':
            admin_dashboard(st.session_state.user)
         # Logout button
        if st.button("Logout"):
            st.session_state.is_logged_in = False
    else:
        option = st.sidebar.selectbox("Register/Login", ["Student Registration", "User Login"])
        if option == "Student Registration":
            user_registration()
        elif option == "User Login":
            user_login()
            
    
     # Section for SQL query execution(Just used for reference from frontend)
    st.sidebar.title("SQL Query Executor")
    query = st.sidebar.text_area("Enter SQL Query:")
    
    if st.sidebar.button("Execute Query"):
        if query:
            query_result = execute_query(query)
            
            # Display query result as a table
            if isinstance(query_result, str):  
                st.error(query_result) 
            else:
                if query_result: 
                    df = pd.DataFrame(query_result)  
                    st.write("Query Result:")
                    st.table(df) 
                else:
                    st.info("Query executed successfully, but no results returned.")
        else:
            st.warning("Please enter an SQL query.")

    db.close()

if __name__ == '__main__':
    main()
