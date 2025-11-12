from time import sleep
from utils.brick import Motor, wait_ready_sensors

class DeliverySystem:
    def __init__(self, motor: Motor):
        wait_ready_sensors()
        self.motor = motor

    # windmill-like delivery system
    def rotate(self, power: int = 10, duration: float = 1.0):
        self.motor.set_power(power)
        sleep(duration)
        self.motor.set_power(0)



    # piston-like delivery system
    def push(self, power: int = 50, duration: float = 0.5):
        self.motor.set_power(power)
        sleep(duration)
        self.motor.set_power(-power)
        sleep(duration)
        self.motor.set_power(0)