import pyttsx3
import queue

def init_tts():
    engine = pyttsx3.init()
    return engine

def process_reading_queue(engine, reading_queue, stop_event):
    while True:
        text = reading_queue.get()
        if text is None or stop_event.is_set():  # None か stop_event がセットされたら停止
            engine.stop()
            return
        engine.say(text)
        engine.runAndWait()
