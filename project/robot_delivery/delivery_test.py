from time import sleep
import delivery_system as deliv_sys

ROTATE_BUTTON = TouchSensor(1);
MOTOR = Motor("A")

class DeliveryTest:
    def __init__(self, motor):
        self.delivery_system = deliv_sys.DeliverySystem(motor)

    def rotate_test(self, ROTATE_POWER = 10, ROTATE_TIME = 1.0):
        # Main loop: runs indefinitely
        while True: 
            while ROTATE_BUTTON.is_pressed():
                sleep(0.1)
            self.delivery_system.rotate(ROTATE_POWER, ROTATE_TIME)
            while not ROTATE_BUTTON.is_pressed():
                sleep(0.1)

    def push_test(self, PUSH_POWER = 50, PUSH_TIME = 0.5):
        # Main loop: runs indefinitely
        while True: 
            while ROTATE_BUTTON.is_pressed():
                sleep(0.1)
            self.delivery_system.push(PUSH_POWER, PUSH_TIME)
            while not ROTATE_BUTTON.is_pressed():
                sleep(0.1)


# power const
ROTATE_POWER = 10
ROTATE_TIME = 1.0
PUSH_POWER = 50

CUR_MODE = "ROTATE"  # ROTATE or PUSH

wait_ready_sensors(True)
print("Done waiting")

def main() :
    try:
        # Main loop: runs indefinitely
        while True: 
            if CUR_MODE == "PUSH":
                while ROTATE_BUTTON.is_pressed():
                    sleep(0.1)
                delivery_system.push(PUSH_POWER, ROTATE_TIME/2)
                while not ROTATE_BUTTON.is_pressed():
                    sleep(0.1)
                    
            elif CUR_MODE == "ROTATE":
                while ROTATE_BUTTON.is_pressed():
                    sleep(0.1)
                delivery_system.rotate(ROTATE_POWER, ROTATE_TIME)
                while not ROTATE_BUTTON.is_pressed():
                    sleep(0.1)
            
    except BaseException:
        pass
    finally:
        print("Done testing")
        reset_brick()  # Turn off everything on the brick's hardware, and reset it
        exit()

if __name__ == "__main__":
    main()


