from zone_detection.zone_detection import ZoneDetection
from utils.brick import EV3GyroSensor, Motor
from robot_movement.robot_movement import RobotMovement
from color_sensor.color_sensor import ColorSensor
from time import sleep


class LineTracker:
    color_sensor: ColorSensor
    robot_movement: RobotMovement
    gyro: EV3GyroSensor
    isLeft: bool
    zone_detection: ZoneDetection
    turn_count: int = 0
    orqnge_count: int = 0

    def __init__(
        self,
        robot_movement: RobotMovement,
        color_sensor: ColorSensor,
        gyro: EV3GyroSensor,
        zone_detection: ZoneDetection,
    ):
        self.robot_movement = robot_movement
        self.color_sensor = color_sensor
        self.isLeft = False
        self.gyro = gyro
        self.zone_detection = zone_detection

    def follow_line2(self):
        R_POWER = 30
        L_POWER = 15

        self.robot_movement.adjust_speed(L_POWER, R_POWER)

        while True:
            rgb = self.color_sensor.get_current_rgb()
            color = self.color_sensor.get_current_color()

            if color == "ORANGE":
                self.robot_movement.adjust_speed(0, 0)
                self.zone_detection.detect_zone()

            ratio = self.get_ratio(rgb)

            self.robot_movement.adjust_left_speed(
                L_POWER + (L_POWER / 2) * ratio / 0.16
            )

            if ratio > 0.8:
                self.turn_count += 1
                print(self.turn_count)

                if self.turn_count % 4 != 3:
                    self.turn_right()
                    sleep(0.1)
                    self.robot_movement.adjust_speed(L_POWER, R_POWER)
                else:
                    self.robot_movement.adjust_speed(R_POWER, R_POWER)
                    sleep(1)
                    self.robot_movement.adjust_speed(L_POWER, R_POWER)

            sleep(0.01)

    def get_ratio(
        self,
        rgb: tuple[float, float, float],
    ) -> float:
        dist_diff = self.color_sensor.get_distance(
            self.color_sensor.cache["BLACK"], "WHITE"
        )

        diff = self.color_sensor.get_distance(rgb, "WHITE")

        return diff / dist_diff

    def turn_right(self):
        print("turning right")
        self.robot_movement.intersection_turn_right()
        self.zone_detection.enabled = True
