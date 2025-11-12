from utils.brick import EV3ColorSensor, wait_ready_sensors, TouchSensor

class ColorSensor:
    def __init__(self, sensor: EV3ColorSensor):
        wait_ready_sensors()
        self.sensor = sensor

    def get_rgb(self) -> list[float]:
        return self.sensor.get_rgb()
    
        
    