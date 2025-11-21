from time import sleep
from color_sensor.color_sensor import ColorSensor
from gyro_sensor.gyro_sensor import GyroSensor
from robot_movement.robot_movement import RobotMovement


class PackageDiscovery:
    color_sensor: ColorSensor
    robot_movement: RobotMovement
    gyro_sensor: GyroSensor

    def __init__(
        self,
        gyro_sensor: GyroSensor,
        color_sensor: ColorSensor,
        robot_movement: RobotMovement,
    ):
        self.color_sensor = color_sensor
        self.robot_movement = robot_movement
        self.gyro_sensor = gyro_sensor

    def explore_room(self):
        BASE_L = 20
        BASE_R = 20

        package_found = False
        advances = 0
        self.gyro_sensor.set_reference()
        print("GOING WITH REFERENCE:", self.gyro_sensor.get_angle())
        while not package_found and advances < 5:
            advances += 1
            print("Advance:", advances)
            # Check left
            print("Checking LEFT")
            self.robot_movement.adjust_speed(0, BASE_R)
            while self.gyro_sensor.get_angle() > -70:
                if self.color_sensor.get_current_color == "GREEN":
                    package_found = True
                    print("PACKAGE FOUUND")
                    break
            print("Turning back LEFT")
            self.robot_movement.adjust_speed(0, -BASE_R)
            while self.gyro_sensor.get_angle() < 0:
                sleep(0.1)

            if package_found:  # early exit
                break

            print("Checking RIGHT")
            # Check right
            self.robot_movement.adjust_speed(BASE_L, 0)
            while self.gyro_sensor.get_angle() < 70:
                if self.color_sensor.get_current_color == "GREEN":
                    package_found = True
                    print("PACKAGE FOUUND")
                    break
            print("Turning back RIGHT")
            self.robot_movement.adjust_speed(-BASE_L, 0)
            while self.gyro_sensor.get_angle() > 0:
                sleep(0.1)

            # Advance
            self.robot_movement.adjust_speed(BASE_L, BASE_R)
            sleep(0.7)
            self.robot_movement.adjust_speed(0, 0)
