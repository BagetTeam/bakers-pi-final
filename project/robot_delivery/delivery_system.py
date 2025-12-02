from time import sleep
from color_sensor.color_sensor import ColorSensor
from utils.brick import Motor
# from utils.sound import Sound


class DeliverySystem:
    delivery_motor: Motor
    sensor: ColorSensor
    # sound: Sound

    is_active: bool = True
    deg: int = 0
    has_first_been_pushed = False

    def __init__(self, motor: Motor, sensor: ColorSensor, right_motor: Motor):
        print("initializing delivery system")

        self.delivery_motor = motor
        self.delivery_motor.set_limits(20)
        self.right_motor = right_motor
        self.sensor = sensor

        self.delivery_motor.reset_encoder()  # Ensure we start from position 0

    def deliver(self):
        print("DELIVERING")
        self.push()

    # piston-like delivery system
    def push(self):
        print("pushing thing")
        if self.has_first_been_pushed:
            self.delivery_motor.set_position(0)
            sleep(1)

        self.delivery_motor.set_position(-95)
        sleep(1)
        self.has_first_been_pushed = True

    def reset(self):
        self.delivery_motor.set_position(0)
        sleep(1)
