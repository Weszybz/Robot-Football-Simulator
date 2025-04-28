import random
import math
from football_field import FIELD_WIDTH, FIELD_HEIGHT, GOAL_WIDTH
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
    def think_and_act(self, percepts, x, y, sl, sr):
        if not percepts:
            return 0.0, 0.0

        ball_x = percepts['ball_x']
        ball_y = percepts['ball_y']
        goal_top = (FIELD_HEIGHT - GOAL_WIDTH) // 2
        goal_bottom = (FIELD_HEIGHT + GOAL_WIDTH) // 2
        goal_center_y = (goal_top + goal_bottom) // 2

        is_left_goalie = x < FIELD_WIDTH // 2
        track_zone_x = 200  # Track/vision zone

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
            return direction * speed, direction * speed

        # If ball is outside the track zone, reposition to goal center
        dy = goal_center_y - y
        if abs(dy) < 5:
            return 0.0, 0.0  # Already at center or close enough
        direction = 1 if dy > 0 else -1
        speed = min(4.0, max(1.5, abs(dy) / 15))
        return direction * speed, direction * speed


class StrikerBrain:
    """
    Smart offensive AI:
    - Moves vertically to align with ball
    - Gets behind the ball
    - When close, "kicks" ball toward goal by positioning
    """

    # TODO: Striker needs to be aim at the goal everytime.
    def think_and_act(self, percepts, x, y, sl, sr):
        if not percepts:
            return 0.0, 0.0

        ball_x = percepts['ball_x']
        ball_y = percepts['ball_y']
        ball_dx = percepts.get('ball_dx', 0.0)
        ball_dy = percepts.get('ball_dy', 0.0)

        is_left_team = x < FIELD_WIDTH // 2
        goal_x = FIELD_WIDTH if is_left_team else 0
        goal_top = (FIELD_HEIGHT - GOAL_WIDTH) // 2
        goal_bottom = (FIELD_HEIGHT + GOAL_WIDTH) // 2
        goal_center_y = (goal_top + goal_bottom) // 2

        # Predict when ball will reach striker's x
        if ball_dx == 0:
            predicted_ball_y = ball_y
        else:
            time_to_reach = (x - ball_x) / ball_dx
            if time_to_reach < 0:
                predicted_ball_y = ball_y
            else:
                predicted_ball_y = ball_y + ball_dy * time_to_reach
                # Bounce handling
                bounces = 0
                while predicted_ball_y < 0 or predicted_ball_y > FIELD_HEIGHT:
                    if predicted_ball_y < 0:
                        predicted_ball_y = -predicted_ball_y
                    elif predicted_ball_y > FIELD_HEIGHT:
                        predicted_ball_y = 2 * FIELD_HEIGHT - predicted_ball_y
                    bounces += 1
                    if bounces > 2:
                        break

        # Calculate desired vertical offset based on goal alignment
        dx_to_goal = goal_x - x
        dy_to_goal = goal_center_y - predicted_ball_y
        desired_deflection_angle = math.atan2(dy_to_goal, dx_to_goal)

        # Let's increase the offset for stronger deflection control
        # Also scale based on distance to goal for better accuracy
        distance_to_goal = abs(goal_x - x)
        offset_magnitude = 25.0 * math.sin(desired_deflection_angle) * (distance_to_goal / FIELD_WIDTH)

        desired_y = predicted_ball_y + offset_magnitude

        # Debug output
        # print(f"Ball Y: {ball_y}, Predicted Ball Y: {predicted_ball_y}, Desired Y: {desired_y}, Striker Y: {y}")
        # print(f"Offset: {offset_magnitude}, Angle to Goal: {math.degrees(desired_deflection_angle)}")

        dy = desired_y - y
        aligned_vertically = abs(dy) < 5

        if not aligned_vertically:
            direction = 1 if dy > 0 else -1
            speed = min(8.0, max(2.0, abs(dy) / 10))
            return direction * speed, direction * speed

        ball_close = abs(ball_x - x) < 25
        if ball_close:
            push_speed = 6.0 if is_left_team else -6.0
            return push_speed, push_speed

        return 0.0, 0.0


class DefenderBrain:
    def __init__(self, role='left_back'):
        self.role = role
        if role == 'left_back':
            self.x_min, self.x_max = 0, FIELD_WIDTH // 4
            self.base_x, self.base_y = 80, FIELD_HEIGHT // 4
        elif role == 'right_back':
            self.x_min, self.x_max = FIELD_WIDTH // 4, FIELD_WIDTH // 2
            self.base_x, self.base_y = 80, 3 * FIELD_HEIGHT // 4
        else:
            self.x_min, self.x_max = 0, FIELD_WIDTH // 2
            self.base_x, self.base_y = 80, FIELD_HEIGHT // 2

    def think_and_act(self, percepts, x, y, sl, sr):
        if not percepts:
            return 0.0, 0.0

        ball_x = percepts['ball_x']
        ball_y = percepts['ball_y']
        teammates = percepts.get('teammates', [])

        is_left_team = x < FIELD_WIDTH // 2
        track_zone_x = FIELD_WIDTH // 4  # Defenders track only in defensive quarter

        # Determine if ball is in vision/track zone
        if is_left_team:
            should_track = ball_x <= track_zone_x
        else:
            should_track = ball_x >= FIELD_WIDTH - track_zone_x

        # If not tracking, return to base
        if not should_track:
            return self._move_towards(x, y, self.base_x, self.base_y)

        dx, dy = 0.0, 0.0

        # Stay in horizontal zone
        if x < self.x_min:
            dx += 2.0
        elif x > self.x_max:
            dx -= 2.0

        # Repel from teammates
        for mate_x, mate_y in teammates:
            dist_x = x - mate_x
            dist_y = y - mate_y
            dist = (dist_x**2 + dist_y**2)**0.5
            if dist < 20.0 and dist > 0:
                dx += (dist_x / dist) * 5.0
                dy += (dist_y / dist) * 5.0

        # Track the ball vertically
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
    """
    Facilitates passes and transitions:
    - Aligns with ball within vision zone
    - Returns to base position when ball is out of vision
    """

    def __init__(self):
        self.base_x = FIELD_WIDTH // 2
        self.base_y = FIELD_HEIGHT // 2

    def think_and_act(self, percepts, x, y, sl, sr):
        if not percepts:
            return 0.0, 0.0

        ball_x = percepts['ball_x']
        ball_y = percepts['ball_y']

        # Define vision zone: middle third
        vision_min_x = FIELD_WIDTH // 3
        vision_max_x = 2 * FIELD_WIDTH // 3
        in_vision_zone = vision_min_x <= ball_x <= vision_max_x

        # 1. If ball is out of vision -> go back to base
        if not in_vision_zone:
            return self._move_towards(x, y, self.base_x, self.base_y)

        # 2. Ball is in vision -> align vertically with ball
        dy = ball_y - y
        aligned_vertically = abs(dy) < 10

        if not aligned_vertically:
            direction = 1 if dy > 0 else -1
            speed = min(7.0, max(2.0, abs(dy) / 10))
            return direction * speed, direction * speed

        # 3. Aligned -> push forward
        is_left_team = x < FIELD_WIDTH // 2
        push_speed = 4.0 if is_left_team else -4.0
        return push_speed, push_speed

    def _move_towards(self, x, y, target_x, target_y):
        dx = target_x - x
        dy = target_y - y
        dist = (dx**2 + dy**2)**0.5
        if dist < 3:
            return 0.0, 0.0  # Close enough to base
        move_speed = min(5.0, dist / 5.0)  # Faster return to base
        return (dx / dist) * move_speed, (dy / dist) * move_speed


class FieldAwareBrain:
    """
    Adjusts tactics based on field position:
    - Aggressive in attacking half
    - Conservative in defensive half
    """
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