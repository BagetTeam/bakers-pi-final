import threading
import time
from pathlib import Path
import simpleaudio as sa


class MusicLooper:
    def __init__(self):
        self.bg_path = Path("sounds/background.wav")
        self.effects = {
            "TURNING": Path("sounds/delivery.wav"),
            "FINISH": Path("sounds/what-is-this-diddy-blud-doing-on-the (mp3cut.net).wav"),
            "DELIVERY": Path("sounds/WE-ARE-CHARLIE-KIRK (mp3cut.net).wav"),
        }
        if not self.bg_path.exists():
            raise FileNotFoundError(self.bg_path)

        # Load background audio data once
        self._bg_wave = sa.WaveObject.from_wave_file(str(self.bg_path))

        # State management
        self._thread = None
        self._stop_event = threading.Event()
        self._pause_event = threading.Event()
        self._pause_event.set()  # Start unpaused

        # Lock for all audio operations
        self._audio_lock = threading.Lock()

        # Current play object (always accessed with lock held)
        self._current_play_obj = None

        # Effect lock
        self._effect_lock = threading.Lock()

    def start(self):
        """Start the background music loop."""

        if self._thread and self._thread.is_alive():
            return

        self._stop_event.clear()
        self._thread = threading.Thread(target=self._bg_loop, daemon=True)
        self._thread.start()

    def _bg_loop(self):
        """Background thread loop for playing music."""
        while not self._stop_event.is_set():
            # Wait until unpaused
            self._pause_event.wait()

            if self._stop_event.is_set():
                break

            # Start playback with lock held
            with self._audio_lock:
                if self._stop_event.is_set() or not self._pause_event.is_set():
                    continue
                self._current_play_obj = self._bg_wave.play()

            # Monitor playback (check lock periodically)
            while True:
                time.sleep(0.05)  # Longer sleep to reduce contention

                # Re-check pause event frequently
                if not self._pause_event.is_set():
                    with self._audio_lock:
                        if self._current_play_obj:
                            self._current_play_obj.stop()
                            self._current_play_obj = None
                    break

                # Check if naturally finished
                with self._audio_lock:
                    if (
                        self._current_play_obj
                        and not self._current_play_obj.is_playing()
                    ):
                        self._current_play_obj = None
                        break

                # Check stop event
                if self._stop_event.is_set():
                    with self._audio_lock:
                        if self._current_play_obj:
                            self._current_play_obj.stop()
                            self._current_play_obj = None
                    break

    def stop(self):
        """Stop all playback and the background thread."""
        self._stop_event.set()
        self._pause_event.set()  # Unblock if paused

        with self._audio_lock:
            if self._current_play_obj:
                self._current_play_obj.stop()
                self._current_play_obj = None

        if self._thread:
            self._thread.join(timeout=2.0)
            self._thread = None

    def play_effect(self, effect_name: str):
        """
        Play an effect WAV file, interrupting the background.
        This call blocks until the effect finishes.
        """
        effect_path = self.effects.get(effect_name)
        if not effect_path:
            raise ValueError(f"Effect '{effect_name}' not found")
        effect = Path(effect_path)
        if not effect.exists():
            raise FileNotFoundError(effect)
        
        effect_thread = threading.Thread(target=self._play_effect_thread, args=(effect,), daemon=True)
        effect_thread.start()
        
    def _play_effect_thread(self, effect: Path):
        with self._effect_lock:
            # Pause background
            self._pause_event.clear()

            # Stop current background playback
            with self._audio_lock:
                if self._current_play_obj:
                    self._current_play_obj.stop()
                    self._current_play_obj = None

            # Small delay to let audio system settle
            time.sleep(0.05)

            # Play effect
            try:
                effect_wave = sa.WaveObject.from_wave_file(str(effect))
                effect_play = effect_wave.play()
                effect_play.wait_done()
            except Exception as e:
                print(f"Error playing effect: {e}")
            finally:
                # Resume background
                self._pause_event.set()

    def is_running(self):
        return self._thread and self._thread.is_alive()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.stop()


if __name__ == "__main__":
    # Demo:
    # - Put two WAV files in the project (background.wav and effect.wav).
    # - Run: python demo/loop_with_effect.py

    looper = MusicLooper()
    looper.start()
    print("Background started. Press Ctrl+C to quit. Playing effect every 6s for demo.")
    try:
        while True:
            time.sleep(2)
            print("Playing effect...")
            looper.play_effect("DELIVERY")
            print("Effect done; background resumed.")
            time.sleep(4)
            looper.play_effect("FINISH")
            print("finished waiting cycle")
    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        looper.stop()
