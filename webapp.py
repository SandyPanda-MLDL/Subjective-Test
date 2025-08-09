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
        "https://drive.google.com/file/d/1xTdKZa5tizzf7TYs4vUwuOpc56f_P9H8/preview",
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
        "https://drive.google.com/file/d/1KWmFwTYXZP0Ya0D2BbGWOv-Zjtk7er1o/preview"
    ),
    
    (
        "https://drive.google.com/file/d/1k2MstIwtV6Lr_tXVe5Pu3UZ9uM_Lg1Bn/preview",
        "https://drive.google.com/file/d/17h-wDx06f-UtPljw_Se5hVDbD0u0259K/preview"
    ),
    
    (
        "https://drive.google.com/file/d/1cm7TyXl962Q8xe5DK7PgRW9qCXDSxE4z/preview",
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




naturalness_samples_preview = [
    "https://drive.google.com/file/d/1nuM3JhHLIVNge6pkaPAHuqxXvVitX0jW/preview",
    "https://drive.google.com/file/d/1REaYqV_VDn4_m44fe--PkHFWuyHgDwuz/preview",
    "https://drive.google.com/file/d/1WEa-vyLL6P11hgpsGtpIs1qYKcczlTCI/preview",
    "https://drive.google.com/file/d/1RSsWf9-Wc7mTBgsFdWkkJGc2pVcDpw2H/preview",
    "https://drive.google.com/file/d/1_9KbsjI9zQJK_y76aXcaiyC-hDDTup2b/preview",
    "https://drive.google.com/file/d/1ENkLvhBubT6hQ2dYzk0VHFYGhd8BaWxs/preview",
    "https://drive.google.com/file/d/1Vqs4I5-nvFXANLl7W62tr4grEKun1udZ/preview",
    "https://drive.google.com/file/d/1GGZNOdpdLfnPtleM8afftByuVJRRCSfP/preview",
    "https://drive.google.com/file/d/1wOc9lQU5q0TIcQjSXpBZUdpX8k1VQQaA/preview",
    "https://drive.google.com/file/d/1s6dAIMJJvZ_aW6XCRFeeG6AeTdzUiB5v/preview",
    "https://drive.google.com/file/d/1T2NlV1N14HZCG1YorKkpiHycwRjKU4Gq/preview",
    "https://drive.google.com/file/d/1SwJWBD1OK6U7aibcT43gDABlEox7KuxE/preview",
    "https://drive.google.com/file/d/1A4XZ1pkpvLq0IxPWQYJhFk18qxoGwWN2/preview",
    "https://drive.google.com/file/d/1TX4v03JSvqZ1Vk-ZgF8u4bwdde_9gVu8/preview",
    "https://drive.google.com/file/d/1laOtIabwMG-Hwrii1SKAniIoeiChw0b-/preview",
    "https://drive.google.com/file/d/1oVHm4UCmK15Uiikbc5m028SPdGEwdTkg/preview"
    "https://drive.google.com/file/d/1Hgrp5jcT9-kVvVxTWCCPQz1rIpH0jMgj/preview",
    "https://drive.google.com/file/d/1KQj6g1hzYqQebxXnqzNwpQZrjMbIKv0q/preview",
]


naturalness_samples = [gdrive_preview_to_direct(url) for url in naturalness_samples_preview]

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
    st.markdown("<h2 style='font-weight:bold; font-size:1.8rem; margin-top:-10px;'>Speaker Anonymization Assessment</h2>",  unsafe_allow_html=True)
    st.markdown("<h3>Subjective Test Instructions", unsafe_allow_html=True)

    st.markdown("""
    **Test-1 (Speaker Verification Test) :-**
    - (Disclaimer: The entire test should take no more than 15-20 minutes to complete.)
    - First of all please enter your email address in the box provided below.
    - It is to be noted that loading the page may take some time.
    - For each pair of audio samples provided below, listen to the reference sample (right-hand side) and the test sample (left-hand side).
    - Please remember that the test samples can be natural sample (without any modification) or modified sample (modified using some anonymization algorithm).
    - Please indicate "Yes" or "No" to specify whether both samples belong to the same speaker or two different speakers.
    - If you are unsure then spend some more time analyzing the samples, but still can't make the decision then select "Can't Say". 
    - After entering your response the page may take some time to reload again depending on your internet speed.
    - Each sample lasts 10–15 seconds but there are also some samples having duration 2-3 seconds.
    """)
    
    st.markdown("""
    **Test-2 (Naturalness and Age Group Estimation Test) :-**
    - Rate the samples based on their naturalness by giving a score between 1 to 5, where 1 means Very unnatural (sounds highly artificial) and 5 means Very natural (highest naturalness – sounds like the speech was actually produced by a human).
    - Then try to estimate the age group of the respective speakers. There are three age groups provided: 0-10 years, 11-18 years and more than 18 years. Select any of these three based on your perceptual analysis.
    - Once all responses are done (including email address) then finally press the submission button provided at the end of the page. 
    - Wait until the system confirms a successful submission. If any responses are missing, it will display a list of the unanswered items.
     """)

    email = st.text_input("Please enter your email address:", key="email")

    # ---------------- PAIRWISE TEST SECTION ----------------
    if "answers" not in st.session_state:
        st.session_state.answers = [None] * len(audio_pairs)

    st.subheader("Test 1 – Speaker Verification Test (Pairwise Test)")
    for i, (audio1_url, audio2_url) in enumerate(audio_pairs):
        st.header(f"Pair {i+1}")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Test Sample**")
            st.audio(load_audio_bytes(audio1_url), format='audio/wav')
        with col2:
            st.markdown("**Reference Sample**")
            st.audio(load_audio_bytes(audio2_url), format='audio/wav')

        st.session_state.answers[i] = st.radio(
            "Do these two audios belong to the same speaker?",
            ("Yes", "No", "Can't Say"),
            index=(
                0 if st.session_state.answers[i] == "Yes"
                else 1 if st.session_state.answers[i] == "No"
                else 2 if st.session_state.answers[i] == "Can't Say"
                else None
            ),
            key=f"pair_{i}"
        )
        st.markdown("---")

    # ---------------- NATURALNESS & AGE GROUP SECTION ----------------
    if "naturalness" not in st.session_state:
        st.session_state.naturalness = [None] * len(naturalness_samples)
    if "agegroup" not in st.session_state:
        st.session_state.agegroup = [None] * len(naturalness_samples)

    st.subheader("Test 2 – Naturalness & Age Group Estimation Test")
    st.markdown("""
    **Naturalness rating: (in a scale 1-5)**  
    1 = Very unnatural (sounds highly artificial)  
    5 = Very natural (highest naturalness – sounds like the speech is actually produced by a human)  
    """)

    for i, audio_url in enumerate(naturalness_samples):
        st.header(f"Sample {i+1}")
        st.audio(load_audio_bytes(audio_url), format='audio/wav')

        st.session_state.naturalness[i] = st.slider(
            "Rate the naturalness",
            1, 5,
            value=st.session_state.naturalness[i] if st.session_state.naturalness[i] else 3,
            key=f"nat_{i}"
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

    # ---------------- SUBMISSION ----------------
    if st.button("Submit All Responses"):
        missing_info = []

        # Check email
        if email.strip() == "":
            missing_info.append("Email address is missing")
        elif "@" not in email or "." not in email:
            missing_info.append("Invalid email address format")

        # Check unanswered pairwise
        unanswered_pairs = [i+1 for i, ans in enumerate(st.session_state.answers) if ans not in ("Yes", "No", "Can't Say")]
        if unanswered_pairs:
            missing_info.append(f"Unanswered pairs: {', '.join(map(str, unanswered_pairs))}")

        # Check unanswered naturalness/age
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
            # Save pairwise
            for i, (audio1_url, audio2_url) in enumerate(audio_pairs):
                row = [email, f"Pair_{i+1}", audio1_url, audio2_url, st.session_state.answers[i], "", ""]
                sheet.append_row(row)
            # Save naturalness/age
            for i, audio_url in enumerate(naturalness_samples):
                row = [email, f"Sample_{i+1}", audio_url, "", "", st.session_state.naturalness[i], st.session_state.agegroup[i]]
                sheet.append_row(row)

            st.success("✅ All responses recorded in Google Sheets! Thank you.")
            st.session_state.answers = [None] * len(audio_pairs)
            st.session_state.naturalness = [None] * len(naturalness_samples)
            st.session_state.agegroup = [None] * len(naturalness_samples)

if __name__ == "__main__":
    main()



