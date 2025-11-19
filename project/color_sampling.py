from time import sleep
<<<<<<< HEAD
from utils.brick import EV3ColorSensor, reset_brick, wait_ready_sensors, TouchSensor
=======
from utils.brick import EV3ColorSensor,configure_ports, reset_brick, wait_ready_sensors, TouchSensor
>>>>>>> main
from color_sensor.color_sensor import ColorSensor

DELAY_SEC = 0.01  # seconds of delay between measurements
DATA_FILE_BASE_PATH = "../data_analysis/color_data/"

# complete this based on your hardware setup
<<<<<<< HEAD
COLOR_SENSOR = EV3ColorSensor(1)
TOUCH_SENSOR = TouchSensor(2)
ANOTHER_TOUCHE = TouchSensor(3)
=======
TOUCH_SENSOR, COLOR_SENSOR , TOUCH_SENSOR2 = configure_ports(
    PORT_1=TouchSensor,
    PORT_2=EV3ColorSensor,
    PORT_3=TouchSensor
)
>>>>>>> main


def main():
    wait_ready_sensors(
        True
    )  # Input True to see what the robot is trying to initialize! False to be silent.
    print("Color Sensor is ready.")
    color_sensor = ColorSensor(COLOR_SENSOR)
<<<<<<< HEAD
    try:
        for color in ColorSensor.REFS.keys():
            collect_color_sensor_data(color, color_sensor)
    except BaseException:  # capture all exceptions including KeyboardInterrupt (Ctrl-C)
        print("error")
        pass
    finally:
        reset_brick()  # Turn off everything on the brick's hardware, and reset it
        exit()
=======
    for color in ColorSensor.REFS.keys():
        print("COLOR:", color)
        collect_color_sensor_data(color, color_sensor)

    reset_brick()  # Turn off everything on the brick's hardware, and reset it
    exit()
>>>>>>> main


def collect_color_sensor_data(color: str, color_sensor: ColorSensor):
    print("-=-=-=-=- Collect color data for", color, "-=-=-=-=-")
    file_output = f"{DATA_FILE_BASE_PATH}{color.lower()}.txt"
    output = []
<<<<<<< HEAD
    i = 0

    while not ANOTHER_TOUCHE.is_pressed():
=======
    
    while True:
        if TOUCH_SENSOR2.is_pressed():
            print("GOING TO NEXT COLOR BUTTON PRESS")
            while TOUCH_SENSOR2.is_pressed():
                sleep(DELAY_SEC)
            print("GOING TO NEXT COLOR")
            break
>>>>>>> main
        if TOUCH_SENSOR.is_pressed():
            print(f"Touch sensor pressed, collecting rgb data for {color}...")
            while TOUCH_SENSOR.is_pressed():
                r, g, b = color_sensor.get_rgb()
<<<<<<< HEAD
                if color_sensor.filter_data(
                    r, g, b
                ):  # If None is given, then data collection failed that time
                    i += 1
                    print(f"{color}: {i}")
                    output.append(f"{r}, {g}, {b}")
                sleep(DELAY_SEC)
            print("Touch sensor released, stopping data collection.")

    while ANOTHER_TOUCHE.is_pressed():
        sleep(DELAY_SEC)

    with open(file_output, "w") as file:
        file.write("\n".join(output))

=======
                if color_sensor.filter_data(r, g, b): # If None is given, then data collection failed that time
                    print(r, g, b)
                    output.append(f"{r}, {g}, {b}")
                sleep(DELAY_SEC)
            print("Touch sensor released, stopping data collection.")
            
    print("Writing to fie")
    with open(file_output, "w") as file:
        file.write("\n".join(output))
    print("WRITEN TO FILE")
    
>>>>>>> main

if __name__ == "__main__":
    main()
