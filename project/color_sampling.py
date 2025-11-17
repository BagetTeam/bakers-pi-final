from time import sleep
from utils.brick import EV3ColorSensor,configure_ports, reset_brick, wait_ready_sensors, TouchSensor
from color_sensor import ColorSensor

DELAY_SEC = 0.01  # seconds of delay between measurements
DATA_FILE_BASE_PATH = "../data_analysis/color_data/"

# complete this based on your hardware setup
TOUCH_SENSOR, COLOR_SENSOR , TOUCH_SENSOR2 = configure_ports(
    PORT_1=TouchSensor,
    PORT_2=EV3ColorSensor,
    PORT_3=TouchSensor
)


def main():
    wait_ready_sensors(True) # Input True to see what the robot is trying to initialize! False to be silent.
    print("Color Sensor is ready.")
    color_sensor = ColorSensor(COLOR_SENSOR)
    try:
        for color in ColorSensor.REFS.keys():
            collect_color_sensor_data(color, color_sensor)
    except BaseException:  # capture all exceptions including KeyboardInterrupt (Ctrl-C)
        pass
    finally:
        reset_brick()  # Turn off everything on the brick's hardware, and reset it
        exit()

def collect_color_sensor_data(color: str, color_sensor: ColorSensor):
    print("-=-=-=-=- Collect color data for", color, "-=-=-=-=-")
    file_output = f"{DATA_FILE_BASE_PATH}{color.lower()}.txt"
    output = []
    
    while True:
        if TOUCH_SENSOR2.is_pressed():
            while TOUCH_SENSOR2.is_pressed():
                sleep(DELAY_SEC)
            break
        if TOUCH_SENSOR.is_pressed():
            print(f"Touch sensor pressed, collecting rgb data for {color}...")
            while TOUCH_SENSOR.is_pressed():
                r, g, b = color_sensor.get_rgb()
                if color_sensor.filter_data(r, g, b): # If None is given, then data collection failed that time
                    output.append(f"{r}, {g}, {b}")
                sleep(DELAY_SEC)
            print("Touch sensor released, stopping data collection.")
            

    with open(file_output, "w") as file:
        file.write("\n".join(output))

    

if __name__ == "__main__":
    main()
