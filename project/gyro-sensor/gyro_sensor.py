from utils.brick import EV3GyroSensor, wait_ready_sensors

class GyroSensor:
    def __init__(self, sensor: EV3GyroSensor):
        wait_ready_sensors()
        self.sensor = sensor
        self.sensor.set_mode("abs")

    def get_angle(self) -> float:
        return self.sensor.get_abs_measure()
    
    
    