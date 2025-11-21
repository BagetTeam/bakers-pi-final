from time import sleep
from color_sensor.color_sensor import ColorSensor
from robot_movement.robot_movement import RobotMovement
from utils.brick import Motor, wait_ready_sensors
from utils.sound import Sound


class DeliverySystem:
    delivery_motor: Motor
    sensor: ColorSensor
    sound: Sound

    is_active: bool = True
    deg: int = 0
    has_first_been_pushed = False

    def __init__(
        self, motor: Motor, sensor: ColorSensor, right_motor: Motor, sound: Sound
    ):
        print("initializing delivery system")

        self.delivery_motor = motor
        self.delivery_motor.set_limits(30)
        self.right_motor = right_motor
        self.sensor = sensor
        self.sound = sound

        self.delivery_motor.reset_encoder()  # Ensure we start from position 0

    def deliver(self):
        print("DELIVERING")
        color = self.sensor.get_current_color()
        print(color)

        self.push()

        self.sound.play()
        self.sound.wait_done()
        # self.right_motor.wait_is_stopped()

    # piston-like delivery system
    def push(self, power: int = 50, duration: float = 0.5):
        print("pushing thing")
        if self.has_first_been_pushed:
            self.delivery_motor.set_position(0)
            sleep(2)

        self.delivery_motor.set_position(135)
        sleep(2)
        self.has_first_been_pushed = True
