from utils.brick import (
    Motor,
    TouchSensor,
    reset_brick,
    wait_ready_sensors,
    configure_ports,
)
from robot_movement import robot_movement_test as robot_move_test

TOUCH1, TOUCH2, MOTOR1, MOTOR2 = configure_ports(
    PORT_1=TouchSensor,
    PORT_2=TouchSensor,
    PORT_A=Motor,
    PORT_D=Motor,
    wait=True,
    print_status=True,
)

def main():
    movement_test = robot_move_test.MovementTest(TOUCH1, TOUCH2, MOTOR1, MOTOR2)

    try:
        movement_test.corner_turning_test(TURNING_POWER=25)
    except BaseException:
        pass
    finally:
        print("Done testing")
        reset_brick()  # Turn off everything on the brick's hardware, and reset it
        exit()

if __name__ == "__main__":
    main()