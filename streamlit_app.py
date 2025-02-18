import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode
import speech_recognition as sr
import queue
import av
import numpy as np

# Title and Description
st.title("🎤 Live Speech-to-Text Recognition")
st.write("Speak into your microphone, and the app will transcribe your speech in real time.")

# Queue to store audio frames
audio_queue = queue.Queue()

# WebRTC Audio Stream
def audio_callback(frame: av.AudioFrame) -> av.AudioFrame:
    audio = frame.to_ndarray()
    audio_data = sr.AudioData(audio.tobytes(), 16000, 2)  # Convert to SpeechRecognition format
    
    recognizer = sr.Recognizer()
    try:
        text = recognizer.recognize_google(audio_data)
        st.text_area("Live Transcription:", value=text, height=150)
    except sr.UnknownValueError:
        st.warning("Speech not recognized, please try again.")
    except sr.RequestError:
        st.error("Could not request results, check your internet connection.")

    return frame

# Start WebRTC Stream
webrtc_streamer(
    key="speech-to-text",
    mode=WebRtcMode.SENDONLY,
    audio_receiver_size=1024,
    media_stream_constraints={"video": False, "audio": True},
    async_processing=True,
    rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
    audio_frame_callback=audio_callback,  # Use audio callback instead of video_processor_factory
)
