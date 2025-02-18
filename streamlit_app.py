import streamlit as st
import speech_recognition as sr
import tempfile
import os

# Title and Description
st.title("🎤 Speech to Text Recognition App")
st.write("Upload an audio file, and the app will transcribe it into text.")

# Speech Recognition Object
recognizer = sr.Recognizer()

# File Uploader
audio_file = st.file_uploader("Upload an audio file (WAV, MP3, OGG)", type=["wav", "mp3", "ogg"])

if audio_file is not None:
    st.audio(audio_file, format="audio/wav")
    
    # Save uploaded file to a temporary location
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        temp_audio.write(audio_file.read())
        temp_audio_path = temp_audio.name

    # Process the audio file
    with sr.AudioFile(temp_audio_path) as source:
        st.write("🔄 Processing audio...")
        audio_data = recognizer.record(source)

    # Perform Speech Recognition
    try:
        text = recognizer.recognize_google(audio_data)
        st.subheader("📝 Transcribed Text:")
        st.write(text)
    except sr.UnknownValueError:
        st.error("⚠️ Sorry, could not understand the audio.")
    except sr.RequestError:
        st.error("🚫 Could not request results, check your internet connection.")

    # Clean up temporary file
    os.remove(temp_audio_path)

