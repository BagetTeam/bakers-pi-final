from utils.brick import Motor, EV3ColorSensor
from robot_movement.robot_movement import RobotMovement
from color_sensor.color_sensor import ColorSensor
from time import sleep

class LineTracker(RobotMovement):
    def __init__(self, left_motor: Motor, right_motor: Motor, color_sensor: ColorSensor):
        super().__init__(left_motor, right_motor)
        self.color_sensor = color_sensor
        self.isLeft = False

    def follow_line(self, base_power: int = 30, correction_factor: float = 10.0):
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