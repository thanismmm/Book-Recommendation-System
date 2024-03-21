import streamlit as st
import subprocess

def login(username, password):
    # Replace this with your own logic to verify the user's credentials
    if username == 'admin' and password == '123':
        return True
    else:
        return False

# Create the login form
st.title('Welcome Back!')
username = st.text_input('Username')
password = st.text_input('Password', type='password')

if st.button('Login'):
    if login(username, password):
        st.success('Login successful!')
        # Call your app.py file here
        subprocess.run(['streamlit', 'run', 'app.py'])  # Use 'streamlit run' instead of 'python'
    else:
        st.error('Invalid username or password')
