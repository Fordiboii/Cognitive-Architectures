import numpy as np

class MamdaniReasoning:
    def __init__(self):
        self.samplePoints = np.arange(-10, 10.5, 0.5).tolist()
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

    def rule_5(self, distPosition):
        # If distance is VERYSMALL then action is BRAKEHARD

        verySmallFuzzyResult = self.reverse_grade(
            distPosition,
            self.distance['VerySmall'][0],
            self.distance['VerySmall'][1],
            1.0
        )
        return verySmallFuzzyResult, 'BrakeHard'

    def generate_clipped_action_fuzzy_set(self, resultAndAction):
        clip = resultAndAction[0]
        ruleAction = resultAndAction[1]

        if ruleAction == 'BrakeHard':
            return {
                pos:
                self.reverse_grade(
                    pos,
                    self.action[ruleAction][0],
                    self.action[ruleAction][1],
                    clip
                )
                for pos in self.samplePoints
            }
        elif ruleAction == 'FloorIt':
            return {
                pos:
                self.grade(
                    pos,
                    self.action[ruleAction][0],
                    self.action[ruleAction][1],
                    clip
                )
                for pos in self.samplePoints
            }
        else:
            return {
                pos:
                self.triangle(
                    pos,
                    self.action[ruleAction][0],
                    self.action[ruleAction][1],
                    self.action[ruleAction][2],
                    clip
                )
                for pos in self.samplePoints
            }

    def aggregate_action_sets(self, action_sets):
        aggregateDict = {}
        for point in self.samplePoints:
            value = 0
            for set in action_sets:
                value = max(value, set[point])
            aggregateDict[point] = value
        return aggregateDict

    def centre_of_gravity(self, aggregatedActionDict):
        values = [aggregatedActionDict[key]*key for key in aggregatedActionDict]
        numerator = sum(values)
        denominator = sum(aggregatedActionDict[key] for key in aggregatedActionDict)
        return numerator / denominator


distance = 3.7
delta = 1.2

mam = MamdaniReasoning()

# Save the rule results
rules_res = []
rules_res.append(mam.rule_1(distance, delta))
rules_res.append(mam.rule_2(distance, delta))
rules_res.append(mam.rule_3(distance, delta))
rules_res.append(mam.rule_4(distance, delta))
rules_res.append(mam.rule_5(distance))

# Print all rules and their results
ruleNo = 1
for rule in rules_res:
    print("rule " + str(ruleNo) + ": ", rule)
    ruleNo += 1

# Generate all clipped action fuzzy sets.
action_sets = [mam.generate_clipped_action_fuzzy_set(ruleResult) for ruleResult in rules_res]

# Generate aggregate of all action sets
aggregate = mam.aggregate_action_sets(action_sets)

# Print centre of gravity
print(mam.centre_of_gravity(aggregate))
