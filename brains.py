import random
import math
from football_field import FIELD_WIDTH, FIELD_HEIGHT, GOAL_WIDTH, FIELD_MARGIN
MIN_SPACING = 20.0
REPULSION_FACTOR = 5.0

# TODO: Seperate the position brains to the perception ones. Position brains should adapt the perception brains depending on wht team they are on.
# TODO: Perception Brains can be like different tactics and they all each have their own team.

# TODO: Only the closest player should move towards the ball, everyone else moves relative to the position of the ball/teammates (maybe closest player=full speed, other teammates=half speed).
class ReactiveBrain:
    """ Moves the bot vertically toward the ball. Slows down when near the ball. """
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
    """ Always moves full-speed toward the ball vertically."""
    def think_and_act(self, percepts, x, y, sl, sr):
        if not percepts:
            return 0.0, 0.0
        ball_y = percepts['ball_y']
        if abs(ball_y - y) < 10:
            return 0.0, 0.0
        return (8.0, 8.0) if ball_y > y else (-8.0, -8.0)


class RandomWanderBrain:
    """ Ignores the ball and moves up/down randomly.Used for testing baseline performance. """
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
    """ Camps inside goal area and starts tracking the ball once it's within 100px in front of the goal."""
    #TODO: Goalkeeper needs to reposition back to middle of goal when the ball is within it's vision (18-yard box).
    def __init__(self, perception_type=None):
        self.perception_type = perception_type

    def think_and_act(self, percepts, x, y, sl, sr):
        if not percepts:
            return 0.0, 0.0

        ball_x = percepts['ball_x']
        ball_y = percepts['ball_y']
        goal_top = (FIELD_HEIGHT - GOAL_WIDTH) // 2
        goal_bottom = (FIELD_HEIGHT + GOAL_WIDTH) // 2
        goal_center_y = (goal_top + goal_bottom) // 2

        is_left_goalie = x < FIELD_WIDTH // 2
        track_zone_x = 300  # Track/vision zone

        # Determine if ball is in track zone
        if is_left_goalie:
            should_track = ball_x <= x + track_zone_x
        else:
            should_track = ball_x >= x - track_zone_x

        # Track the ball vertically if in zone and ball is within goal vertical range
        if should_track and goal_top <= ball_y <= goal_bottom:
            dy = ball_y - y
            if abs(dy) < 5:
                return 0.0, 0.0
            direction = 1 if dy > 0 else -1
            speed = min(6.0, max(2.0, abs(dy) / 10))
            return 0.0, direction * speed

        # If ball is outside the track zone, reposition to goal center
        dy = goal_center_y - y
        if abs(dy) < 5:
            return 0.0, 0.0  # Already at center or close enough
        direction = 1 if dy > 0 else -1
        speed = min(4.0, max(1.5, abs(dy) / 15))
        return 0.0, direction * speed


class StrikerBrain:
    """
    Striker AI that focuses on positioning and moving towards the ball. Shooting is handled in football_field.py.
    """
    def __init__(self, role='center_forward', perception_type=None):
        self.perception_type = perception_type
        self.role = role  # 'center_forward' or 'wide_forward'

    def think_and_act(self, percepts, x, y, sl, sr):
        if not percepts:
            return 0.0, 0.0
        ball_x = percepts['ball_x']
        ball_y = percepts['ball_y']
        dx = (ball_x - x) * 0.15
        dy = (ball_y - y) * 0.15
        speed = math.hypot(dx, dy)
        if speed > 8.0:
            dx = (dx / speed) * 8.0
            dy = (dy / speed) * 8.0
        return dx, dy


class DefenderBrain:
    def __init__(self, role='left_back', perception_type=None):
        self.role = role
        self.initialized = False
        self.perception_type = perception_type

    def setup(self, is_left_team):
        if is_left_team:
            if self.role == 'left_back':
                self.base_x = 200
                self.base_y = FIELD_HEIGHT // 4
            elif self.role == 'right_back':
                self.base_x = 200
                self.base_y = 3 * FIELD_HEIGHT // 4
        else:
            if self.role == 'left_back':
                self.base_x = FIELD_WIDTH - 200
                self.base_y = FIELD_HEIGHT // 4
            elif self.role == 'right_back':
                self.base_x = FIELD_WIDTH - 200
                self.base_y = 3 * FIELD_HEIGHT // 4

        self.initialized = True

    def think_and_act(self, percepts, x, y, sl, sr):
        if not percepts:
            return 0.0, 0.0

        ball_x = percepts['ball_x']
        ball_y = percepts['ball_y']
        teammates = percepts.get('teammates', [])
        ball_from_teammate = percepts.get('ball_from_teammate', False)

        is_left_team = x < FIELD_WIDTH // 2

        if not self.initialized:
            self.setup(is_left_team)

        # Determine if we're in possession based on ball_from_teammate
        team_has_possession = ball_from_teammate

        # 1. Calculate whether ball is inside defender's field of view
        if is_left_team:
            should_track = ball_x <= FIELD_WIDTH // 3
        else:
            should_track = ball_x >= 2 * FIELD_WIDTH // 3

        dx, dy = 0.0, 0.0

        # --- Always repel from teammates ---
        for mate_x, mate_y in teammates:
            dist_x = x - mate_x
            dist_y = y - mate_y
            dist = (dist_x ** 2 + dist_y ** 2) ** 0.5
            if dist < MIN_SPACING and dist > 0:
                dx += (dist_x / dist) * REPULSION_FACTOR
                dy += (dist_y / dist) * REPULSION_FACTOR

        if not should_track:
            # --- Ball is NOT in view -> Return to base ---
            move_dx, move_dy = self._move_towards(x, y, self.base_x, self.base_y)
            dx += move_dx
            dy += move_dy
            return dx, dy

        # --- Ball IS in view ---
        if team_has_possession:
            # When in possession, maintain more disciplined positioning
            # Right back stays on right, left back stays on left
            target_y = ball_y
            if self.role == 'right_back':
                target_y = max(FIELD_HEIGHT // 2, min(ball_y, 3 * FIELD_HEIGHT // 4))
            else:  # left_back
                target_y = min(FIELD_HEIGHT // 2, max(ball_y, FIELD_HEIGHT // 4))
            
            # Move towards target position with controlled speed
            vertical_diff = target_y - y
            if abs(vertical_diff) > 5:
                direction_y = 1 if vertical_diff > 0 else -1
                speed_y = min(5.0, max(2.0, abs(vertical_diff) / 10))  # Reduced speed when in possession
                dy += direction_y * speed_y
        else:
            # When defending, track more aggressively
            vertical_diff = ball_y - y
            if abs(vertical_diff) > 5:
                direction_y = 1 if vertical_diff > 0 else -1
                speed_y = min(7.0, max(2.0, abs(vertical_diff) / 10))
                dy += direction_y * speed_y

        return dx, dy

    def _move_towards(self, x, y, target_x, target_y):
        dx = target_x - x
        dy = target_y - y
        dist = (dx**2 + dy**2)**0.5
        if dist < 3:
            return 0.0, 0.0
        move_speed = min(5.0, dist / 5.0)
        return (dx / dist) * move_speed, (dy / dist) * move_speed


class MidfielderBrain:
    def __init__(self, perception_type=None):
        self.base_y = FIELD_HEIGHT // 2
        self.perception_type = perception_type

    def think_and_act(self, percepts, x, y, sl, sr):
        if not percepts:
            return 0.0, 0.0
        ball_x = percepts['ball_x']
        ball_y = percepts['ball_y']
        is_left_team = x < FIELD_WIDTH // 2
        dx = (ball_x - x) * 0.15
        dy = (ball_y - y) * 0.15
        speed = math.hypot(dx, dy)
        if speed > 7.0:
            dx = (dx / speed) * 7.0
            dy = (dy / speed) * 7.0
        return dx, dy


class FieldAwareBrain:
    """
    Adjusts tactics based on field position:
    - Aggressive in attacking half
    - Conservative in defensive half
    """
    def __init__(self, perception_type=None):
        self.perception_type = perception_type

    def think_and_act(self, percepts, x, y, sl, sr):
        if not percepts:
            return 0.0, 0.0

        ball_x = percepts['ball_x']
        ball_y = percepts['ball_y']
        dy = ball_y - y

        is_left_team = x < FIELD_WIDTH // 2
        in_attacking_half = ball_x > FIELD_WIDTH // 2 if is_left_team else ball_x < FIELD_WIDTH // 2

        if abs(dy) < 10:
            return 0.0, 0.0

        direction = 1 if dy > 0 else -1
        speed = 8.0 if in_attacking_half else 4.0
        return direction * speed, direction * speed