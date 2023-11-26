import streamlit as st
from database import create_connection
# Streamlit UI for user registration
def user_registration():
    st.subheader("Student Registration")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    

    if st.button("Register"):
        account_type = "student"
        db = create_connection()
        cursor = db.cursor()
        cursor.execute("INSERT INTO User (Username, Password) VALUES (%s, %s)", (username, password))
        user_id = cursor.lastrowid
        cursor.execute("INSERT INTO Account (User_ID, Account_Type) VALUES (%s, %s)", (user_id, account_type))
        db.commit()
        cursor.close()
        db.close()
        st.success("Student registered successfully.")
