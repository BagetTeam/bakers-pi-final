import math
from threading import Thread
from time import sleep
from typing import Union
from utils.brick import TouchSensor


class StopButton:
    sensor: TouchSensor 
    was_pressed: bool = False
    thread: Thread
    thread_run: bool = True

    def __init__(self, sensor: TouchSensor):
        print("initializing stop button")
        self.sensor = sensor
        self.thread = Thread(target=self.main, args=[])
        self.thread.start()

    def main(self):
        while self.thread_run:
            if(self.sensor.is_pressed()):
                self.was_pressed = True
            sleep(0.01)

    def dispose(self):
        print("disposing color sensor")
        self.thread_run = False
        self.thread.join()