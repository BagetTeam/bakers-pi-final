import math
from threading import Thread
from time import sleep
from typing import Union
from utils.brick import EV3GyroSensor


class GyroSensor:
    sensor: EV3GyroSensor
    current_angle: float # degrees
    cache: dict = {}
    thread: Thread
    thread_run: bool = True

    def __init__(self, sensor: EV3GyroSensor):
        print("initializing gyro sensor")
        self.sensor = sensor
        # self.current_angle = 
        self.init_cache()
                
        self.sensor.set_mode("abs")
        self.thread = Thread(target=self.main, args=[])
        self.thread.start()
        self.current_angle: float = 0.0

    def init_cache(self):
        # No cache needed for gyro sensor, but method included for consistency
        self.cache['REF'] = self.sensor.get_abs_measure()
    
    def main(self):
        while self.thread_run:
            _ = self.__get_angle()
            sleep(0.01)

    def __get_angle(self) -> float:
        return self.sensor.get_abs_measure() - self.cache['REF']
    
    def get_current_angle(self) -> float:
        return self.current_angle
    
    def set_reference(self):
        self.reference = self.sensor.get_abs_measure()

    def dispose(self):
        print("disposing gyro sensor")
        self.thread_run = False
        self.thread.join()