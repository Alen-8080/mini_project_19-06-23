import csv
import re
import streamlit as st

def validate_inputs(username, password, user_type, branch, semester, college, phone_no):
    # Check if any required field is empty
    if not username or not password or not user_type or not branch or not semester or not college or not phone_no:
        return False

    # Check if password has at least 6 characters
    if len(password) < 6:
        return False

    # Check if password contains at least one number
    if not re.search(r'\d', password):
        return False

    return True

def save_to_csv(username, password, user_type, branch, semester, college, phone_no):
    with open('data.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([username, password, user_type, branch, semester, college, phone_no])

def signup():
    st.empty()

    css = """
    .container {
        max-width: 400px;
        margin: 0 auto;
        padding: 20px;
        background-color: #ffffff;
        border-radius: 5px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    }

    h2 {
        text-align: center;
        color: #333333;
    }

    label {
        display: block;
        margin-bottom: 10px;
        color: #555555;
    }

    input[type="text"],
    input[type="submit"] {
        width: 100%;
        padding: 10px;
        font-size: 16px;
        border-radius: 3px;
        border: 1px solid #dddddd;
    }

    input[type="submit"] {
        background-color: #4CAF50;
        color: #ffffff;
        cursor: pointer;
    }

    .error {
        color: #ff0000;
        margin-top: 10px;
    }
    """

    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

    st.markdown("<h2>Chatbot Registration</h2>", unsafe_allow_html=True)
    with st.form("signup_form"):
        username = st.text_input("Name:")
        password = st.text_input("Password", type="password")
        user_type = st.selectbox("Type", ["Student", "Teacher"])
        branch = st.text_input("Branch")
        semester = st.text_input("Semester")
        college = st.text_input("College")
        phone_no = st.text_input("Phone Number")
        
        form_reset = st.form_submit_button("Reset")
        if form_reset:
            # Reset the form fields if the "Reset" button is clicked
            username = ""
            password = ""
            user_type = ""
            branch = ""
            semester = ""
            college = ""
            phone_no = ""
            
        if st.form_submit_button("Sign Up Now"):
            if validate_inputs(username, password, user_type, branch, semester, college, phone_no):
                save_to_csv(username, password, user_type, branch, semester, college, phone_no)
                st.success("Sign up successful!")
                return True
            else:
                st.error("Please fill in all the required fields or ensure the password has at least 6 characters and one number.")

    return False

def main():
    st.set_page_config(page_title="Login and Chat Example",
                        layout="centered",
                        initial_sidebar_state="auto")

    if not st.session_state.login_status:
        st.title("Login Page")
        username = st.text_input("Username:")
        password = st.text_input("Password:", type="password")
        button_clicked = st.button("Login")

        if button_clicked:
            # Add your authentication logic here
            # If authentication is successful, set the login status to True
            if username == "admin" and password == "password":
                st.session_state.login_status = True
            else:
                st.error("Invalid username or password. Please try again.")

        st.markdown("Don't have an account? [Sign up now](signup)")

    else:
        st.title("Welcome to the Chatbot")
        st.write("You are logged in.")

if __name__ == "__main__":
    main()
