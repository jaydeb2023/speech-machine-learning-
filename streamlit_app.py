import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode
import speech_recognition as sr
import queue
import av

# Title and Description
st.title("🎤 Live Speech-to-Text Recognition")
st.write("Speak into your microphone, and the app will transcribe your speech in real time.")

# Create an audio queue
audio_queue = queue.Queue()

# Speech recognition callback function
def callback(indata, frame_count, time_info, status):
    audio_queue.put(bytes(indata))

# WebRTC Audio Stream
class AudioProcessor:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.source = sr.Microphone()
    
    def recv(self, frame: av.AudioFrame) -> av.AudioFrame:
        audio = frame.to_ndarray()
        audio_data = sr.AudioData(audio.tobytes(), 16000, 2)
        
        try:
            text = self.recognizer.recognize_google(audio_data)
            st.text_area("Live Transcription:", value=text, height=150)
        except sr.UnknownValueError:
            st.warning("Speech not recognized, please try again.")
        except sr.RequestError:
            st.error("Could not request results, check your internet connection.")
        
        return frame

# Start WebRTC
webrtc_streamer(
    key="speech-to-text",
    mode=WebRtcMode.SENDONLY,
    audio_receiver_size=1024,
    media_stream_constraints={"video": False, "audio": True},
    async_processing=True,
    rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
    video_processor_factory=AudioProcessor,
)


