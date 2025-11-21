from color_sensor.color_sensor import ColorSensor
from robot_movement.robot_movement import RobotMovement

class PackageDiscovery:
    color_sensor: ColorSensor
    robot_movement: RobotMovement

    def __init__(self, color_sensor: ColorSensor, robot_movement: RobotMovement):
        self.color_sensor = color_sensor
        self.robot_movement = robot_movement

    def explore_room(self):
        pass