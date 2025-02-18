import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode
import speech_recognition as sr
import av

# Title
st.title("🎤 Live Speech-to-Text Recognition")
st.write("Speak into your microphone, and the app will transcribe your speech in real time.")

# Audio Processor Class
class AudioProcessor:
    def __init__(self):
        self.recognizer = sr.Recognizer()
    
    def recv(self, frame: av.AudioFrame) -> av.AudioFrame:
        audio_data = frame.to_ndarray()
        audio = sr.AudioData(audio_data.tobytes(), 16000, 2)

        try:
            text = self.recognizer.recognize_google(audio)
            st.text_area("Live Transcription:", value=text, height=150)
        except sr.UnknownValueError:
            st.warning("Could not understand audio")
        except sr.RequestError:
            st.error("Speech recognition request failed")

        return frame

# WebRTC Streamer
webrtc_streamer(
    key="speech-to-text",
    mode=WebRtcMode.SENDONLY,
    media_stream_constraints={"video": False, "audio": True},
    async_processing=True,
    rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
    video_processor_factory=AudioProcessor,
)

