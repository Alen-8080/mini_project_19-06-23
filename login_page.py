import streamlit as st

def login_page():
    st.markdown(
        """
        <!DOCTYPE html>
        <html>
        <head>
          <link rel="stylesheet" href="{{ url_for('static', filename='style_login.css') }}">
        </head>
        <body>
          <div class="container">
            <img src="{{ url_for('static', filename='/home/alen/Desktop/llm_model/static/ktu-logo(1).png') }}" alt="KTU Logo" class="logo">
            <h1 class="title">Welcome to the KTU Chatbot</h1>
            <form id="login-form">
              <input type="text" name="username" id="username" class="input" placeholder="Enter your username" required>
              <br>
              <input type="password" name="password" id="password" class="input" placeholder="Enter your password" required>
              <br>
              <input type="submit" value="Login" class="button">
            </form>
            <p id="error" class="error"></p>
          </div>
          <script src="{{ url_for('static', filename='script_login.js') }}"></script>
        </body>
        </html>
        """
    )
