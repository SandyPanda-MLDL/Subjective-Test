import json
import requests
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# Google Sheets setup
SCOPE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]
SPREADSHEET_NAME = "SubjectiveTestResults"

# Authenticate Google Sheets client from Streamlit secrets
@st.cache_resource(ttl=3600)
def get_gsheet_client():
    creds_json_str = st.secrets["GS_CREDS_JSON"]
    creds_dict = json.loads(creds_json_str)
    creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPE)
    client = gspread.authorize(creds)
    return client

def open_sheet():
    client = get_gsheet_client()
    sheet = client.open(SPREADSHEET_NAME).sheet1
    return sheet

# Utility to convert Google Drive preview URL to direct download URL
def gdrive_preview_to_direct(url):
    import re
    match = re.search(r'/d/([a-zA-Z0-9_-]+)', url)
    if match:
        file_id = match.group(1)
        return f"https://drive.google.com/uc?export=download&id={file_id}"
    else:
        return url

# Naturalness sample URLs
naturalness_samples_preview = [
    "https://drive.google.com/file/d/1nwytw1t-PUvUHIHKsMjjT6eZWBc117PI/preview",
    "https://drive.google.com/file/d/1REaYqV_VDn4_m44fe--PkHFWuyHgDwuz/preview",
    "https://drive.google.com/file/d/1trvIsvNTID-VXSui6syhlIEvGraNReKz/preview",
    "https://drive.google.com/file/d/1RSsWf9-Wc7mTBgsFdWkkJGc2pVcDpw2H/preview",
    "https://drive.google.com/file/d/1e-AnCoiNM6txlL8ZFCpBTn6S6EfGDpQ-/preview",
    "https://drive.google.com/file/d/1ENkLvhBubT6hQ2dYzk0VHFYGhd8BaWxs/preview",
    "https://drive.google.com/file/d/1H4h6zIMOxeQeUPDkx-8MPxXwQlrZ56WO/preview",
    "https://drive.google.com/file/d/1GGZNOdpdLfnPtleM8afftByuVJRRCSfP/preview",
    "https://drive.google.com/file/d/1UQnZNmQhV-7IrjxgV8Gs06qQjIKQy_79/preview",
    "https://drive.google.com/file/d/1s6dAIMJJvZ_aW6XCRFeeG6AeTdzUiB5v/preview",
    "https://drive.google.com/file/d/1fi_9ZaO5VtDpoT8jwe6_3WZXnQLKZIUN/preview",
    "https://drive.google.com/file/d/1SwJWBD1OK6U7aibcT43gDABlEox7KuxE/preview",
    "https://drive.google.com/file/d/10Z0BGxnXgT6rw5AY-s2TwzzQ4ToA1Vzb/preview",
    "https://drive.google.com/file/d/1TX4v03JSvqZ1Vk-ZgF8u4bwdde_9gVu8/preview",
    "https://drive.google.com/file/d/1uqgv1r5wNWzqkSFBzsW4Tg3EqgVjVhV9/preview",
    "https://drive.google.com/file/d/1oVHm4UCmK15Uiikbc5m028SPdGEwdTkg/preview",
    "https://drive.google.com/file/d/1Manh3kGFELRKMLH1f8SBVjm-Zk6gva_w/preview",
    "https://drive.google.com/file/d/1KQj6g1hzYqQebxXnqzNwpQZrjMbIKv0q/preview",
]

# Convert to direct download links
naturalness_samples = [gdrive_preview_to_direct(url) for url in naturalness_samples_preview]

def load_audio_bytes(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.content

def main():
    st.markdown("<h1 style='font-weight:bold;'>Subjective Test</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='font-weight:bold; font-size:1.8rem; margin-top:-10px;'>Speaker Naturalness and Age Group Estimation Test</h2>", unsafe_allow_html=True)
    
    st.markdown("""
    **(Naturalness and Age Group Estimation Test) :-**
    - **Rate the samples based on their naturalness by giving a score between 1 to 5, where 1 means Very unnatural and 5 means Very natural.**
    - **Then estimate the age group: 0-10 years, 11-18 years, or More than 18 years.**
    - Enter your email address before submission.
    - Press "Submit All Responses" after completing all items.
    """, unsafe_allow_html=True)

    email = st.text_input("Please enter your email address:", key="email")

    if "naturalness" not in st.session_state:
        st.session_state.naturalness = [None] * len(naturalness_samples)
    if "agegroup" not in st.session_state:
        st.session_state.agegroup = [None] * len(naturalness_samples)

    st.subheader("Naturalness & Age Group Estimation Test")

    for i, audio_url in enumerate(naturalness_samples):
        st.header(f"Sample {i+1}")
        st.audio(load_audio_bytes(audio_url), format='audio/wav')

        # Slider with labels inside
        slider_label = "<div style='display:flex; justify-content:space-between;'><span>1 = Very unnatural</span><span>5 = Very natural</span></div>"
        st.markdown(slider_label, unsafe_allow_html=True)

        st.session_state.naturalness[i] = st.slider(
            "",
            min_value=1,
            max_value=5,
            value=st.session_state.naturalness[i] if st.session_state.naturalness[i] else 3,
            step=1,
            key=f"nat_{i}",
            label_visibility="collapsed"
        )

        st.session_state.agegroup[i] = st.selectbox(
            "Select the perceived age group",
            ["0–10 years", "11–18 years", "More than 18 years"],
            index=(
                ["0–10 years", "11–18 years", "More than 18 years"].index(st.session_state.agegroup[i])
                if st.session_state.agegroup[i] in ["0–10 years", "11–18 years", "More than 18 years"]
                else 2
            ),
            key=f"age_{i}"
        )
        st.markdown("---")

    if st.button("Submit All Responses"):
        missing_info = []

        if email.strip() == "":
            missing_info.append("Email address is missing")
        elif "@" not in email or "." not in email:
            missing_info.append("Invalid email address format")

        unanswered_nat = [i+1 for i, val in enumerate(st.session_state.naturalness) if val is None]
        unanswered_age = [i+1 for i, val in enumerate(st.session_state.agegroup) if val is None]
        if unanswered_nat:
            missing_info.append(f"Missing naturalness ratings: {', '.join(map(str, unanswered_nat))}")
        if unanswered_age:
            missing_info.append(f"Missing age group selections: {', '.join(map(str, unanswered_age))}")

        if missing_info:
            st.error("Please check the following before submitting:\n- " + "\n- ".join(missing_info))
        else:
            sheet = open_sheet()
            for i, audio_url in enumerate(naturalness_samples):
                row = [email, f"Sample_{i+1}", audio_url, "", "", st.session_state.naturalness[i], st.session_state.agegroup[i]]
                sheet.append_row(row)

            st.success("✅ All responses recorded in Google Sheets! Thank you.")
            st.session_state.naturalness = [None] * len(naturalness_samples)
            st.session_state.agegroup = [None] * len(naturalness_samples)


if __name__ == "__main__":
    main()

