from color_sensor.color_sensor import ColorSensor
from utils.brick import (
    Motor,
    TouchSensor,
    EV3ColorSensor,
    reset_brick,
    configure_ports,
    wait_ready_sensors,
)
from robot_movement import robot_movement_test as robot_move_test
from linetracking_system import linetracker, test_linetracker

TOUCH1 = TouchSensor(1)
COLOR = EV3ColorSensor(3)
MOTOR1 = Motor("A")
MOTOR2 = Motor("D")
wait_ready_sensors(True)

COLOR_SENSOR = ColorSensor(COLOR)


def main():
    # movement_test = robot_move_test.MovementTest(TOUCH1, TOUCH2, MOTOR1, MOTOR2)
    line_tracker = linetracker.LineTracker(MOTOR1, MOTOR2, COLOR_SENSOR)
    line_tracker_test = test_linetracker.LineTrackingTest(line_tracker)
    try:
        line_tracker_test.test(10, 10)
        # movement_test.corner_turning_test(TURNING_POWER=25)
    except BaseException:
        print("WHYYYYYYYYY")
        pass
    finally:
        print("Done testing")
        reset_brick()  # Turn off everything on the brick's hardware, and reset it
        exit()


if __name__ == "__main__":
    main()
