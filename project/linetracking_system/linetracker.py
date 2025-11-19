from utils.brick import Motor, EV3ColorSensor
from robot_movement.robot_movement import RobotMovement
from color_sensor.color_sensor import ColorSensor
from time import sleep

class LineTracker(RobotMovement):
    def __init__(self, left_motor: Motor, right_motor: Motor, color_sensor: ColorSensor):
        super().__init__(left_motor, right_motor)
        self.color_sensor = color_sensor
        self.isLeft = False

    def follow_line(self, base_power: int = 30, correction_factor: int = 10):
        """
        Adjusts motor speeds based on sensor reading to follow a line.
        
        :param sensor_reading: An integer representing the line sensor's reading.
                               Typically, lower values indicate the line is centered,
                               while higher values indicate deviation.
        :param base_power: The base power level for the motors.
        :param correction_factor: A factor to adjust the speed difference between motors.
        """
        
        # get the color sensor value from the color sensor thread
        # use it to calibrate the middle brightness value.
        # adjust
        # convert color sensor value to a range between -100 to 100

        previous_color = -1
        while True:
            color = self.color_sensor.get_color_detected()
            if color == "BLACK":
                self.adjust_speed(0, 0)
                self.change_relative_angle(correction_factor, -correction_factor)
                sleep(0.1)
                previous_color = 0
            elif color == "WHITE" and previous_color != 1:
                self.adjust_speed(base_power, base_power + 5)
                previous_color = 1
            sleep(0.01)

    def follow_line2(self, base_power: int = 30):
        left_speed_adjust = [-5, 15]
        while True:
            color = self.color_sensor.get_color_detected()
            if color == "BLACK":
                dist_black = self.color_sensor.get_distance(self.color_sensor.get_rgb(), "BLACK")
                if dist_black < 0.1:
                    self.intersection_turn_right()
                self.adjust_speed(base_power + left_speed_adjust[1], base_power)
            elif color == "WHITE":
                self.adjust_speed(base_power + left_speed_adjust[0], base_power)

        
    def follow_line3(self, base_power: int = 30, correction_factor: int = 10, alpha: float = 1.0, threshold: float = 0.3):
        # run a loop to continuously adjust motor speeds based on sensor reading

        white_ref, black_ref = self.color_sensor.cache["WHITE"], self.color_sensor.cache["BLACK"]
        
        def euclidean_distance(rgb1, rgb2):
            return sum((a - b) ** 2 for a, b in zip(rgb1, rgb2)) ** 0.5

        while True:
            # Unpack the values: current rgb, white reference, black reference
            # Note: get_rgb_detected returns (rgb, white, black)
            # We use a throwaway variable for the refs since we cached them above, 
            # or we could just use get_rgb() if available. 
            rgb, _, _ = self.color_sensor.get_rgb_detected()
            
            dist_to_black = euclidean_distance(rgb, black_ref)
            dist_to_white = euclidean_distance(rgb, white_ref)
            
            # Calculate Blackness Ratio (0.0 = White, 1.0 = Black)
            total_dist = dist_to_white + dist_to_black
            if total_dist == 0: 
                total_dist = 0.001 # Analyze prevent division by zero
                
            blackness = dist_to_white / total_dist

            # adjust motor speeds based on the normalized blackness ratio
            if blackness < threshold:
                # on white (ratio is low), slight left (turn towards the line)
                # To turn left: Right motor > Left motor
                self.adjust_speed(base_power, base_power + correction_factor)
            else:
                # on black/edge, turn right (away from the line)
                # Proportional to how "black" it is.
                # blackness increases as we get deeper into the line
                turn_strength = blackness * alpha
                self.adjust_speed(base_power + turn_strength, base_power)
            
