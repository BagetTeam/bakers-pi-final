from utils.brick import Motor
from robot_movement.robot_movement import RobotMovement
from color_sensor.color_sensor import ColorSensor
from time import sleep


class LineTracker(RobotMovement):
    def __init__(
        self, left_motor: Motor, right_motor: Motor, color_sensor: ColorSensor
    ):
        super().__init__(left_motor, right_motor)
        self.color_sensor = color_sensor
        self.isLeft = False

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
                self.adjust_speed(base_power, base_power + correction_factor)
            if blackness >= threshold_black:
                # a line is being crossed, we should turn 90 deg
                self.intersection_turn_right(power=base_power)
                sleep(2)  # wait for the turn to complete
            else:
                # on black/edge, turn right proportionally to how black it is
                turn_strength = blackness * alpha
                self.adjust_speed(base_power + turn_strength, base_power)
            sleep(0.01)
