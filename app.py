import streamlit as st
import requests
import speech_recognition as sr
import pyttsx3


st.title("Music Chatbot")

# Function to send user input to backend and receive response
def get_bot_response(user_input):
    response = requests.post("http://127.0.0.1:8000/get_response", json={"dialog": [user_input]})
    if response.ok:
        return response.json()
    return None

# Function to perform speech-to-text conversion
def transcribe_audio():
    recognizer = sr.Recognizer()
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)

    with sr.Microphone() as mic:
        recognizer.adjust_for_ambient_noise(mic)
        # st.write("Recording...")
        audio = recognizer.listen(mic)

    try:
        text = recognizer.recognize_google(audio)
        st.write(f"Transcription: {text}")
        print(f"Text: {text}")
        return text
    except sr.UnknownValueError:
        st.write("Could not understand audio")
        return None
    except sr.RequestError as e:
        st.write(f"Error: {e}")
        return None

# Sidebar for user input options
input_option = st.sidebar.selectbox("Select input method:", ("Text", "Audio"))

if input_option == "Text":
    # Initialize chat messages if not already initialized
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []

    # Input field for user text input
    user_input = st.sidebar.text_input("You:", "")

    # Button to send user message
    if st.sidebar.button("Send"):
        # Get user input
        user_message = {'actor': 'user', 'payload': user_input, 'timestamp': len(st.session_state.chat_messages)}
        st.session_state.chat_messages.append(user_message)

        # Get bot response
        bot_response = get_bot_response(user_input)

        if bot_response:
            # Append bot response to chat history
            bot_message = {'actor': 'bot', 'payload': bot_response['generated_response'], 'timestamp': len(st.session_state.chat_messages)}
            st.session_state.chat_messages.append(bot_message)
            
            # Display chat history
            for message in st.session_state.chat_messages:
                if message['actor'] == 'user':
                    st.text_input("You:", value=message['payload'], key=message['timestamp'], disabled=True)
                elif message['actor'] == 'bot':
                    st.text_area("Bot:", value=message['payload'], key=message['timestamp'], disabled=True)

            # songs recommendations
            st.write("Music Recommendations:")
            for rec in bot_response["recommendations"]:
                st.write(f"- {rec['name']} by {rec['artist']['name']}")
                listen_url = rec['url']
                st.markdown(f"[Listen]({listen_url})")

elif input_option == "Audio":
   # Button to record audio
    recording = st.sidebar.button("Record")

    if recording:
        with st.spinner("Recording..."):
            stop_recording = st.sidebar.button("Cancel")
            if stop_recording:
                st.write("Recording stopped.")
            else:
                transcribed_text = transcribe_audio()
                if transcribed_text:
                    bot_response = get_bot_response(transcribed_text)
                    if bot_response:
                        # Append bot response to chat history
                        bot_message = {'actor': 'bot', 'payload': bot_response['generated_response'], 'timestamp': len(st.session_state.chat_messages)}
                        st.session_state.chat_messages.append(bot_message)

                        # Display chat history
                        for message in st.session_state.chat_messages:
                            if message['actor'] == 'user':
                                st.text_input("You:", value=message['payload'], key=message['timestamp'], disabled=True)
                            elif message['actor'] == 'bot':
                                st.text_area("Bot:", value=message['payload'], key=message['timestamp'], disabled=True)

                        # Display music recommendations
                        st.write("Music Recommendations:")
                        for rec in bot_response["recommendations"]:
                            st.write(f"- {rec['name']} by {rec['artist']['name']}")
                            listen_url = rec['url']
                            st.markdown(f"[Listen]({listen_url})")
        
    else:
        st.write("Click 'Record' to start recording.")
