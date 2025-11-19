from time import sleep
from color_sensor.color_sensor import ColorSensor
from robot_movement.robot_movement import RobotMovement
from robot_delivery.delivery_system import DeliverySystem
from utils.brick import EV3ColorSensor, Motor, reset_brick, wait_ready_sensors

motor = Motor("C")
left_motor = Motor("A")
right_motor = Motor("D")
sensor = EV3ColorSensor(3)
wait_ready_sensors(True)

color_sensor = ColorSensor(sensor)
robot_movement = RobotMovement(left_motor, right_motor)
delivery_system = DeliverySystem(motor, color_sensor, robot_movement)


def main():
    try:
        delivery_system.deliver()
    except BaseException:
        print("exception")
        pass
    finally:
        color_sensor.dispose()
        reset_brick()


if __name__ == "__main__":
    main()
