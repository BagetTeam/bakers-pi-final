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

    def follow_line3(
        self,
        base_power: int = 30,
        correction_factor: int = 10,
        alpha: float = 1.0,
        threshold: float = 0.3,
        threshold_black: float = 0.6,
    ):
        # run a loop to continuously adjust motor speeds based on sensor reading

        while True:
            color = self.color_sensor.get_current_color()

            if color != "BLACK" and color != "WHITE":
                continue

            rgb = self.color_sensor.get_current_rgb()
            print(color)

            dist_to_black = self.color_sensor.get_distance(rgb, "BLACK")
            dist_to_white = self.color_sensor.get_distance(rgb, "WHITE")

            # Calculate Blackness Ratio (0.0 = White, 1.0 = Black)
            total_dist = dist_to_white + dist_to_black
            if total_dist == 0:
                total_dist = 0.001  # Analyze prevent division by zero

            blackness = dist_to_white / total_dist

            # adjust motor speeds based on the normalized blackness ratio
            if blackness < threshold:
                # on white (ratio is low), slight left (turn towards the line)
                # To turn left: Right motor > Left motor
                self.robot_movement.adjust_speed(
                    base_power, base_power + correction_factor
                )
            if blackness >= threshold_black:
                # a line is being crossed, we should turn 90 deg
                self.robot_movement.intersection_turn_right(power=base_power)
                sleep(2)  # wait for the turn to complete
            else:
                # on black/edge, turn right proportionally to how black it is
                turn_strength = blackness * alpha
                self.robot_movement.adjust_speed(base_power + turn_strength, base_power)

            sleep(0.01)

    def follow_line2(self):
        R_POWER = 20
        L_POWER = 10

        self.robot_movement.adjust_speed(L_POWER, R_POWER)

        while True:
            rgb = self.color_sensor.get_current_rgb()

            ratio = self.get_ratio(rgb)

            self.robot_movement.adjust_left_speed(
                L_POWER + (L_POWER / 2) * ratio / 0.20
            )

            if ratio > 0.8:
                self.turn_count += 1

                if self.turn_count % 4 != 3:
                    self.turn_right()
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
        self.zone_detection.detect_zone()
