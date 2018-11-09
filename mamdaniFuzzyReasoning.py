import numpy as np

class MamdaniReasoning:
    def __init__(self):
        self.samplePoints = np.arange(0, 10.5, 0.5).tolist()
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

    def triangle(self, position, x0, x1, x2, clip):
        value = 0.0
        if (position < x0) or (position > x2):
            return value
        elif (position >= x0) and (position <= x1):
            value = (position - x0)/(x1 - x0)
        elif (position >= x1) and (position <= x2):
            value = (x2 - position)/(x1 - x0)
        # Check if value exceeds the clipping limit.
        if value > clip:
            value = clip
        return value

    def grade(self, position, x0, x1, clip):
        value = 0.0
        if position < x0:
            return value
        elif position >= x1:
            value = clip
            return value
        else:
            value = (position-x0) / (x1-x0)

        # Check if value exceeds clipping limit.
        if value > clip:
            value = clip
        return value

    def reverse_grade(self, position, x0, x1, clip):
        value = 0.0
        if position > x1:
            return value
        elif position <= x0:
            value = clip
            return value
        else:
            value = (x1 - position) / (x1 - x0)

        # Check if value exceeds clipping limit.
        if value > clip:
            value = clip
        return value

    def rule_1(self, distPosition, deltaPosition):
        # If distance is SMALL and delta is GROWING then action is NONE

        smallFuzzyResult = self.triangle(
            distPosition,
            self.distance['Small'][0],
            self.distance['Small'][1],
            self.distance['Small'][2],
            1.0
        )
        growingFuzzyResult = self.triangle(
            deltaPosition,
            self.delta['Growing'][0],
            self.delta['Growing'][1],
            self.delta['Growing'][2],
            1.0
        )
        return min(smallFuzzyResult, growingFuzzyResult), 'None'

    def rule_2(self, distPosition, deltaPosition):
        # If distance is SMALL and delta is STABLE then action is SLOWDOWN

        smallFuzzyResult = self.triangle(
            distPosition,
            self.distance['Small'][0],
            self.distance['Small'][1],
            self.distance['Small'][2],
            1.0
        )
        stableFuzzyResult = self.triangle(
            deltaPosition,
            self.delta['Stable'][0],
            self.delta['Stable'][1],
            self.delta['Stable'][2],
            1.0
        )
        return min(smallFuzzyResult, stableFuzzyResult), 'SlowDown'

    def rule_3(self, distPosition, deltaPosition):
        # If distance is PERFECT and delta is GROWING then action is SPEEDUP

        perfectFuzzyResult = self.triangle(
            distPosition,
            self.distance['Perfect'][0],
            self.distance['Perfect'][1],
            self.distance['Perfect'][2],
            1.0
        )
        growingFuzzyResult = self.triangle(
            deltaPosition,
            self.delta['Growing'][0],
            self.delta['Growing'][1],
            self.delta['Growing'][2],
            1.0
        )
        return min(perfectFuzzyResult, growingFuzzyResult), 'SpeedUp'

    def rule_4(self, distPosition, deltaPosition):
        # If distance is VERYBIG and (delta is NOT GROWING or delta is NOT GROWINGFAST) then action is FLOORIT

        veryBigFuzzyResult = self.grade(
            distPosition,
            self.distance['VeryBig'][0],
            self.distance['VeryBig'][1],
            1.0
        )
        growingFuzzyResult = self.triangle(
            deltaPosition,
            self.delta['Growing'][0],
            self.delta['Growing'][1],
            self.delta['Growing'][2],
            1.0
        )
        growingFastFuzzyResult = self.grade(
            deltaPosition,
            self.delta['GrowingFast'][0],
            self.delta['GrowingFast'][1],
            1.0
        )

        if growingFuzzyResult > 0.0 and growingFastFuzzyResult > 0.0:
            return 0.0, 'FloorIt'
        else:
            deltaValue = 1.0

        return min(veryBigFuzzyResult, deltaValue), 'FloorIt'

    def rule_5(self, distPosition, deltaPosition):
        # If distance is VERYSMALL then action is BRAKEHARD

        verySmallFuzzyResult = self.reverse_grade(
            distPosition,
            self.distance['VerySmall'][0],
            self.distance['VerySmall'][1],
            1.0
        )
        return verySmallFuzzyResult, 'BrakeHard'

    def action_clipped_samples(self, resultAndAction):
        clip = resultAndAction(0)
        ruleAction = resultAndAction(1)
        if ruleAction == 'BrakeHard':
            return [
                ( pos,
                self.reverse_grade(
                    pos,
                    self.action['BrakeHard'][0],
                    self.action['BrakeHard'][1],
                    clip
                )
                  ) for pos in self.samplePoints
                ]
        elif ruleAction == 'SlowDown':
            pass
        elif ruleAction == 'None':
            pass
        elif ruleAction == 'SpeedUp':
            pass
        else:



mam = MamdaniReasoning()
print("rule 1: ", mam.rule_1(3.7, 1.2))
print("rule 2: ", mam.rule_2(3.7, 1.2))
print("rule 3: ", mam.rule_3(3.7, 1.2))
print("rule 4: ", mam.rule_4(3.7, 1.2))
print("rule 5: ", mam.rule_5(3.7, 1.2))

rules_res = []
rules_res.append(mam.rule_1(3.7, 1.2))
rules_res.append(mam.rule_2(3.7, 1.2))
rules_res.append(mam.rule_3(3.7, 1.2))
rules_res.append(mam.rule_4(3.7, 1.2))
rules_res.append(mam.rule_5(3.7, 1.2))