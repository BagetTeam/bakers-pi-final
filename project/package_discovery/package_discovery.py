import math
from time import sleep
from color_sensor.color_sensor import ColorSensor
from gyro_sensor.gyro_sensor import GyroSensor
from robot_delivery.delivery_system import DeliverySystem
from robot_movement.robot_movement import RobotMovement


class PackageDiscovery:
    color_sensor: ColorSensor
    robot_movement: RobotMovement
    gyro_sensor: GyroSensor
    delivery_system: DeliverySystem

    def __init__(
        self,
        gyro_sensor: GyroSensor,
        color_sensor: ColorSensor,
        robot_movement: RobotMovement,
        delivery_system: DeliverySystem,
    ):
        self.color_sensor = color_sensor
        self.robot_movement = robot_movement
        self.gyro_sensor = gyro_sensor
        self.delivery_system = delivery_system

    def explore_room(self):
        BASE_L = 20
        BASE_R = 20
        advance_time = 0.5

        package_found = False
        advances = 0
        self.gyro_sensor.set_reference()
        print("GOING WITH REFERENCE:", self.gyro_sensor.get_reference())
        while not package_found and advances < 10:
            advances += 1
            print("Advance:", advances)
            # Check left
            print("Checking LEFT")
            package_found = self.look_sides(0, BASE_R, 70)
            self.robot_movement.adjust_speed(0, 0)
            sleep(0.2)
            if package_found:  # early exit
                break

            print("Checking RIGHT")
            # Check right
            package_found = self.look_sides(BASE_L, 0, 70)
            self.robot_movement.adjust_speed(0, 0)
            sleep(0.2)

            self.robot_movement.adjust_speed(10, 10)
            sleep(0.4)
            self.robot_movement.adjust_speed(0, 0)

        # Backtrack
        self.robot_movement.adjust_speed(-BASE_L, -BASE_R)
        while self.color_sensor.get_current_color() != "ORANGE":
            sleep(0.01)
        self.robot_movement.a_bit_forward()
        self.robot_movement.adjust_speed(0, 0)

        return package_found

    def look_sides(self, left_power: float, right_power: float, angle: float) -> bool:
        isRight = True if left_power > right_power else False
        MINN_SPEED = max(right_power, left_power)
        package_found = False

        self.robot_movement.adjust_speed(left_power, right_power)
        while abs(self.gyro_sensor.get_angle()) < abs(angle):
            if self.color_sensor.get_current_color() == "GREEN":
                package_found = True
                print("PACKAGE FOUUND")
                self.delivery_package()
                break
            sleep(0.01)
        sleep(0.5)

        while True:
            cur_angle = self.gyro_sensor.get_angle()

            if (isRight and cur_angle <= 0) or (not isRight and cur_angle >= 0):
                break

            speed_l = (
                0
                if left_power == 0
                else MINN_SPEED
                + (2 * left_power - MINN_SPEED) * math.sin(math.pi * cur_angle / angle)
            )
            speed_r = (
                0
                if right_power == 0
                else MINN_SPEED
                + (2 * right_power - MINN_SPEED) * math.sin(math.pi * cur_angle / angle)
            )

            self.robot_movement.adjust_speed(-speed_l, -speed_r)
            sleep(0.01)

        self.robot_movement.adjust_speed(10, 10)
        sleep(0.4)
        self.robot_movement.adjust_speed(0, 0)

        return package_found

    def delivery_package(self):
        self.robot_movement.adjust_speed(0, 0)
        sleep(0.2)
        self.robot_movement.adjust_speed(0, -20)
        sleep(1)
        self.robot_movement.adjust_speed(0, 0)
        sleep(0.5)
        self.delivery_system.deliver()
        sleep(0.5)
        self.robot_movement.adjust_speed(0, 20)
        sleep(1)
        self.robot_movement.adjust_speed(0, 0)
        sleep(0.2)
