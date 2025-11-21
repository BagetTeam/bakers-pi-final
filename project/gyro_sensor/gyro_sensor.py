from utils.brick import EV3GyroSensor

class GyroSensor:
    sensor: EV3GyroSensor
    reference: float

    def __init__(self, sensor: EV3GyroSensor):
        self.sensor = sensor
        self.sensor.set_mode("abs")
        self.reference = 0.0

    def get_angle(self) -> float:
        return self.sensor.get_abs_measure() - self.reference
    
    def set_reference(self):
        self.reference = self.sensor.get_abs_measure()

    def set_reference(self, reference: float):
        self.reference = reference
        
    def get_reference(self):
        return self.reference
