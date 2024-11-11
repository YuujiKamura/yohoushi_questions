import pyttsx3
import threading


def stop_reading(self):
    # stop_eventがセットされると読み上げを終了する
    if self.engine:
        with self.reading_lock:
            self.stop_event.set()
            try:
                self.engine.stop()
            except RuntimeError:
                pass  # エラーが発生した場合は無視して続行
        self.update_status_label("読み上げ状態: 停止中")


def read_aloud_question(self):
    with self.reading_lock:
        if not self.stop_event.is_set():
            self.update_status_label("読み上げ状態: 読み上げ中")
            threading.Thread(target=lambda: read_aloud_question(self)).start()

def read_aloud_option(app, option_idx):
    """
    Starts reading aloud the specified option.
    :param app: The application instance containing the options and engine.
    :param option_idx: The index of the option to be read aloud.
    """
    if not app.reading_lock.locked():
        app.stop_event.clear()
        app.update_status_label("読み上げ状態: 読み上げ中")
        threading.Thread(target=_read_aloud, args=(app, app.current_question['選択肢'][option_idx],)).start()

def read_aloud_reason(app):
    """
    Starts reading aloud the reasons for the current question.
    :param app: The application instance containing the reasons and engine.
    """
    if not app.reading_lock.locked():
        app.stop_event.clear()
        app.update_status_label("読み上げ状態: 読み上げ中")
        threading.Thread(target=_read_aloud, args=(app, "\n".join(app.current_question['解説']),)).start()

def _read_aloud(app, text):
    """
    Internal function to handle the text-to-speech operation.
    :param app: The application instance containing the engine.
    :param text: The text to be read aloud.
    """
    with app.reading_lock:
        if not app.stop_event.is_set():  # Only start reading if stop event is not set
            app.engine = pyttsx3.init()  # Reinitialize the engine
            app.engine.say(text)
            app.engine.runAndWait()
        app.update_status_label("読み上げ状態: 停止中")