from color_sensor.color_sensor import ColorSensor
from robot_movement.robot_movement import RobotMovement

class PackageDiscovery:
    color_sensor: ColorSensor
    robot_movement: RobotMovement

    def __init__(self, color_sensor: ColorSensor, robot_movement: RobotMovement):
        self.color_sensor = color_sensor
        self.robot_movement = robot_movement

    def explore_room(self):
        BASE_L = 20
        BASE_R = 20

        for advances in range(5):
            self.robot_movement.adjust_speed(0, BASE_R)

            self.robot_movement.adjust_speed(BASE_L, 0)

            

