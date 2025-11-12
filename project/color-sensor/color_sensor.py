from utils.brick import EV3ColorSensor, wait_ready_sensors

class ColorSensor:
    REFS = {
        "RED": (255.0, 0.0, 0.0),
        "GREEN": (0.0, 255.0, 0.0),
        "BLUE": (0.0, 0.0, 255.0),
        "YELLOW": (255.0, 255.0, 0.0),
        "BLACK": (0.0, 0.0, 0.0),
        "WHITE": (255.0, 255.0, 255.0)
    }

    NORMALIZED_REFS = {key: ColorSensor.normalize_rgb(value) for key, value in REFS.items()}

    def __init__(self, sensor: EV3ColorSensor):
        wait_ready_sensors()
        self.sensor = sensor
        

    def get_rgb(self) -> list[float]:
        return self.sensor.get_rgb()
    
    def classify_color(self) -> str:
        rgb = self.get_rgb()
        red, green, blue = rgb

        if red > green and red > blue:
            return "red"
        elif green > red and green > blue:
            return "green"
        elif blue > red and blue > green:
            return "blue"
        else:
            return "unknown"
    
    @staticmethod
    def normalize_rgb(rgb: tuple[float]) -> tuple[float]:
        total = sum(rgb)
        if total == 0:
            return (0.0, 0.0, 0.0)
        return (value / total for value in rgb)
    
    def filter_data(r, g, b):
        if r is not None and g is not None and b is not None:
            if r > 0 and g > 0 and b > 0:
                return True
        return False

    
    def is_color_detected(self, target_color: str, threshold: float = 0.1) -> bool:
        rgb = self.get_rgb()
        normalized_rgb = self.__normalize_rgb(rgb)
        red, green, blue = normalized_rgb

        if target_color == "red":
            return red > green + threshold and red > blue + threshold
        elif target_color == "green":
            return green > red + threshold and green > blue + threshold
        elif target_color == "blue":
            return blue > red + threshold and blue > green + threshold
        else:
            return False
        
    
    

    