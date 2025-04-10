import streamlit as st
import pandas as pd
import json

# File paths
NAMES_FILE = "names.json"
TRACKER_FILE = "tracker_data.csv"

# Load names from JSON
def load_names():
    try:
        with open(NAMES_FILE, "r") as f:
            data = json.load(f)
        return data.get("names", [])
    except FileNotFoundError:
        return []

# Define the case study schedule based on the document
schedule = [
    ("April 14", "Project Onboarding & Setup"),
    ("April 15", "Data Ingestion & Preprocessing"),
    ("April 16", "Exploratory Data Analysis"),
    ("April 17", "Feature Engineering (RFM)"),
    ("April 18", "Cohort Segmentation"),
    ("April 21", "Retention Analysis"),
    ("April 22", "Churn Analysis"),
    ("April 23", "CLV Modeling (Probabilistic)"),
    ("April 24", "CLV Modeling (ML)"),
    ("April 25", "Clustering & Final Reporting")
]

# Load tracker data
def load_tracker_data(name):
    try:
        tracker_data = pd.read_csv(TRACKER_FILE)
    except FileNotFoundError:
        tracker_data = pd.DataFrame(columns=["Name", "Date", "Theme", "Completed", "Comments"])
    
    # Filter data for the selected name
    user_data = tracker_data[tracker_data["Name"] == name].copy()
    
    # If user data is empty, create new rows
    if user_data.empty:
        user_data = pd.DataFrame([{
            "Name": name,
            "Date": date,
            "Theme": theme,
            "Completed": False,
            "Comments": ""
        } for date, theme in schedule])
    else:
        # Ensure all dates from the schedule are present
        existing_dates = user_data["Date"].tolist()
        for date, theme in schedule:
            if date not in existing_dates:
                new_row = pd.DataFrame([{
                    "Name": name,
                    "Date": date,
                    "Theme": theme,
                    "Completed": False,
                    "Comments": ""
                }])
                user_data = pd.concat([user_data, new_row], ignore_index=True)
                
    user_data.set_index("Date", inplace=True)
    return user_data

# Save tracker data
def save_tracker_data(user_data):
    user_data = user_data.reset_index()
    try:
        existing_tracker = pd.read_csv(TRACKER_FILE)
    except FileNotFoundError:
        existing_tracker = pd.DataFrame(columns=["Name", "Date", "Theme", "Completed", "Comments"])
        
    # Filter out old entries for the user
    existing_tracker = existing_tracker[existing_tracker["Name"] != user_data["Name"].iloc[0]]
    
    # Append the updated user data
    updated_tracker = pd.concat([existing_tracker, user_data], ignore_index=True)
    updated_tracker.to_csv(TRACKER_FILE, index=False)

# Load names
names = load_names()

# Name selection
selected_name = st.selectbox("Select your name", names)

# Load user data
user_data = load_tracker_data(selected_name)

# Editable DataFrame
edited_data = st.data_editor(
    user_data,
    column_config={
        "Completed": st.column_config.CheckboxColumn(
            "Completed",
            default=False,
        ),
        "Theme": st.column_config.TextColumn("Theme", disabled=True)
    },
    disabled=["Date"],
    use_container_width=True
)

# Save button
if st.button("Save Progress"):
    save_tracker_data(edited_data.copy())
    st.success("Progress saved!")

# Instructions
st.markdown("""
### Instructions:
1.  **Select Your Name**: Choose your name from the dropdown.
2.  **Track Progress**: Use the checkbox to mark tasks as completed.
3.  **Add Comments**: Provide any comments or blockers in the comments section.
4.  **Save**: Click the 'Save Progress' button to save your updates.
""")




