from time import sleep
import math
from project.utils.brick import (
    EV3ColorSensor,
    Motor    
)

COLOR_SENSOR = EV3ColorSensor(2)
MOTOR = Motor("A")

class LineTracker:
    def __init__(self, sensor=COLOR_SENSOR, motor=MOTOR, kp=0.8, base=0.0):
        self.sensor = sensor
        self.motor = motor
        self.kp = kp
        self.base = base
        self.black = None
        self.white = None
        self.threshold = 50.0

    def _read_reflection(self):
        s = self.sensor
        # try common attribute/method names used by different EV3 libs
        for attr in ("reflected_light_intensity", "reflection", "reflected_light", "value", "read"):
            try:
                val = getattr(s, attr)
                # if callable, call it
                if callable(val):
                    val = val()
                return float(val)
            except Exception:
                pass
        # last resort: some sensors expose values as a tuple/list at `value(0)` or `values`
        try:
            if hasattr(s, "value") and callable(s.value):
                v = s.value(0)
                return float(v)
        except Exception:
            pass
        raise RuntimeError("Could not read reflection from sensor with known API")

    def calibrate(self, samples=20, delay=0.1):
        input("Place sensor over BLACK (line) and press Enter to start sampling...")
        black_vals = []
        for _ in range(samples):
            try:
                black_vals.append(self._read_reflection())
            except Exception:
                pass
            sleep(delay)
        input("Place sensor over WHITE (background) and press Enter to start sampling...")
        white_vals = []
        for _ in range(samples):
            try:
                white_vals.append(self._read_reflection())
            except Exception:
                pass
            sleep(delay)

        if black_vals:
            self.black = sum(black_vals) / len(black_vals)
        if white_vals:
            self.white = sum(white_vals) / len(white_vals)

        if self.black is not None and self.white is not None:
            self.threshold = (self.black + self.white) / 2.0
        print(f"Calibration done. black={self.black:.2f}, white={self.white:.2f}, threshold={self.threshold:.2f}")

    def compute_correction(self, reflection, target=None):
        if target is None:
            target = self.threshold
        error = target - reflection
        return self.kp * error + self.base

    def _apply_to_motor(self, correction):
        m = self.motor
        # scale correction into a plausible motor speed/power range
        # assume correction in [-100,100] roughly; clamp
        try:
            c = float(correction)
        except Exception:
            return
        # clamp to -100..100
        c = max(min(c, 100.0), -100.0)

        # try common methods in order
        # 1) on or on_for_seconds (ev3dev/pybricks style)
        try:
            if hasattr(m, "on"):
                m.on(c)
                return
            if hasattr(m, "on_for_seconds"):
                m.on_for_seconds(c, 0.1)
                return
        except Exception:
            pass

        # 2) run_forever / run (ev3dev2 LargeMotor)
        try:
            if hasattr(m, "run_forever"):
                m.run_forever(speed_sp=c)
                return
            if hasattr(m, "run"):
                m.run(c)
                return
        except Exception:
            pass

        # 3) speed_sp / duty_cycle_sp properties then write a command if available
        try:
            if hasattr(m, "speed_sp"):
                m.speed_sp = c
                if hasattr(m, "command"):
                    m.command = "run-forever"
                return
            if hasattr(m, "duty_cycle_sp"):
                m.duty_cycle_sp = c
                if hasattr(m, "command"):
                    m.command = "run-forever"
                return
        except Exception:
            pass

        # Last resort: try a generic set_speed / set_power
        try:
            if hasattr(m, "set_speed"):
                m.set_speed(c)
            elif hasattr(m, "set_power"):
                m.set_power(c)
        except Exception:
            pass

    def follow(self, duration=None, apply_correction=None, interval=0.02):
        start = time()
        try:
            while True:
                reflection = self._read_reflection()
                corr = self.compute_correction(reflection)
                if apply_correction:
                    try:
                        apply_correction(corr, reflection)
                    except Exception:
                        pass
                else:
                    # default behavior: attempt to apply correction to single MOTOR
                    self._apply_to_motor(corr)
                # also give some terminal feedback
                print(f"reflect={reflection:.2f}, corr={corr:.2f}")
                if duration is not None and (time() - start) >= duration:
                    break
                sleep(interval)
        except KeyboardInterrupt:
            print("Stopped by user")
        finally:
            # try to stop motor nicely
            try:
                if hasattr(self.motor, "off"):
                    self.motor.off()
                elif hasattr(self.motor, "stop"):
                    self.motor.stop()
                elif hasattr(self.motor, "command"):
                    self.motor.command = "stop"
            except Exception:
                pass        