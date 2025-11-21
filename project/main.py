from color_sensor.color_sensor import ColorSensor
from gyro_sensor.gyro_sensor import GyroSensor
from utils.sound import Sound
from robot_delivery.delivery_system import DeliverySystem
from robot_movement.robot_movement import RobotMovement
from utils.brick import (
    EV3GyroSensor,
    Motor,
    TouchSensor,
    EV3ColorSensor,
    reset_brick,
    wait_ready_sensors,
)
from linetracking_system import linetracker, test_linetracker
import sys

from zone_detection.zone_detection import ZoneDetection

TOUCH1 = TouchSensor(1)
# TOUCH2 = TouchSensor(2)
COLOR = EV3ColorSensor(3)
GYRO = EV3GyroSensor(4)
MOTOR_LEFT = Motor("A")
MOTOR_RIGHT = Motor("D")
MOTOR_DELIVERY = Motor("C")
SOUND = Sound(1, 100, "C4")
wait_ready_sensors(True)


COLOR_SENSOR = ColorSensor(COLOR)
GYRO_SENSOR = GyroSensor(GYRO)

DELIVERY_SYSTEM = DeliverySystem(MOTOR_DELIVERY, COLOR_SENSOR, MOTOR_RIGHT, SOUND)
ROBOT_MOVEMENT = RobotMovement(MOTOR_LEFT, MOTOR_RIGHT, GYRO_SENSOR)
ZONE_DETECTION = ZoneDetection(COLOR_SENSOR, DELIVERY_SYSTEM, ROBOT_MOVEMENT)
line_tracker = linetracker.LineTracker(
    ROBOT_MOVEMENT, COLOR_SENSOR, GYRO, ZONE_DETECTION
)
line_tracker_test = test_linetracker.LineTrackingTest(line_tracker)


def main(test: str):
    # movement_test = robot_move_test.MovementTest(TOUCH1, TOUCH2, MOTOR1, MOTOR2)
    try:
        if test == "line":
            line_tracker_test = test_linetracker.LineTrackingTest(line_tracker)
            line_tracker_test.test(10, 10)
        elif test == "delivery":
            delivery_system = DeliverySystem(
                MOTOR_DELIVERY, COLOR_SENSOR, MOTOR_RIGHT, SOUND
            )
            zone_detection = ZoneDetection(
                COLOR_SENSOR, delivery_system, ROBOT_MOVEMENT
            )
            zone_detection.detect_zones()
            # delivery_system.deliver()
        elif test == "mvt":
            # movement_test = robot_move_test.MovementTest(TOUCH1, TOUCH2, MOTOR_LEFT, MOTOR_RIGHT)
            # movement_test.corner_turning_test(TURNING_POWER=25)
            pass
        else:
            print("what the helly is ts test")
    except BaseException:
        print("WHYYYYYYYYY hello world")
        pass
    finally:
        print("Done testing")
        COLOR_SENSOR.dispose()
        reset_brick()  # Turn off everything on the brick's hardware, and reset it
        exit()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        print("Arguments provided:", sys.argv[1:])
        main(sys.argv[1])
    else:
        print("Provide test: [line, delivery, mvt]")
