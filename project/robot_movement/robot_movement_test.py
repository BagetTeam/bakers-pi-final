from time import sleep
from robot_movement import robot_movement as rbt_mvt

class MovementTest:
    def __init__(self, touch_sensor1, touch_sensor2, motor1, motor2):
        self.touch1 = touch_sensor1
        self.touch2 = touch_sensor2
        self.robot_movement = rbt_mvt.RobotMovement(motor1, motor2)

    def intersection_turning_test(self, TURNING_POWER):
        RIGHT_SENSOR = self.touch1
        LEFT_SENSOR = self.touch2

        # Main loop: runs indefinitely
        while True: 
            while RIGHT_SENSOR.is_pressed():
                self.robot_movement.intersection_turn_right(TURNING_POWER)
                sleep(0.1)
            while LEFT_SENSOR.is_pressed():
                self.robot_movement.intersection_turn_left(TURNING_POWER)
                sleep(0.1)
            self.robot_movement.stop_move()

    def corner_turning_test(self, TURNING_POWER):
        RIGHT_SENSOR = self.touch1
        LEFT_SENSOR = self.touch2

        # Main loop: runs indefinitely
        while True: 
            while RIGHT_SENSOR.is_pressed():
                self.robot_movement.corner_turn_right(TURNING_POWER)
                sleep(0.1)
            while LEFT_SENSOR.is_pressed():
                self.robot_movement.corner_turn_left(TURNING_POWER)
                sleep(0.1)
            self.robot_movement.stop_move()

    def forward_backward_test(self, FWD_POWER):
        FORWARD_SENSOR = self.touch1
        BACKWARD_SENSOR = self.touch2

        # Main loop: runs indefinitely
        while True: 
            while FORWARD_SENSOR.is_pressed():
                self.robot_movement.move_straight(FWD_POWER)
                sleep(0.1)
            while BACKWARD_SENSOR.is_pressed():
                self.robot_movement.move_straight(-FWD_POWER)
                sleep(0.1)
            self.robot_movement.stop_move()
