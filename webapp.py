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

def gdrive_preview_to_direct(url):
    import re
    match = re.search(r'/d/([a-zA-Z0-9_-]+)', url)
    if match:
        file_id = match.group(1)
        return f"https://drive.google.com/uc?export=download&id={file_id}"
    else:
        return url

def load_audio_bytes(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.content

# -------------------------
# Your audio file structure
# -------------------------
# Example: Each set is [reference, test1, test2, test3]
# Replace these with your real Google Drive preview links

sets_preview = [
    [
        "https://drive.google.com/file/d/1PktD0Wjsaryk4QdugY_esP19PNnOgt9G/preview",
        "https://drive.google.com/file/d/1Nwry4T-8w99GN0s7R2_1xqRT49FckLj1/preview",
        "https://drive.google.com/file/d/1lbEyPt062AaUvnMn1VFw0QgRfgO36S8S/preview",
        "https://drive.google.com/file/d/1EpZdO4tQSZLjWnh28LFCgusZheog_U1X/preview"
    ],
    [
        "https://drive.google.com/file/d/1IM1flhHJlUZSb99fJZHgw0qEwzEkCwBv/preview",
        "https://drive.google.com/file/d/1cJGIKWVLskE3W3z2U-IidO8g_VFKgbSk/preview",
        "https://drive.google.com/file/d/1W9ZIBUQAWp88zGf8CsWFPJBVC1BTknue/preview",
        "https://drive.google.com/file/d/1p9scTRz72UD1ukGcAWWw3w_3r8yWhWVb/preview"
    ],
    
    [
        "https://drive.google.com/file/d/1YWeWStbiu6r9UtUgjMkm1WB2lFBJX5zq/preview",
        "https://drive.google.com/file/d/1V5nsHR75-fsPWgniX2dJtlzUAREbk1lh/preview",
        "https://drive.google.com/file/d/1AjekLmFs8hbSSJoOR5q_kETeH3a1jMwI/preview",
        "https://drive.google.com/file/d/1CRUlPuj-OnGFddnZCmPC5BNx8SD92Nfj/preview"
    ],
    
    [
        "https://drive.google.com/file/d/1PYxQ3qHFdBFMZ60PvFMRV-eL0O0Di7AG/preview",
        "https://drive.google.com/file/d/1HV4Xp7K1D2ipZWJh1SgdGSfOwgQlPYDG/preview",
        "https://drive.google.com/file/d/1S88jRjAbRYqrNpEwsz6lC2JG3uBTbMBO/preview",
        "https://drive.google.com/file/d/1NjLijVxvfmyvc5RtigSA57TEkyT07Duu/preview"
    ],
    
    [
        "https://drive.google.com/file/d/10m2ckmt8XQYrva2N9gShe2hXpwunazSK/preview",
        "https://drive.google.com/file/d/1GNtztruj0BxGDWiULUVQAyq47iCq1_pF/preview",
        "https://drive.google.com/file/d/11TZo7R6rt3qzv3HLgXQWod_Y-aZ6jeqy/preview",
        "https://drive.google.com/file/d/1vVMsgFBXqhsU7PaViOINMOGaMJE4XuA5/preview"
    ],
    
     [
        "https://drive.google.com/file/d/1eDHUqYnMdlXmavNUx0NWVz1zlp9ruzu4/preview",
        "https://drive.google.com/file/d/1Kxl1HTbfMakfOMenGrOEkKWDBQFUBwes/preview",
        "https://drive.google.com/file/d/1_q4IbXPBt6GZqjD1tafl21lOMnWfgSFu/preview",
        "https://drive.google.com/file/d/1rXdVPd9lGCaI5rTYXRbfIYPJ7oxonOPO/preview"
    ],
    
     [
        "https://drive.google.com/file/d/1M2GobP7I5B8sLnFflKcoAtYjbiXIojqw/preview",
        "https://drive.google.com/file/d/1QIcTo8NgXdDLZqYpMjB9i7LmVd_4wqXK/preview",
        "https://drive.google.com/file/d/1_u1-YboR0-HrtK7gUFT_cqTWctvVpVY2/preview",
        "https://drive.google.com/file/d/1Nsfvg69EQXQVvstnl5YIq5lNDargxwS7/preview"
    ],
    
     [
        "https://drive.google.com/file/d/1Q3vYirAyAL-0TXGf5SLmc7V74qodykiI/preview",
        "https://drive.google.com/file/d/1bYdQofLqvGauLhPGJn89Qb8uhyQYwzrW/preview",
        "https://drive.google.com/file/d/1OKzVk5TPHl24r0_1rcqM9XG3pEi1WZI3/preview",
        "https://drive.google.com/file/d/1jJuJmALlYj4SIZeWRFgTTdWAP8PbBbB2/preview"
    ],
    
     [
        "https://drive.google.com/file/d/1uVGz_x6uKFzslOI0Q5DJd5YOflmK8Rlf/preview",
        "https://drive.google.com/file/d/1UxmtS3yJ4_WAZzvVUzs-VqxQ4eG2sbBi/preview",
        "https://drive.google.com/file/d/1V0C0Ikz-DCKUUmuU9dzlU8EsIta6SgKD/preview",
        "https://drive.google.com/file/d/1WevddcOA6QiJZrISC1Xt8zTvXywoxkuu/preview"
    ],
    
     [
        "https://drive.google.com/file/d/1kz5mHhTtYBbjllxPPkwCB2dhe8RllAoc/preview",
        "https://drive.google.com/file/d/1GVVOC6pxygVVvOl8PfuZJWyovp_iGrGs/preview",
        "https://drive.google.com/file/d/117l8G-BJ4Y9udVtgiQvFYBdHYAKFFO4r/preview",
        "https://drive.google.com/file/d/1qHrP4qETPbBs1BOfo8wH6tT0Ve0EWZLA/preview"
    ],
    
     [
        "https://drive.google.com/file/d/1Do109vDBcfeIpRAZQ-SyshGq7vX4DJAR/preview",
        "https://drive.google.com/file/d/15Xa5fkQOgIpu6py42mGUk4E0qiAuo8md/preview",
        "https://drive.google.com/file/d/1DEZNhIkZMtC971oypWq6dCiRq7Z8VoPM/preview",
        "https://drive.google.com/file/d/1zUOG1d_TlACW8G3M-AjYstLJ2ZJy6jzW/preview"
    ],
    
     [
        "https://drive.google.com/file/d/1WhigPH2vEtsdn7zGzXtgWYUG3dV9u_WS/preview",
        "https://drive.google.com/file/d/1M4oYXasMGREu8d-k3nuDBPQEZ1UlJtjO/preview",
        "https://drive.google.com/file/d/17gx0eRkhjY4lMkOJ_mTzihSiRVVWoReK/preview",
        "https://drive.google.com/file/d/1ClV2BjPy4eUvZrqMZqsoqQo_72yi8J6G/preview"
    ],
    
    [
        "https://drive.google.com/file/d/1oVqa-SmLgdDC6T81LVYp01szpY878Qpg/preview",
        "https://drive.google.com/file/d/1QsKiUjY5wL0XC55Nvy8dwq2WdP5xKg3A/preview",
        "https://drive.google.com/file/d/1qwgdHCaFCWG87k5ga8Z39vzJRpyJMbFX/preview",
        "https://drive.google.com/file/d/1JngfZ1rtCsSfQcFoxB0_RWzUe6OfDtpG/preview"
    ],
    
    [
        "https://drive.google.com/file/d/1DLN1rghwOlU0madKSPEC1RcQnpWV9iI5/preview",
        "https://drive.google.com/file/d/1WkjqeY-eW9arWqoCMS2lqPGmye_tPmTs/preview",
        "https://drive.google.com/file/d/1eA6F9aIoyl01t5AcHPiteNvXJOfKciCQ/preview",
        "https://drive.google.com/file/d/1pEGzWw2Zdzj9lQWE_NJV-tJ3DWvnDwnQ/preview"
    ],
    
    # ... Add until Set 14
]

# Convert to direct download
sets_audio = [[gdrive_preview_to_direct(url) for url in set_urls] for set_urls in sets_preview]

# -------------------------
# Main App
# -------------------------
def main():
    st.markdown("<h1 style='font-weight:bold;'>Reference Speaker Identification Test</h1>", unsafe_allow_html=True)

    st.markdown("""
    **Instructions:**
    - Each set contains 1 Reference sample and 3 Test samples.
    - Listen to the Reference sample first.
    - Then listen to the 3 Test samples.
    - Select which Test sample matches the Reference speaker's voice.
    - If you are unsure, we recommend you to give some more time for analysis but still can't make then select **"Can't say"**.
    - After all sets, click "Submit All Responses".
    """, unsafe_allow_html=True)

    email = st.text_input("Please enter your email address:", key="email")

    if "choices" not in st.session_state:
        st.session_state.choices = [None] * len(sets_audio)

    for set_idx, audio_urls in enumerate(sets_audio):
        st.subheader(f"Set {set_idx + 1}")

        st.markdown("**Reference Sample:**")
        st.audio(load_audio_bytes(audio_urls[0]), format='audio/wav')

        st.markdown("**Test Samples:**")
        for i in range(1, 4):
            st.markdown(f"**Test Sample {i}:**")
            st.audio(load_audio_bytes(audio_urls[i]), format='audio/wav')

        st.session_state.choices[set_idx] = st.radio(
            "Select the sample that matches the Reference speaker:",
            options=["1", "2", "3", "Can't say"],
            index=(
                ["1", "2", "3", "Can't say"].index(st.session_state.choices[set_idx])
                if st.session_state.choices[set_idx] in ["1", "2", "3", "Can't say"]
                else 3
            ),
            key=f"choice_{set_idx}"
        )
        st.markdown("---")

    if st.button("Submit All Responses"):
        missing_info = []
        if email.strip() == "":
            missing_info.append("Email address is missing")
        elif "@" not in email or "." not in email:
            missing_info.append("Invalid email address format")

        unanswered = [i+1 for i, val in enumerate(st.session_state.choices) if val is None]
        if unanswered:
            missing_info.append(f"Missing selections for sets: {', '.join(map(str, unanswered))}")

        if missing_info:
            st.error("Please check the following before submitting:\n- " + "\n- ".join(missing_info))
        else:
            sheet = open_sheet()
            for set_idx, choice in enumerate(st.session_state.choices):
                row = [email, f"Set-{set_idx+1}", choice]
                sheet.append_row(row)

            st.success("✅ All responses recorded in Google Sheets! Thank you.")
            st.session_state.choices = [None] * len(sets_audio)


if __name__ == "__main__":
    main()

