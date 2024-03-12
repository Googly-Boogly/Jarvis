import webrtcvad
from vosk import Model, KaldiRecognizer
import json

vad = webrtcvad.Vad()
# Set aggressiveness from 0 to 3
vad.set_mode(1)

def frame_generator(frame_duration_ms, audio, sample_rate):
    # Generates audio frames to be passed to VAD
    n = int(sample_rate * (frame_duration_ms / 1000.0) * 2)
    offset = 0
    while offset + n < len(audio):
        yield audio[offset:offset+n]
        offset += n

def vad_check(sample_rate, frame_duration_ms, padding_duration_ms, vad, audio):
    frames = frame_generator(frame_duration_ms, audio, sample_rate)
    # Check VAD here, return True if speech detected in any frame
    for frame in frames:
        if vad.is_speech(frame, sample_rate):
            return True
    return False


model = Model("path/to/vosk/model")


def wake_word_detected(audio):
    rec = KaldiRecognizer(model, 16000)
    if rec.AcceptWaveform(audio):
        result = json.loads(rec.Result())
        # Assuming your wake word is "activate"
        if "activate" in result.get('text', ''):
            return True
    return False
