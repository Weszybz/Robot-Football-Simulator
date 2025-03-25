import random
from football_field import FIELD_WIDTH, FIELD_HEIGHT, GOAL_WIDTH

class ReactiveBrain:
    """
    Moves the bot vertically toward the ball.
    Slows down when near the ball.
    """
    def think_and_act(self, percepts, x, y, sl, sr):
        if not percepts:
            return 0.0, 0.0

        ball_y = percepts['ball_y']
        dy = ball_y - y

        if abs(dy) < 10:
            return 0.0, 0.0  # Already close to the ball

        speed = min(8.0, max(2.0, abs(dy) / 10))
        direction = 1 if dy > 0 else -1
        return direction * speed, direction * speed


class ChargeAtBallBrain:
    """
    Always moves full-speed toward the ball vertically.
    """
    def think_and_act(self, percepts, x, y, sl, sr):
        if not percepts:
            return 0.0, 0.0

        ball_y = percepts['ball_y']
        if abs(ball_y - y) < 10:
            return 0.0, 0.0

        return (8.0, 8.0) if ball_y > y else (-8.0, -8.0)


class RandomWanderBrain:
    """
    Ignores the ball and moves up/down randomly.
    Used for testing baseline performance.
    """
    def __init__(self):
        self.counter = 0
        self.direction = 1

    def think_and_act(self, percepts, x, y, sl, sr):
        self.counter -= 1
        if self.counter <= 0:
            self.counter = random.randint(20, 60)
            self.direction = random.choice([-1, 1])
        return 5.0 * self.direction, 5.0 * self.direction


class GoalkeeperBrain:
    """
    Camps inside goal area and starts tracking the ball
    once it's within 100px in front of the goal.
    """
    def think_and_act(self, percepts, x, y, sl, sr):
        if not percepts:
            return 0.0, 0.0

        ball_x = percepts['ball_x']
        ball_y = percepts['ball_y']

        # Define vertical limits of goal area
        goal_top = (FIELD_HEIGHT - GOAL_WIDTH) // 2
        goal_bottom = (FIELD_HEIGHT + GOAL_WIDTH) // 2

        # Define tracking zone: start reacting if ball is nearby horizontally
        is_left_goalie = x < FIELD_WIDTH // 2
        track_zone_x = 200  # how far in front of the goal to start tracking

        if is_left_goalie:
            should_track = ball_x <= x + track_zone_x
        else:
            should_track = ball_x >= x - track_zone_x

        if not should_track:
            return 0.0, 0.0

        # Stay within goal posts vertically
        if ball_y < goal_top or ball_y > goal_bottom:
            return 0.0, 0.0

        # Move up or down to follow ball
        dy = ball_y - y
        if abs(dy) < 5:
            return 0.0, 0.0

        direction = 1 if dy > 0 else -1
        speed = min(6.0, max(2.0, abs(dy) / 10))
        return direction * speed, direction * speed


class StrikerBrain:
    """
    Smart offensive AI:
    - Moves vertically to align with ball
    - Gets behind the ball
    - When close, \"kicks\" ball toward goal by positioning
    """
    def think_and_act(self, percepts, x, y, sl, sr):
        if not percepts:
            return 0.0, 0.0

        ball_x = percepts['ball_x']
        ball_y = percepts['ball_y']
        dy = ball_y - y

        is_left_team = x < FIELD_WIDTH // 2
        behind_ball = (x < ball_x - 15) if is_left_team else (x > ball_x + 15)
        aligned_vertically = abs(dy) < 10

        if not aligned_vertically:
            direction = 1 if dy > 0 else -1
            speed = min(8.0, max(2.0, abs(dy) / 10))
            return direction * speed, direction * speed

        if behind_ball:
            # Move toward the ball for a push
            push_speed = 6.0 if is_left_team else -6.0
            return push_speed, push_speed
        else:
            # Already past the ball — back off
            return -2.0, -2.0 if is_left_team else (2.0, 2.0)