import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

def signup(username, password):
    try:
        existing_df = pd.read_excel("login.xlsx")
        new_df = pd.DataFrame({"Username": [username], "Password": [password], "Signup Date": [datetime.now()]})
        updated_df = pd.concat([existing_df, new_df], ignore_index=True)
        updated_df.to_excel("login.xlsx", index=False)
    except FileNotFoundError:
        df = pd.DataFrame({"Username": [username], "Password": [password], "Signup Date": [datetime.now()]})
        df.to_excel("login.xlsx", index=False)


def login(username, password):
    df = pd.read_excel("login.xlsx")
    if (df["Username"] == username).any():
        user_row = df[df["Username"] == username]
        if (user_row["Password"] == password).any():
            return True
    return False

def add_event(event_name, event_date, event_time):
    event_datetime = datetime.combine(event_date, event_time)
    current_datetime = datetime.now()
    countdown_timedelta = event_datetime - current_datetime
    remaining_days = countdown_timedelta.days
    remaining_seconds = countdown_timedelta.seconds
    remaining_hours = remaining_seconds // 3600
    remaining_minutes = (remaining_seconds % 3600) // 60
    remaining_seconds %= 60
    if remaining_days < 0:
        remainder_message = f"It's time for {event_name}!"
    else:
        remainder_message = f"Remaining time: {remaining_days} days, {remaining_hours} hours, {remaining_minutes} minutes, {remaining_seconds} seconds."
    df = pd.DataFrame({"Event Name": [event_name], "Event Date": [event_date], "Event Time": [event_time], "Countdown": [remainder_message]})
    try:
        existing_df = pd.read_excel("data.xlsx")
        updated_df = pd.concat([existing_df, df], ignore_index=True)
    except FileNotFoundError:
        updated_df = df
    updated_df.to_excel("data.xlsx", index=False)
    st.session_state.event_data_exists = True
    st.session_state.latest_event = df  # Store the latest event details

def main():
    st.title("Event Countdown App")
    
    # Check if user is already logged in
    if st.session_state.logged_in:
        st.write("Welcome back!")
        # Display main page content here
    else:
        st.write("Welcome to the Event Countdown App! Please log in or sign up.")
        page = st.radio("Select an option:", ("Login", "Signup"))

        if page == "Login":
            username = st.text_input("Username:")
            password = st.text_input("Password:", type="password")
            if st.button("Login"):
                if login(username, password):
                    st.session_state.logged_in = True
                    st.success("Login successful!")
                else:
                    st.error("Invalid username or password.")

        elif page == "Signup":
            username = st.text_input("Create Username:")
            password = st.text_input("Create Password:", type="password")
            confirm_password = st.text_input("Confirm Password:", type="password")
            if st.button("Signup"):
                if password == confirm_password:
                    signup(username, password)
                    st.success("Signup successful! Please log in.")
                else:
                    st.error("Passwords do not match.")

    if st.session_state.logged_in:
        st.write("Enter event details:")
        event_name = st.text_input("Event Name:")
        event_date = st.date_input("Event Date:")
        event_time = st.text_input("Event Time (HH:MM):")
        if st.button("Add Event"):
            event_time = datetime.strptime(event_time, "%H:%M").time()
            add_event(event_name, event_date, event_time)
            st.success("Event added successfully!")

        if st.button("View All Events"):
            view_all_events()

        if st.session_state.event_data_exists and "latest_event" in st.session_state:
            st.write("Current Event Details:")
            latest_event = st.session_state.latest_event
            st.write(f"Event: {latest_event['Event Name'].iloc[0]}, Date: {latest_event['Event Date'].iloc[0]}, Time: {latest_event['Event Time'].iloc[0]}")
            if "It's time for" in latest_event['Countdown'].iloc[0]:
                st.warning(latest_event['Countdown'].iloc[0])
            else:
                st.write(f"Countdown: {latest_event['Countdown'].iloc[0]}")

def view_all_events():
    df = pd.read_excel("data.xlsx")
    st.write(df)

if __name__ == "__main__":
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "event_data_exists" not in st.session_state:
        st.session_state.event_data_exists = False
    main()
