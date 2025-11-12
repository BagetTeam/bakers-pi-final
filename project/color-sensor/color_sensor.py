from utils.brick import EV3ColorSensor, wait_ready_sensors, TouchSensor

class ColorSensor:
    def __init__(self, sensor: EV3ColorSensor):
        wait_ready_sensors()
        self.sensor = sensor
        self.sensor.set_mode("RGB-RAW")

    def get_rgb(self):
        return self.sensor.get_value(0), self.sensor.get_value(1), self.sensor.get_value(2)
    
    