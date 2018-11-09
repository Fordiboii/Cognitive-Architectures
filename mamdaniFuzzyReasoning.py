class MamdaniReasoning:
    def __init__(self):
        self.clip = 1.0
        self.distance = \
            {
                'VerySmall': (1.0, 2.5),
                'Small': (1.5, 3.0, 4.5),
                'Perfect': (3.5, 5.0, 6.5),
                'Big': (5.5, 7.0, 8.5),
                'VeryBig': (7.5, 9.0)
            }
        self.delta = \
            {
                'ShrinkingFast': (-4.0, -2.5),
                'Shrinking': (-3.5, -2.0, -0.5),
                'Stable': (-1.5, 0.0, 1.5),
                'Growing': (0.5, 2.0, 3.5),
                'GrowingFast': (2.5, 4.0)
            }
        self.action = \
            {
                'BrakeHard': (-8.0, -5.0),
                'SlowDown': (-7.0, -4.0, -1.0),
                'None': (-3.0, 0.0, 3.0),
                'SpeedUp': (1.0, 4.0, 7.0),
                'FloorIt': (5.0, 8.0)
            }

    def triangle(self, position, x0, x1, x2):
        value = 0.0
        if x2 < position < x0:
            return value
        elif x1 <= position >= x0:
            value = (position - x0)/(x1 - x0)
        elif x2 <= position >= x1:
            value = (position - x1)/(x2 - x1)

        # Check if value exceeds the clipping limit.
        if value > self.clip:
            value = self.clip
            return value
        else:
            return value

    def grade(self, position, x0, x1):
        value = 0.0
        if position < x0:
            return value
        elif position >= x1:
            value = self.clip
            return value
        else:
            value = (position-x0) / (x1-x0)

        # Check if value exceeds clipping limit.
        if value > self.clip:
            value = self.clip
            return value
        else:
            return value

    def reverse_grade(self, position, x0, x1):
        value = 0.0
        if position > x1:
            return value
        elif position <= x0:
            value = self.clip
            return value
        else:
            value = (x1 - position) / (x1 - x0)

        # Check if value exceeds clipping limit.
        if value > self.clip:
            value = self.clip
            return value
        else:
            return value
