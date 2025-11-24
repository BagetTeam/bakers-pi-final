from gyro_sensor.gyro_sensor import GyroSensor
from zone_detection.zone_detection import ZoneDetection
from robot_movement.robot_movement import RobotMovement
from color_sensor.color_sensor import ColorSensor
from stop_button.stop_button import StopButton
from time import sleep


class LineTracker:
    stop_button: StopButton
    color_sensor: ColorSensor
    robot_movement: RobotMovement
    gyro: GyroSensor
    isLeft: bool
    zone_detection: ZoneDetection
    turn_count: int = 0
    orqnge_count: int = 0

    def __init__(
        self,
        robot_movement: RobotMovement,
        color_sensor: ColorSensor,
        gyro: GyroSensor,
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
        R_POWER = 30
        L_POWER = 20

        self.robot_movement.adjust_speed(L_POWER, R_POWER)
        n_delivery = 0

        while True:
            rgb = self.color_sensor.get_current_rgb()
            color = self.color_sensor.get_current_color()

            if color == "ORANGE" and self.zone_detection.enabled:
                if n_delivery == 2:
                    self.robot_movement.adjust_speed(R_POWER, R_POWER)
                    sleep(0.5)
                    raise Exception("Done")

                if self.zone_detection.detect_zone():
                    n_delivery += 1
                self.robot_movement.adjust_speed(L_POWER, R_POWER)

            ratio = self.get_ratio(rgb)

            self.robot_movement.adjust_left_speed(
                L_POWER + (L_POWER / 2) * (ratio**2) / 0.20
            )

            if ratio > 0.80:
                self.turn_count += 1
                print(self.turn_count)

                if self.turn_count % 4 != 3:
                    if n_delivery == 2 and self.turn_count == 13:
                        self.robot_movement.adjust_speed(R_POWER + 5, R_POWER)
                        sleep(0.2)
                        self.robot_movement.adjust_speed(L_POWER, R_POWER)
                        self.turn_count += 1
                    else:
                        self.turn_right(90)
                        sleep(0.1)
                        self.robot_movement.adjust_speed(L_POWER, R_POWER)
                else:
                    if n_delivery == 2:
                        if self.turn_count == 7 or self.turn_count == 15:
                            self.turn_right(90)
                    else:
                        self.robot_movement.adjust_speed(R_POWER + 5, R_POWER)
                        sleep(0.2)
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

        if any(i == self.turn_count for i in [1, 5, 8, 13]):
            self.robot_movement.intersection_turn_right(deg)
        else:
            self.robot_movement.adjust_speed(30, -5)
            self.gyro.set_reference()

            seen_white = False
            seen_black = False

            while True:
                color = self.color_sensor.get_current_color()

                if color == "WHITE":
                    if seen_white and seen_black:
                        break

                    seen_white = True

                if seen_white and color == "BLACK":
                    seen_black = True

                sleep(0.01)

        self.zone_detection.enabled = True
