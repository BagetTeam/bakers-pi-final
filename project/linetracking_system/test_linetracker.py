from linetracking_system.linetracker import LineTracker

class LineTrackingTest:
    def __init__(self, linetracking: LineTracker):
        self.linetracking = linetracking
    
    def test(self, base_power, correction_factor):
        self.linetracking.follow_line(base_power=base_power, correction_factor=correction_factor)