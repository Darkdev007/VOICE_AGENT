from cartesia import Cartesia
import sounddevice as sd
import numpy as np
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("CARTESIA_API_KEY")
client = Cartesia(api_key=api_key)


def speak_text(text: str):
    """Convert text to speech and play it immediately."""
    buffer = bytearray()
    chunk_iter = client.tts.bytes(
        model_id = "sonic-3",
        transcript = text,
        voice = {
            "mode" : "id",
            "id" : "6ccbfb76-1fc6-48f7-b71d-91ac6298247b"
        },
        output_format = {
            "container" : "raw", #would be "wav" for saving files
            "sample_rate": 44100,
            "encoding" : "pcm_f32le"
        },
    )

    #to save the file
    # with open("sonic.wav", "wb") as f:
    #     for chunk in chunk_iter:
    #         f.write(chunk)

    def audio_callback(outdata, frames, time, status):
        nonlocal buffer 
        bytes_needed = frames * 4

        if len(buffer) >= bytes_needed:
            chunk = buffer[:bytes_needed]
            buffer = buffer[bytes_needed:]
            audio = np.frombuffer(chunk, dtype=np.float32)
            outdata[:] = audio.reshape(-1, 1)
        else:
            outdata[:] = np.zeros((frames, 1), dtype=np.float32)

    #open and audio output stream
    with sd.OutputStream(
        samplerate=44100,
        channels=1,
        dtype="float32",
        callback=audio_callback,
        blocksize=1024
    ) :
        
        for chunk in chunk_iter:
            buffer.extend(chunk)
            
        while len(buffer) > 0:
            sd.sleep(50)

