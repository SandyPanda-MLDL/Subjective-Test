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

SPREADSHEET_NAME = "SubjectiveTestResults"  # Your Google Sheet name

# Authenticate Google Sheets client from Streamlit secrets
@st.cache_resource(ttl=3600)
def get_gsheet_client():
    creds_json_str = st.secrets["GS_CREDS_JSON"]  # get the JSON string from secrets
    creds_dict = json.loads(creds_json_str)       # parse JSON string to dict
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
        return url  # fallback if no match

# Replace with your actual public preview links
audio_pairs_preview = [
    (
        "https://drive.google.com/file/d/1NnrKT5cw5p29DzVswZECBA1dJ1tdIuTI/preview",
        "https://drive.google.com/file/d/1-sALpb42wFD5ce8ne1d3gO-IC-djOjgv/preview"
    ),
]

# Convert preview URLs to direct download URLs
audio_pairs = [
    (gdrive_preview_to_direct(a1), gdrive_preview_to_direct(a2))
    for a1, a2 in audio_pairs_preview
]

def load_audio_bytes(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.content

def main():
    st.title("Same Speaker Subjective Test")

    email = st.text_input("Please enter your email address:", key="email")

    if "answers" not in st.session_state:
        st.session_state.answers = [None] * len(audio_pairs)

    for i, (audio1_url, audio2_url) in enumerate(audio_pairs):
        st.header(f"Pair {i+1}")

        col1, col2 = st.columns(2)
        with col1:
            audio1_bytes = load_audio_bytes(audio1_url)
            st.audio(audio1_bytes, format='audio/wav')
            st.write(f"Audio 1 URL: {audio1_url}")
        with col2:
            audio2_bytes = load_audio_bytes(audio2_url)
            st.audio(audio2_bytes, format='audio/wav')
            st.write(f"Audio 2 URL: {audio2_url}")

        answer = st.radio(
            "Do these two audios belong to the same speaker?",
            ("Yes", "No"),
            key=f"pair_{i}",
            index=0 if st.session_state.answers[i] == "Yes" else 1 if st.session_state.answers[i] == "No" else None
        )
        st.session_state.answers[i] = answer

        st.markdown("---")

    all_answered = all(ans in ("Yes", "No") for ans in st.session_state.answers)
    email_entered = email.strip() != "" and "@" in email and "." in email

    if all_answered and email_entered:
        if st.button("Submit All Responses"):
            sheet = open_sheet()
            for i, (audio1_url, audio2_url) in enumerate(audio_pairs):
                row = [email, audio1_url, audio2_url, st.session_state.answers[i]]
                sheet.append_row(row)
            st.success("All responses recorded in Google Sheets! Thank you.")
            st.session_state.answers = [None] * len(audio_pairs)
    else:
        st.info("Please answer all pairs and enter a valid email to submit.")

if __name__ == "__main__":
    main()

