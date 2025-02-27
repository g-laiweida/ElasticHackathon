# app.py (Streamlit UI)
import streamlit as st
import re
from backend import find_relevant_category, find_relevant_news_genre, find_news_articles_by_genre
# Dummy credentials (you can replace this with actual user data or a database)
USER_CREDENTIALS = {"user1": "password123", "user2": "mypassword", "user3": "admin123"}

# Function to extract the numeric part of the username
def extract_user_id(username):
    match = re.search(r'\d+', username)  # \d+ matches one or more digits
    if match:
        return int(match.group())  # Return the number as integer
    else:
        return None  # Return None if no number is found


# Function to validate login
def check_login(username, password):
    if username in USER_CREDENTIALS:
        return True
    return False

# Login page
def login_page():# Display the image (logo or placeholder)
    image_url = "https://cdn.freelogovectors.net/wp-content/uploads/2019/02/OCBC-bank-logo.png"  # Replace with your image URL
    st.image(image_url, use_container_width=True)
    st.title("Welcome to OCBC")

    # Input fields for username and password
    username = st.text_input("Username", "")
    password = st.text_input("Password", "", type="password")

    # Login button
    if st.button("Login"):
        if check_login(username, password):
            st.session_state.logged_in = True  # Set session state to logged in
            st.session_state.user_id = extract_user_id(username)  # Save user_id to session
            st.session_state.login_success = True  # Flag successful login
            st.success("Login successful!")
            
        else:
            st.session_state.login_success = False  # Invalid login flag
            st.error("Invalid username or password. Please try again.")

# Logout Page
def logout_page():
    st.title("Logout Page")
    st.write("You have been logged out successfully.")
    st.write("Click below to return to the login page.")
    
    if st.button("Go to Login Page"):
        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.login_success = False
        st.session_state.logged_out = False


# Define the sidebar only for the main screen
def sidebar_navigation():

    # Dummy content in the sidebar
    st.sidebar.markdown("### News for you")
    st.sidebar.markdown("### Transactions")
    st.sidebar.markdown("### Account details")
    st.sidebar.markdown("### Contact us")

    # Logout Button
    if st.sidebar.button("Logout"):
        logout()

# Logout Function
def logout():
    # Reset the session state variables
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.login_success = False

    # Redirect to logout page
    st.session_state.logged_out = True
   
    
# Main screen (News Recommendation System)
def main_screen():
    # Assuming functions like 'find_relevant_category', 'find_relevant_news_genre', 
    # 'find_news_articles_by_genre' are defined elsewhere in the backend
     # Show the sidebar navigation on the main screen
    user_id = st.session_state.user_id  # Get the user_id from session state

    # Display the image (logo or placeholder)
    image_url = "https://cdn.freelogovectors.net/wp-content/uploads/2019/02/OCBC-bank-logo.png"  # Replace with your image URL
    st.image(image_url, use_container_width=True)

    # Streamlit UI Title
    st.title("News Article Recommendations")

    # Display a welcome message
    st.write(f"Click to generate news just for you!")

    # A button to trigger the recommendation process
    if st.button('Get Recommendations'):
        st.write(f"Fetching recommendations for You...")

        # Fetch relevant category
        relevant_category = find_relevant_category(user_id)

        if relevant_category:
            st.write(f"You are mostly interested in: {relevant_category}")

            # Fetch relevant news genre
            relevant_genre = find_relevant_news_genre(relevant_category)

            if relevant_genre:
                st.write(f"This is your reccomended genre of news: {relevant_genre}")

                # Fetch and display the recommended news articles
                news_articles = find_news_articles_by_genre(relevant_genre)
                st.write(f"News Articles for Genre '{relevant_genre}':")

                if news_articles:
                    for article in news_articles:
                        st.write(f" - {article['message']}")
                else:
                    st.write("No articles found for this genre.")
            else:
                st.write("No relevant genre found for the selected category.")
        else:
            st.write("No relevant category found for the provided User ID.")

# Main Flow of the App
def main():
    # Check if the user is logged out
    if 'logged_out' in st.session_state and st.session_state.logged_out:
        logout_page()  # Show logout page when logged out
    elif 'logged_in' in st.session_state and st.session_state.logged_in:
        sidebar_navigation()  # Show the sidebar with logout button
        main_screen()  # Show the main screen with content
    else:
        login_page()  # Show the login page without the sidebar

# Run the main function
if __name__ == "__main__":
    main()

