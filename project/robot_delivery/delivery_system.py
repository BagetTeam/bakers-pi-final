from time import sleep
from color_sensor.color_sensor import ColorSensor
from robot_movement.robot_movement import RobotMovement
from utils.brick import Motor, wait_ready_sensors


class DeliverySystem:
    delivery_motor: Motor
    sensor: ColorSensor
    movement: RobotMovement

    is_active: bool = True
    deg: int = 0
    has_first_been_pushed = False

    def __init__(self, motor: Motor, sensor: ColorSensor, movement: RobotMovement):
        print("initializing delivery system")

        self.delivery_motor = motor
        self.sensor = sensor
        self.movement = movement
        self.delivery_motor.reset_encoder()  # Ensure we start from position 0

    def deliver(self):
        print("DELIVERING")
        color = self.sensor.get_current_color()
        print(color)

        # if color == "GREEN":
        self.move_back()
        sleep(1)
        self.push()

    def move_back(self, power: int = 50, duration: float = 0):
        print("moving back")
        self.movement.set_limits(20)
        self.movement.change_relative_angle(0, -20)

        while self.movement.is_robot_motor_moving():
            sleep(0.2)

    # piston-like delivery system
    def push(self, power: int = 50, duration: float = 0.5):
        print("pushing thing")
        angle = 360 if self.has_first_been_pushed else 180
        self.delivery_motor.set_position_relative(angle)
        self.delivery_motor.wait_is_stopped()
        self.has_first_been_pushed = True

        self.movement.change_relative_angle(0, 20)
