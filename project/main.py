from utils.brick import (
    Motor,
    reset_brick,
    wait_ready_sensors,
    TouchSensor,
)
from robot_movement import robot_movement_test as robot_move_test

TOUCH1 = TouchSensor(1)
TOUCH2 = TouchSensor(2)
MOTOR1 = Motor("A")
MOTOR2 = Motor("D")

def main():
    wait_ready_sensors(True)
    print("Done waiting")
    movement_test = robot_move_test.MovementTest(TOUCH1, TOUCH2, MOTOR1, MOTOR2)


    try:
        movement_test.turning_test(TURNING_POWER=25)
    except BaseException:
        pass
    finally:
        print("Done testing")
        reset_brick()  # Turn off everything on the brick's hardware, and reset it
        exit()

if __name__ == "__main__":
    main()