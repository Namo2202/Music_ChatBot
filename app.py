import streamlit as st
import requests

st.title("Music Chatbot")

user_input = st.text_input("You:", "")
if st.button("Send"):
    st.write(f"You: {user_input}")

    # Send user input to backend
    response = requests.post("http://127.0.0.1:8000/get_response", json={"dialog": [user_input]})

    if response.ok:
        data = response.json()
        st.write(f"Bot: {data['generated_response']}")
        st.write("Music Recommendations:")
        for rec in data["recommendations"]:
            st.write(f"- {rec['name']} by {rec['artist']['name']}")
            listen_url = rec['url']
            st.markdown(f"[Listen]({listen_url})")
