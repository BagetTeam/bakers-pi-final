from color_sensor.color_sensor import ColorSensor
from robot_delivery.delivery_system import DeliverySystem
from robot_movement.robot_movement import RobotMovement
from utils.brick import (
    Motor,
    TouchSensor,
    EV3ColorSensor,
    reset_brick,
    wait_ready_sensors,
)
from robot_movement import robot_movement_test as robot_move_test
from linetracking_system import test_linetracker
import sys

from utils.sound import Sound
from zone_detection.zone_detection import ZoneDetection

TOUCH1 = TouchSensor(1)
TOUCH2 = TouchSensor(2)
COLOR = EV3ColorSensor(3)
MOTOR_LEFT = Motor("A")
MOTOR_RIGHT = Motor("D")
MOTOR_DELIVERY = Motor("C")

SOUND = Sound(duration=1, pitch="C4", volume=150)
wait_ready_sensors(True)

COLOR_SENSOR = ColorSensor(COLOR)
ROBOT_MOVEMENT = RobotMovement(MOTOR_LEFT, MOTOR_RIGHT)


def main(test: str = ""):
    try:
        if test == "line":
            line_tracker_test = test_linetracker.LineTrackingTest(ROBOT_MOVEMENT, COLOR_SENSOR)
            line_tracker_test.test(10, 10)
        elif test == "delivery":
            delivery_system = DeliverySystem(MOTOR_DELIVERY, COLOR_SENSOR, MOTOR_RIGHT, SOUND)
            zone_detection = ZoneDetection(COLOR_SENSOR, delivery_system, ROBOT_MOVEMENT)
            zone_detection.detect_zones()
        elif test == "mvt":   
            movement_test = robot_move_test.MovementTest(TOUCH1, TOUCH2, MOTOR_LEFT, MOTOR_RIGHT)
            movement_test.corner_turning_test(TURNING_POWER=25)
        else:
            print("what the helly is ts test")
    except BaseException:
        print("WHYYYYYYYYY")
        pass
    finally:
        print("Done testing")
        reset_brick()  # Turn off everything on the brick's hardware, and reset it
        exit()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        print("Arguments provided:", sys.argv[1:])
        main(sys.argv[1])
    else:
        print("Provide test: [line, delivery, mvt]")
