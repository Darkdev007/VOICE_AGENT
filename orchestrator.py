from agent import ask_agent
from stt import stream_audio_to_text, stop_event
from tts import speak_text
import time

def run_voice_agent_pipeline():
    """Main function to run the voice agent pipeline."""

    def handle_transcript(transcript: str):
        print(f"\n[Transcript] : {transcript}")
        # send transcipt to langchain agent
        response_text = ask_agent(transcript)
        print(f"[Agent] : {response_text}")
        #Convert agent response to speech
        speak_text(response_text)

    #start Assembly AI streaming
    ws_app, stream, audio = stream_audio_to_text(handle_transcript, silence_timeout=3)

    print("Voice agent running. Speak into your microphone...")
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nStopping voice agent...")
        stop_event.set()
        if ws_app:
            ws_app.close()
        if stream:
            stream.stop_stream()
            stream.close()
        if audio:
            audio.terminate()
        print("Pipeline stopped cleanly.")