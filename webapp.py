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
        "https://drive.google.com/file/d/1XONnz-t-9kSCBIvMEiDq91j5LTZ_hYHt/preview",
        "https://drive.google.com/file/d/1NnrKT5cw5p29DzVswZECBA1dJ1tdIuTI/preview"
    ),
    (
        "https://drive.google.com/file/d/1TXqTSIB_u5-a8LcJ34MtbyzyBKr6QoIR/preview",
        "https://drive.google.com/file/d/1uezSxd8NyMaiOgIoMD6MWXacEHHiDdNV/preview"
    ),
    
    (
        "https://drive.google.com/file/d/1XkTkB4Qm6lLbARprkvCv8y7xXhZHPiO0/preview",
        "https://drive.google.com/file/d/1k_0uiadUhZEGSTbX-n1th6O7rz4YW53B/preview"
    ),
    
    (
        "https://drive.google.com/file/d/1PUsjq5KCrFm949e4n17qgsjlUiqsdkAP/preview",
        "https://drive.google.com/file/d/1KsR4Y5mpMuVxoqHQnzu61MLNo0zipzj_/preview"
    ),
    
    (
        "https://drive.google.com/file/d/1DQaY8lM9xLdSns-Fi1ZNXDhUqTC91Ml1/preview",
        "https://drive.google.com/file/d/1hMjZothxu-PvlYVjV2X73v61JTNDob93/preview"
    ),
    
    (
        "https://drive.google.com/file/d/1_wRbABYz12Ep-uZ4BPHYWkbK-eG1QxC8/preview",
        "https://drive.google.com/file/d/1LnwKy4llwTLW8c_f-fvtDE5eITBab5VB/preview"
    ),
    
    (
        "https://drive.google.com/file/d/1-2zF1gw_Yc7u5SSFoOE059SpJFJ7wLsv/preview",
        "https://drive.google.com/file/d/1sYyXcA_sU2Yqdh1VypGe3zgrBxQyQU4H/preview"
    ),
    
    (
        "https://drive.google.com/file/d/1BLiu6hJPPMra_Zbv-iGpQYW5upwU2yfQ/preview",
        "https://drive.google.com/file/d/1PQSuq5T1XCEcfgWPu-23Db4wi-0I1f2R/preview"
    ),
    
     (
        "https://drive.google.com/file/d/1KU7_O8q5sYXVw5aWKQ2t6-1JoReetoTd/preview",
        "https://drive.google.com/file/d/128ZQk0CreUM6PQcov1iSQq786iXin65a/preview"
    ),
    
     (
        "https://drive.google.com/file/d/1-Hv3cQ0ZiubTwuOtwX26V0xUmppAVGqQ/preview",
        "https://drive.google.com/file/d/1e6fqQpybxKDQpVfM2prTO7abzd29dLod/preview"
    ),
    
    (
        "https://drive.google.com/file/d/1LniRcqZQ4ykOT7L75WhL9Wq66PlSVS76/preview",
        "https://drive.google.com/file/d/1a_H92cEoSukvoW4YvZjnSniQtYKxqkLS/preview"
    ),
    
    (
        "https://drive.google.com/file/d/1ApWYjiKQ4JAHwoHlBC3d0dQSp_Z6RlHQ/preview",
        "https://drive.google.com/file/d/1ydcsfslENdLHVl9Yn7_zJMOued2Lg_ZN/preview"
    ),
    
    (
        "https://drive.google.com/file/d/1hJkE4dtmZctHKpiMamWAoLeKslnm6TDd/preview",
        "https://drive.google.com/file/d/1jgtyzEICgI0zR3ahEQt17EX2dXt1hrlC/preview"
    ),
    
    (
        "https://drive.google.com/file/d/1k2MstIwtV6Lr_tXVe5Pu3UZ9uM_Lg1Bn/preview",
        "https://drive.google.com/file/d/17h-wDx06f-UtPljw_Se5hVDbD0u0259K/preview"
    ),
    
    (
        "https://drive.google.com/file/d/1RWveK2P58VE3N8rVcoQ-btuAI1rp8Tky/preview",
        "https://drive.google.com/file/d/1uBX34G0vI0UxH1cTYC6s8BsZGwTxcGQD/preview"
    ),
    
    (
        "https://drive.google.com/file/d/1LfblnfvLc_81XJeciUjngAe-iiamM4LG/preview",
        "https://drive.google.com/file/d/1ozOlUDkDonYzBSn5G0pHzscpx5txmMjv/preview"
    ),
    
    (
        "https://drive.google.com/file/d/1mRxJqCqG591reJjIXN1UyXmdaIYaAnp_/preview",
        "https://drive.google.com/file/d/1HLkbq-BbvpueaCtQx5MUgnh8lweXxdvo/preview"
    ),
    
    (
        "https://drive.google.com/file/d/1yGBg6Kep4F4tlB90TnOswoqMGgFHCzJr/preview",
        "https://drive.google.com/file/d/1RhR-PTJRkbnWa2Iuhl6ZhlQlW1MtlAMw/preview"
    ),
    
    (
        "https://drive.google.com/file/d/1qgug4w54FcZCQExXzrY2hqS9ECL7XWB8/preview",
        "https://drive.google.com/file/d/13jHuTW-KZrX5ZDelPX5pfxif5f9LfI4b/preview"
    ),
    
    (
        "https://drive.google.com/file/d/11j2ylrGceVY6SnGBUjWkT76jcWLROP-B/preview",
        "https://drive.google.com/file/d/10EMdF0qPG6Bfky54JRmKy7pR-AvBdkH-/preview"
    ),
    
    (
        "https://drive.google.com/file/d/1FoK03av-wm8nCb_k6x8jwOQmBoOdo3sv/preview",
        "https://drive.google.com/file/d/1ggOe-P-RaXz8iGmfgImkjj6oIm2nE02j/preview"
    ),
    
    (
        "https://drive.google.com/file/d/1eVFtt32IIyx-st6HvWIC9NPJiNeMGldn/preview",
        "https://drive.google.com/file/d/1KWT3ryCMrPn-1qAGAL-YRsVOftcuc-Oe/preview"
    ),
    
    (
        "https://drive.google.com/file/d/1-b8vOxa7j4ENA9_OT0S5Ibbn8aFwAABG/preview",
        "https://drive.google.com/file/d/1I4Uk4HbgxzvWKoZikao8qLPzO5dqtxN2/preview"
    ),
    
    (
        "https://drive.google.com/file/d/1cdUXGxTi7U7PhVtlpSvB3tH8Z4fPagAo/preview",
        "https://drive.google.com/file/d/1TaUz8tnBTsCpWkvNnt5Z1WWH3-6MnYqA/preview"
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
    st.markdown("<h1 style='font-weight:bold;'>Subjective Test</h1>", unsafe_allow_html=True)
    # Even bigger and bold heading for "Speaker Anonymization Assessment Test"
    st.markdown("<h2 style='font-weight:bold; font-size:1.8rem; margin-top:-10px;'>Speaker Anonymization Assessment</h2>", unsafe_allow_html=True)


    st.markdown("""
    **Subjective Test Instructions :-**
    
    - First of all please enter your email address in the box provided below.
    - For each pair of audio samples provided below, listen to the reference sample (right-hand side) and the test sample (left-hand side).
    - Please indicate "Yes" or "No" to specify whether both samples belong to the same speaker or two different speakers. If you are unsure, you may select "Can't say"; however, it is advisable to spend some additional time analyzing the samples to make your judgment as accurate as possible. If uncertainty remains, you may leave it as "Can't say".
    - Each sample has a duration ranging from 10 to 15 seconds.
 
    """)

    email = st.text_input("Please enter your email address:", key="email")

    if "answers" not in st.session_state:
        st.session_state.answers = [None] * len(audio_pairs)

    for i, (audio1_url, audio2_url) in enumerate(audio_pairs):
        st.header(f"Pair {i+1}")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<h6 style='margin-bottom: 0.2rem;'>Test Sample</h6>", unsafe_allow_html=True)
            audio1_bytes = load_audio_bytes(audio1_url)
            st.audio(audio1_bytes, format='audio/wav')
            
        with col2:
            st.markdown("<h6 style='margin-bottom: 0.2rem;'>Reference Sample</h6>", unsafe_allow_html=True)
            audio2_bytes = load_audio_bytes(audio2_url)
            st.audio(audio2_bytes, format='audio/wav')
           
        answer = st.radio(
            "Do these two audios belong to the same speaker?",
            ("Yes", "No", "Can't Say"),
            key=f"pair_{i}",
            index=(0 if st.session_state.answers[i] == "Yes" else 1 if st.session_state.answers[i] == "No" else 2 if      st.session_state.answers[i] == "Can't Say"
        else None),
            )
        st.session_state.answers[i] = answer

        st.markdown("---")

    all_answered = all(ans in ("Yes", "No", "Can't Say") for ans in st.session_state.answers)

    email_entered = email.strip() != "" and "@" in email and "." in email

    if all_answered and email_entered:
        if st.button("Submit All Responses"):
            sheet = open_sheet()
            for i, (audio1_url, audio2_url) in enumerate(audio_pairs):
                pair_id = i + 1
                row = [email, pair_id, audio1_url, audio2_url, st.session_state.answers[i]]
                sheet.append_row(row)
            st.success("All responses recorded in Google Sheets! Thank you.")
            st.session_state.answers = [None] * len(audio_pairs)
    else:
        st.info("Please answer all pairs and enter a valid email to submit.")

if __name__ == "__main__":
    main()

