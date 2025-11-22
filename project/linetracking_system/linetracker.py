from zone_detection.zone_detection import ZoneDetection
from utils.brick import EV3GyroSensor, Motor, TouchSensor
from robot_movement.robot_movement import RobotMovement
from color_sensor.color_sensor import ColorSensor
from stop_button.stop_button import StopButton
from time import sleep


class LineTracker:
    stop_button: StopButton
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
        stop_button: StopButton,
    ):
        self.stop_button = stop_button
        self.robot_movement = robot_movement
        self.color_sensor = color_sensor
        self.isLeft = False
        self.gyro = gyro
        self.zone_detection = zone_detection

    def follow_line(self):
        R_POWER = 20
        L_POWER = 10

        self.robot_movement.adjust_speed(L_POWER, R_POWER)

        while True:
            if self.stop_button.was_pressed:
                self.robot_movement.adjust_speed(0, 0)
                print("STOP BUTTON PRESSED - STOPPING LINE TRACKING")
                break

            rgb = self.color_sensor.get_current_rgb()
            color = self.color_sensor.get_current_color()

            if color == "ORANGE" and self.zone_detection.enabled:
                self.zone_detection.detect_zone()
                self.robot_movement.adjust_speed(L_POWER, R_POWER)

            ratio = self.get_ratio(rgb)

            self.robot_movement.adjust_left_speed(
                L_POWER + (L_POWER / 2) * ratio / 0.16
            )

            if ratio > 0.8:
                self.turn_count += 1
                print(self.turn_count)

                if self.turn_count % 4 != 3:
                    self.turn_right(92)
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

    def turn_right(self, deg: int):
        print("turning right")
        self.robot_movement.intersection_turn_right(deg)
        self.zone_detection.enabled = True