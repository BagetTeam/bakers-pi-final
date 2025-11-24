import math
from threading import Thread
from time import sleep
from typing import Union
from utils.brick import EV3ColorSensor


class ColorSensor:
    sensor: EV3ColorSensor
    current_color: str
    cache: dict[str, tuple[float, float, float]] = {}
    thread: Thread
    thread_run: bool = True

    def __init__(self, sensor: EV3ColorSensor):
        print("initializing color sensor")
        self.sensor = sensor
        self.current_color = "UNKNOWN"
        self.init_cache()

        self.thread = Thread(target=self.main, args=[])
        self.thread.start()
        self.current_rgb: tuple[float, float, float] = (0, 0, 0)

    def init_cache(self):
        colors = ["red", "green", "blue", "yellow", "black", "white", "orange"]

        for color in colors:
            with open(f"../data_analysis/color_data/{color}.txt") as file:
                r_sum, g_sum, b_sum = 0, 0, 0

                rows = file.readlines()
                n = len(rows)
                for row in rows:
                    r, g, b = row.split(", ")
                    r_sum += int(r)
                    g_sum += int(g)
                    b_sum += int(b)

                self.cache[color.upper()] = self.__normalize_rgb(
                    (r_sum / n, g_sum / n, b_sum / n)
                )
                # (r_sum / n, g_sum / n, b_sum / n)

        print("cache initialized, ", self.cache)

    def main(self):
        while self.thread_run:
            _ = self.__detect_color()
            sleep(0.01)

    def get_rgb(self) -> tuple[float, float, float]:
        r, g, b = self.sensor.get_rgb()
        # self.sensor.wait_ready()
        return r, g, b

    def __set_rgb_color(self, rgb: tuple[float, float, float], color: str):
        self.current_rgb = self.__normalize_rgb(rgb)
        self.current_color = color

    def __normalize_rgb(
        self, rgb: tuple[float, float, float]
    ) -> tuple[float, float, float]:
        return rgb
        # total = sum(rgb)
        # if total == 0:
        #     return (0.0, 0.0, 0.0)
        # return rgb[0] / total, rgb[1] / total, rgb[2] / total

    def filter_data(
        self, r: Union[float, None], g: Union[float, None], b: Union[float, None]
    ):
        if r is not None and g is not None and b is not None:
            if r > 0 and g > 0 and b > 0:
                return True
        return False

    def __handle_threshold(self, color: str):
        return color

    def get_distance(self, rgb: tuple[float, float, float], target_color: str) -> float:
        if target_color not in self.cache:
            return -1.0
        (rr, gg, bb) = self.cache[target_color]
        r, g, b = rgb
        dist = math.sqrt((r - rr) ** 2 + (g - gg) ** 2 + (b - bb) ** 2)
        return dist

    def classify_color(self, rgb: tuple[float, float, float]) -> str:
        r, g, b = self.__normalize_rgb(rgb)
        color_found = "UNKNOWN"
        closest_dist = math.inf
        for name in self.cache.keys():
            dist = self.get_distance((r, g, b), name)
            if dist < closest_dist:
                closest_dist = dist
                color_found = name
        return color_found

    def __detect_color(self):
        r, g, b = self.get_rgb()
        if not self.filter_data(r, g, b):
            self.__set_rgb_color((r, g, b), "UNKNOWN")
            return "UNKNOWN"
        color_found = self.classify_color((r, g, b))
        color_found = self.__handle_threshold(color_found)
        # extra things

        self.__set_rgb_color((r, g, b), color_found)
        return color_found

    def get_current_color(self) -> str:
        return self.current_color

    def get_current_rgb(self) -> tuple[float, float, float]:
        return self.current_rgb

    def get_ratio(
        self,
        rgb: tuple[float, float, float],
        target1: str,
        target2: str
    ) -> float:
        dist_diff = self.color_sensor.get_distance(
            self.color_sensor.cache[target1], target2
        )

        diff = self.color_sensor.get_distance(rgb, target2)

        return diff / dist_diff
    
    def dispose(self):
        print("disposing color sensor")
        self.thread_run = False
        self.thread.join()
