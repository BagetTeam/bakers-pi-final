import math
from utils.brick import EV3ColorSensor, wait_ready_sensors

class ColorSensor:
    REFS = {
        "RED": (1.0, 0.0, 0.0),
        "GREEN": (0.0, 1.0, 0.0),
        "BLUE": (0.0, 0.0, 1.0),
        "YELLOW": (1.0, 1.0, 0.0),
        "BLACK": (0.0, 0.0, 0.0),
        "WHITE": (1.0, 1.0, 1.0)
    } # temporary

    def __init__(self, sensor: EV3ColorSensor):
        wait_ready_sensors()
        self.sensor = sensor
        self.current_color = "UNKNOWN"
        
    def get_rgb(self) -> list[float]:
        return self.sensor.get_rgb()

    
    def __normalize_rgb(rgb: tuple[float]) -> tuple[float]:
        total = sum(rgb)
        if total == 0:
            return (0.0, 0.0, 0.0)
        return (value / total for value in rgb)
    
    def __filter_data(r, g, b):
        if r is not None and g is not None and b is not None:
            if r > 0 and g > 0 and b > 0:
                return True
        return False

    def __handle_threshold(color):
        return color

    def classify_color(self, r, g, b) -> str:
        color_found = "UNKNOWN"
        closest_dist = math.inf
        for name, (rr, gg, bb) in ColorSensor.REFS.items():
            dist = math.sqrt((r - rr) ** 2 + (g - gg) ** 2 + (b - bb) ** 2)
            if dist < closest_dist:
                closest_dist = dist
                color_found = name
        return color_found
    
    def get_color_detected(self):
        rgb = self.get_rgb()
        if not self.__filter_data:
            return "UNKNOWN"

        color_found = self.classify_color(*rgb)
        color_found = self.__handle_threshold(color_found)
        # extra things

        
        self.current_color = color_found
        return color_found