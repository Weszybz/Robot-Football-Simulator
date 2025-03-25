import math
import random

class ReactiveBrain:
    def think_and_act(self, percepts, x, y, sl, sr):
        if not percepts:
            return 1.0, 1.0  # Wander forward

        angle = percepts['angle_to_ball']
        dist = percepts['distance_to_ball']

        # Turn toward ball
        if angle > 0.1:
            return 1.5, -1.5
        elif angle < -0.1:
            return -1.5, 1.5
        else:
            # Go forward faster if closer to ball
            speed = min(5.0, max(1.0, 200.0 / (dist + 1)))
            return speed, speed

class RandomWanderBrain:
    def __init__(self):
        self.counter = 0
        self.turning = False

    def think_and_act(self, percepts, x, y, sl, sr):
        self.counter -= 1
        if self.counter <= 0:
            self.turning = not self.turning
            self.counter = random.randint(20, 60)

        if self.turning:
            return random.uniform(-2.0, 2.0), random.uniform(-2.0, 2.0)
        else:
            return 2.5, 2.5

class ChargeAtBallBrain:
    def think_and_act(self, percepts, x, y, sl, sr):
        if not percepts:
            return 0.0, 0.0

        angle = percepts['angle_to_ball']
        if abs(angle) < 0.05:
            return 5.0, 5.0  # Go straight
        elif angle > 0:
            return 1.5, -1.5  # Turn left
        else:
            return -1.5, 1.5  # Turn right
