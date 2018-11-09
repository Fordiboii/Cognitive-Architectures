class MamdaniReasoning:
    def __init__(self):
        self.distance = \
            {
                'VerySmall': (1, 2.5),
                'Small': (1.5, 3, 4.5),
                'Perfect': (3.5, 5, 6.5),
                'Big': (5.5, 7, 8.5),
                'VeryBig': (7.5, 9)
            }
        self.delta = \
            {
                'ShrinkingFast': (-4, -2.5),
                'Shrinking': (-3.5, -2, -0.5),
                'Stable': (-1.5, 0, 1.5),
                'Growing': (0.5, 2, 3.5),
                'GrowingFast': (2.5, 4)
            }
        self.action = \
            {
                'BrakeHard': (-8, -5),
                'SlowDown': (-7, -4, -1),
                'None': (-3, 0, 3),
                'SpeedUp': (1, 4, 7),
                'FloorIt': (5, 8)
            }
        