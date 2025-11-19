from time import sleep
from utils.brick import Motor, wait_ready_sensors


class DeliverySystem:
    delivery_motor: Motor
    left_motor: Motor
    right_motor: Motor
    is_active: bool = True
    deg: int = 0
    has_first_been_pushed = False

    def __init__(self, motor: Motor, left_motor: Motor, right_motor: Motor):
        self.delivery_motor = motor
        self.left_motor = left_motor
        self.right_motor = right_motor
        self.delivery_motor.reset_encoder()  # Ensure we start from position 0

    def move_back(self, power: int = 50, duration: float = 0):
        self.right_motor.set_position(-100)
        self.right_motor.wait_is_stopped()

    # piston-like delivery system
    def push(self, power: int = 50, duration: float = 0.5):
        angle = 360 if self.has_first_been_pushed else 180
        self.delivery_motor.set_position_relative(angle)
        self.delivery_motor.wait_is_stopped()
