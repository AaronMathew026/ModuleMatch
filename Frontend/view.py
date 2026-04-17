import streamlit as st
import json
import requests
import time
import os

BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")

st.set_page_config(page_title="Module Match", page_icon="🎓", layout="wide")

st.title("🎓 Module Match")
st.markdown("Discover the perfect modules tailored to your academic journey and career aspirations.")

st.divider()

st.header("👤 1. Profile Information")
st.info("Tell us a bit about yourself so we can personalize your module recommendations.")

with st.form("profile_form", border=True):
    col1, col2, col3 = st.columns([2, 2, 1]) 
    
    with col1:
        name = st.text_input("Full Name", placeholder="e.g., Alex Johnson")
    with col2:
        course = st.text_input("Current Course", placeholder="e.g., BSc Computer Science")
    with col3:
        year = st.number_input("Year of Study", min_value=1, max_value=5, step=1)
        
    col4, col5 = st.columns(2)
    
    with col4:
        interests = st.text_area(
            "Academic Interests", 
            placeholder="e.g., Artificial Intelligence, Data Ethics, Web Development", 
            help="Separate your interests with commas."
        )
    with col5:
        goals = st.text_area(
            "Career Goals", 
            placeholder="e.g., I want to become a Machine Learning Engineer..."
        )
        
    uploaded_file = st.file_uploader("Upload Your CV", type=["pdf"])
    
    if uploaded_file is not None:
        st.success("CV attached successfully!", icon="✅")

    submitted = st.form_submit_button("Submit Profile", type="primary", use_container_width=True)

if submitted:
    if not name or not course:
        st.warning("Please fill in your Name and Course before submitting.", icon="⚠️")
    elif not uploaded_file:
        st.warning("Please upload your CV before submitting.", icon="⚠️")
    else:
        profile_dict = {
            "name": name,
            "year": year,
            "course": course,
            "interests": [i.strip() for i in interests.split(",") if i.strip()], 
            "goals": goals
        }

        profile_json = json.dumps(profile_dict, indent=4)
        payload_data = {"profile": profile_json}
        payload_files = {"cv_pdf": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}

        st.divider()
        st.subheader("⚙️ Processing Application")
        
        progress_text = st.empty()
        progress_bar = st.progress(0)

        try:
            progress_text.info("Uploading data payload... (10%)")
            progress_bar.progress(10)
            time.sleep(0.5)
            
            progress_text.info("Summarizing CV & Larping... (67%)")
            progress_bar.progress(67)
            
            response = requests.post(
                f"{BACKEND_URL}/submit-profile/",
                data=payload_data,
                files=payload_files
            )
            
            progress_text.info("Finalizing recommendations (W Speed)... (89%)")
            progress_bar.progress(89)
            time.sleep(0.5)
            
            progress_text.empty()
            progress_bar.empty()
            
            if response.status_code == 200:
                st.success(f"Welcome, {name}! Here are your module recommendations:", icon="✅")
                
                with st.container(border=True):
                    recommendations = response.json().get("data", "No recommendations found.")
                    st.markdown(recommendations)
                
            elif response.status_code == 422:
                st.error("There was an error with your submission. Please check your profile information and CV format.", icon="❌")
                
            else:
                st.error(f"Unexpected error: {response.status_code}. Please try again later.", icon="❌")
                
        except requests.exceptions.ConnectionError:
            progress_text.empty()
            progress_bar.empty()
            st.error("Could not connect to the backend server. Please ensure it's running and try again.", icon="❌")

st.divider()