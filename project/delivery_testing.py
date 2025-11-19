from time import sleep
from color_sensor.color_sensor import ColorSensor
from utils.sound import Sound
from robot_movement.robot_movement import RobotMovement
from robot_delivery.delivery_system import DeliverySystem
from zone_detection.zone_detection import ZoneDetection
from utils.brick import EV3ColorSensor, Motor, reset_brick, wait_ready_sensors

motor = Motor("C")
left_motor = Motor("A")
right_motor = Motor("D")
sensor = EV3ColorSensor(3)
wait_ready_sensors(True)

color_sensor = ColorSensor(sensor)
sound = Sound(duration=1, pitch="C4", volume=150)
delivery_system = DeliverySystem(motor, color_sensor, right_motor, sound)
movement = RobotMovement(left_motor, right_motor)
zone_detection = ZoneDetection(color_sensor, delivery_system, movement)


def main():
    try:
        zone_detection.detect_zones()
        # delivery_system.deliver()
    except BaseException:
        print("WHYYYYYYYYY")
        pass
    finally:
        color_sensor.dispose()
        reset_brick()
        exit()


if __name__ == "__main__":
    main()
