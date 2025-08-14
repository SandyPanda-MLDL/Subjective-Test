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
#1
    [
        "https://drive.google.com/file/d/1iCKmw1e-uPDdHY6Va_sVOCDvM52HkvY_/preview",
        "https://drive.google.com/file/d/1jNTwzuKQFDV6I7DtmWukm_UNfhpWtUG9/preview",
        "https://drive.google.com/file/d/1AODq6B_8wLCuglwy1AukZW2Gl7_2K3M-/preview",
        "https://drive.google.com/file/d/1TPSOnkY-vvZWwcjpyjFm7Ewk0oCbINie/preview"
    ],
#2
    [
        "https://drive.google.com/file/d/1l4g5a1rDhzqwS2ZMHtdWaP_57ketkOsU/preview",
        "https://drive.google.com/file/d/1cD5E0vgTNH_QZdGKV0bOifexM080HT-Z/preview",
        "https://drive.google.com/file/d/1GqhV6EmbsdJJqwoMog38ff8k4B6-80O2/preview",
        "https://drive.google.com/file/d/1sSi0Pl-WMr-f7QaaXW2Q0XYQj7kNNxca/preview"
    ],
#3   
     [
        "https://drive.google.com/file/d/1LUOFlg2nEKEU2hW8NrGtmzhHhuD3lEt0/preview",
        "https://drive.google.com/file/d/1ND5IvenSmi8xn4O4KJH3_cT_vU7leeZc/preview",
        "https://drive.google.com/file/d/1YxfBAH57nzv4KUopXqBxG23wmjn5lt7a/preview",
        "https://drive.google.com/file/d/1DAcjzKp-akMF8lgogtNd1sZWKaymIMSX/preview"
    ],
#4  
    [
        "https://drive.google.com/file/d/1_UG5pKprZEDEZuttUpDa-uT8KwFZ9s4f/preview",
        "https://drive.google.com/file/d/1lR-nADrRwku5mOO4ZR5UJiBt-pxRDiHu/preview",
        "https://drive.google.com/file/d/1S63bYraiKJUzCuX_gE-NJfjU5SxN-CKt/preview",
        "https://drive.google.com/file/d/1U2iaUtMyvQl1RMtAce9Yr1HrtdqH1pD6/preview"
    ],       
#5   
    [
        "https://drive.google.com/file/d/1YTgt690DaZFYXkIubyKMaezJPQaCcMmW/preview",
        "https://drive.google.com/file/d/1ktiyEbgKVY1eWB5JRqF9HtyGUP1S13p8/preview",
        "https://drive.google.com/file/d/1ydHFGPzT7HSpvL8799Gf6Ly0nj0zQLyk/preview",
        "https://drive.google.com/file/d/1RwO3KQgnlNH_9eM_78xh6FReZeF-75lV/preview"
    ],
#6   
    [
        "https://drive.google.com/file/d/1OzODMVS2-mTg-JTy1y3CttHewb-b8h_T/preview",
        "https://drive.google.com/file/d/1lgdOQpXrv_WBHu6o0s3atRXJwCVfTpLw/preview",
        "https://drive.google.com/file/d/10Mfdfu0nPYgxNQdgw0K8H2NYmqPvOSC_/preview",
        "https://drive.google.com/file/d/1yT26v4dKYATGX7yz_CQqQgXmE1AVXIyP/preview"
    ],
    
#7   
    [
        "https://drive.google.com/file/d/1uWnWrUTt-l4vH2GTdgGgJfavvbpOJTiK/preview",
        "https://drive.google.com/file/d/1VHAbJR6RlQM1_6hhbsxlfUrJpCUV15QX/preview",
        "https://drive.google.com/file/d/1fEDpeacA9GKJtbKFzi1gWgqqsIQxO9BX/preview",
        "https://drive.google.com/file/d/1N1Dy0tX2Ab8XpnA7QmlXub8iB5-B4wxv/preview"
    ],
#8   
    [
        "https://drive.google.com/file/d/1FzVw10OP1tpiH-GO4J9N4PGCyGg4qEl5/preview",
        "https://drive.google.com/file/d/1E5NKh0zAD7Y-rEDIfE_ZGHZCj9Oxdt5r/preview",
        "https://drive.google.com/file/d/1nK0UFQkd8erBzo0qPorpKpmP7P3XZ5yB/preview",
        "https://drive.google.com/file/d/18YgwqpF1QAguMwxzc28cqlRAHf4SHoAy/preview"
    ],     
#9   
    [
        "https://drive.google.com/file/d/1184qnse62bcTynAnLPIrPIW55s2k1PN4/preview",
        "https://drive.google.com/file/d/1cV77Ov6VDw9iAv7uSxAAlhAPZZdfSttg/preview",
        "https://drive.google.com/file/d/1nhfhFMKVwUjwj-4A98dATON_DSdZvJ14/preview",
        "https://drive.google.com/file/d/1WrpKMH3ajGfhumWpznN0rbxiMuxaS8x2/preview"
    ], 
#10   
    [
        "https://drive.google.com/file/d/1j_1TvHV-60de9Bpxfe4x2427s0lGOzEq/preview",
        "https://drive.google.com/file/d/1m30TeVtrIkL1qWqRXGbo5qL-rqKLesQT/preview",
        "https://drive.google.com/file/d/1DKXZmsoxoECA8bDoqIT6REID7Uym6GSj/preview",
        "https://drive.google.com/file/d/16ztnOTsRZFXm8PJd_Qf2csDYnvFDaZYn/preview"
    ],
#11   
    [
        "https://drive.google.com/file/d/1IVcBSWtTUfWGdcrIFOczoo2RByFAtoFf/preview",
        "https://drive.google.com/file/d/19aYAaS63pa6IoF0k1cb2tBV1ICax_YQ4/preview",
        "https://drive.google.com/file/d/1myT3CTrHzpngP59dn1egtgecIbujSTLI/preview",
        "https://drive.google.com/file/d/1myT3CTrHzpngP59dn1egtgecIbujSTLI/preview"
    ],
#12 
  
    [
        "https://drive.google.com/file/d/19LNbJxnUiB2-2cyfLq3UmFAIdGoJPGcv/preview",
        "https://drive.google.com/file/d/1FQqUFnLgiScpJBxTe1cUe-nsEZu5R8rs/preview",
        "https://drive.google.com/file/d/1tP9vhTEtRWWurLbMLvusteyv_xaNnzoK/preview",
        "https://drive.google.com/file/d/155Wlp8CE3jAgVdWiVu77XDmBlVQYQU1C/preview"
    ],   
 #13 
    [
        "https://drive.google.com/file/d/1urhgDCS9TF7pG1BL1XyyQ-prHbOJmo8I/preview",
        "https://drive.google.com/file/d/11hpckdyspWhi1nI2sZ6FawUqq8MXxfXL/preview",
        "https://drive.google.com/file/d/1MB05zmFHZN652WjCgml-4H8E5Y37H1rA/preview",
        "https://drive.google.com/file/d/1cz5z3-iCH8-gMCO9ECL2TmVZiXoEg2u6/preview"
    ],
 #14 
    [
        "https://drive.google.com/file/d/1AOXTr4QujRiyeCy_8Od231YZ99BF5gOM/preview",
        "https://drive.google.com/file/d/1aOdPraKZESh9V66RKQS4W4FP0EvlBsrS/preview",
        "https://drive.google.com/file/d/1-7Ns-jNR5-eEhVZsE9BpGpLJp9HlKsMm/preview",
        "https://drive.google.com/file/d/1192PmPC-Gjq1qz-P9L4T8P9nF2ldMgDE/preview"
    ],
  #15 
    [
        "https://drive.google.com/file/d/1R1opmPWZOYphM4K34yHd1WdIMoFoVnPc/preview",
        "https://drive.google.com/file/d/1M4IAYAUhcqbxwF75hgbhA2_g3Mqg37iu/preview",
        "https://drive.google.com/file/d/1j8GWZ6MCJ9lGRUx3FuHfo22USMtz8YrY/preview",
        "https://drive.google.com/file/d/1C9JnRzTaNogaHSTQ1Xus8OpHOCDxkRrK/preview"
    ],
    #16 
    [
        "https://drive.google.com/file/d/1LKUEw1PqHYgrWUiNwjONsduWFpc8WQxe/preview",
        "https://drive.google.com/file/d/1KSPl-bYceeznadGQOtwH0XIsfrLWme_u/preview",
        "https://drive.google.com/file/d/1x-AuzVPnW_80bw6WyaHlbLouV1fFBiu0/preview",
        "https://drive.google.com/file/d/1Mzpf4d9eZTsEI676YEvgNkYf2x_9C7KT/preview"
    ],
     #17 
    [
        "https://drive.google.com/file/d/16us8KfeTGp5zKWtG6gfu0LSJSgrFV3jT/preview",
        "https://drive.google.com/file/d/1saQ0ZtlNO2RYaQQk54eOme-GUVVDScA8/preview",
        "https://drive.google.com/file/d/1pGPfepjgjJl5CeJSDqfPf8UfydXkwvra/preview",
        "https://drive.google.com/file/d/1EHlpwU-RNuL32taDN3GeZsXxt0NuQAJ1/preview"
    ],
    #18

    [
        "https://drive.google.com/file/d/1AS4ncbXqJ00T0ENYI3PA4gBCDsOfb9iD/preview",
        "https://drive.google.com/file/d/1qKt9VbSISb2p7rWrzw1YRGmzrHd9oGUr/preview",
        "https://drive.google.com/file/d/15QZR1nLPAyEgu1sTO-5t3q-oR7Ps2EBN/preview",
        "https://drive.google.com/file/d/1CBH3qk5LoW_aXtOERJGUxcM3fkYL4K98/preview"
    ],
     #19

    [
        "https://drive.google.com/file/d/16ZYZpDMWURK6KhCw938W0a2ESwKkmjjJ/preview",
        "https://drive.google.com/file/d/1YIjEIsT9UTVjp9wOjrTUK_W7BQtvAvnX/preview",
        "https://drive.google.com/file/d/1f07wFTSNDNeE0-80itkUODPU2xgQTBPX/preview",
        "https://drive.google.com/file/d/1FMQ1e7klWnj5MZIykEq1hHQxbYkRypRB/preview"
    ],
     #20

    [
        "https://drive.google.com/file/d/1LAHvtqxpu1IIXeAA0-rT38dde332rwa1/preview",
        "https://drive.google.com/file/d/1QouGxAZttsbCJYByzJGmG4EhQ3Ax-1vL/preview",
        "https://drive.google.com/file/d/1fhhjQmaT9gKNcARp9cK-Rk5o_TuTlRvL/preview",
        "https://drive.google.com/file/d/1P4FKLR2Pn0Z7nH9R8UW7zImwtKDS3Kng/preview"
    ],
     #21

    [
        "https://drive.google.com/file/d/1ni5zhDdV_pg_t3siw5h5LVRazZ_WWaFt/preview",
        "https://drive.google.com/file/d/1unJ_Q6QTz0VB6C0eYM4s32Haj2tN2Eom/preview",
        "https://drive.google.com/file/d/17n6is0ZXrTxDvIsXMT8LRZmsedeGWDoX/preview",
        "https://drive.google.com/file/d/15yJD8NpOFyEVorfHCeuIOywBjND2Soju/preview"
    ],
     #22

    [
        "https://drive.google.com/file/d/1HXOEA5pJt4SjHGo1Ns4SS2VW0P7CU5uR/preview",
        "https://drive.google.com/file/d/1m-KHTHQzzS1-TBNjNw_Gs97MjtN73Stc/preview",
        "https://drive.google.com/file/d/1LorJkaBpPcf9rZrUR0Xk20XTwa0jYeqp/preview",
        "https://drive.google.com/file/d/1bhrUX8OANX7VKaQucJDxCSiCu419rAiv/preview"
    ],
      #23

    [
        "https://drive.google.com/file/d/11HlkeWYrcdu57VAR1ZOSm_jGVEKGPj3N/preview",
        "https://drive.google.com/file/d/1BHcpvfaL1wpYZRutW-1hh-nP0dzx7-Mu/preview",
        "https://drive.google.com/file/d/1msan2l47tSjokSbpuq6fw4I0ar9ZExV8/preview",
        "https://drive.google.com/file/d/1ESMkEPQTrTLQyvV8IzIU767KwxSarFVJ/preview"
    ],
      #24

    [
        "https://drive.google.com/file/d/1Q3Iyd6RVcMqxE0Nf1s1h89tuofWEtGoI/preview",
        "https://drive.google.com/file/d/1rVrAODKKHNISSonDIjlaylc4FPtRV_vC/preview",
        "https://drive.google.com/file/d/1mhNzGTfU3KB3r7mXgH23ROGrLfTp2YQK/preview",
        "https://drive.google.com/file/d/1eCdZ7f5u47xLge8PlkQrVg8XaIw8UTeH/preview"
    ]                             
                                             
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
    - The Test samples are drawn from modified (anonymised) versions of different speakers' utterances including one of the Reference speaker
    - Please pick the Test sample that you feel is most likely to belong to the Reference speaker. 
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

