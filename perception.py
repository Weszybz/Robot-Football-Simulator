import math

class PerceptionBrain:
    def think_and_act(self, percepts, x, y, speed_left, speed_right):
        """
        Compute movement commands (dx, dy) based on the bot's perception.
        :param percepts: Dictionary from Bot.sense() including ball info
        :param x, y: Current bot position
        :return: dx, dy movement
        """
        raise NotImplementedError("Each brain must implement think_and_act()")

    def sense(self, bot, agents, objects):
        raise NotImplementedError("Each brain must implement sense()")


class FOVPerception(PerceptionBrain):
    def __init__(self, fov_angle=math.pi / 2, fov_range=200):
        self.fov_angle = fov_angle
        self.fov_range = fov_range

    def think_and_act(self, percepts, x, y, speed_left, speed_right):
        if not percepts:
            return 0, 0

        dist = percepts['distance_to_ball']
        angle = percepts['angle_to_ball']

        if dist < self.fov_range and abs(angle) < self.fov_angle / 2:
            # Move toward the ball
            dx = (percepts['ball_x'] - x) * 0.1
            dy = (percepts['ball_y'] - y) * 0.1
            return dx, dy
        else:
            # Idle or random lookaround
            return 0, 0
    def sense(self, bot, agents, objects):
        ball = next((o for o in objects if hasattr(o, 'is_ball') and o.is_ball), None)
        percepts = {}
        if ball:
            dx = ball.x - bot.x
            dy = ball.y - bot.y
            dist = math.hypot(dx, dy)
            angle_to_ball = math.atan2(dy, dx)
            rel_angle = ((angle_to_ball - bot.theta + math.pi) % (2 * math.pi)) - math.pi
            percepts = {
                'distance_to_ball': dist,
                'angle_to_ball': rel_angle,
                'ball_x': ball.x,
                'ball_y': ball.y,
                'ball_dx': ball.dx,
                'ball_dy': ball.dy
            }
        # Add field dimensions and team possession info if available
        from ball import FIELD_WIDTH, FIELD_HEIGHT
        percepts['field_width'] = FIELD_WIDTH
        percepts['field_height'] = FIELD_HEIGHT
        # Team possession info can be set externally if needed
        percepts['team_has_possession'] = getattr(bot, 'team_has_possession', False)
        return percepts

class MemoryPerception(PerceptionBrain):
    def __init__(self):
        self.last_seen_x = None
        self.last_seen_y = None

    def think_and_act(self, percepts, x, y, speed_left, speed_right):
        if percepts:
            self.last_seen_x = percepts['ball_x']
            self.last_seen_y = percepts['ball_y']

        if self.last_seen_x is not None:
            dx = (self.last_seen_x - x) * 0.1
            dy = (self.last_seen_y - y) * 0.1
            return dx, dy
        else:
            return 0, 0
    def sense(self, bot, agents, objects):
        ball = next((o for o in objects if hasattr(o, 'is_ball') and o.is_ball), None)
        if ball:
            dx = ball.x - bot.x
            dy = ball.y - bot.y
            dist = math.hypot(dx, dy)
            angle_to_ball = math.atan2(dy, dx)
            rel_angle = ((angle_to_ball - bot.theta + math.pi) % (2 * math.pi)) - math.pi
            return {
                'distance_to_ball': dist,
                'angle_to_ball': rel_angle,
                'ball_x': ball.x,
                'ball_y': ball.y,
                'ball_dx': ball.dx,
                'ball_dy': ball.dy
            }
        return {}


class Blackboard:
    def __init__(self):
        self.ball_position = None

shared_blackboard = Blackboard()

class BlackboardPerception(PerceptionBrain):
    def __init__(self, team_color):
        self.team = team_color

    def think_and_act(self, percepts, x, y, speed_left, speed_right):
        if percepts:
            shared_blackboard.ball_position = (percepts['ball_x'], percepts['ball_y'])

        if shared_blackboard.ball_position:
            bx, by = shared_blackboard.ball_position
            dx = (bx - x) * 0.1
            dy = (by - y) * 0.1
            return dx, dy
        return 0, 0

    def sense(self, bot, agents, objects):
        ball = next((o for o in objects if hasattr(o, 'is_ball') and o.is_ball), None)
        if ball:
            dx = ball.x - bot.x
            dy = ball.y - bot.y
            dist = math.hypot(dx, dy)
            angle_to_ball = math.atan2(dy, dx)
            rel_angle = ((angle_to_ball - bot.theta + math.pi) % (2 * math.pi)) - math.pi
            return {
                'distance_to_ball': dist,
                'angle_to_ball': rel_angle,
                'ball_x': ball.x,
                'ball_y': ball.y,
                'ball_dx': ball.dx,
                'ball_dy': ball.dy
            }
        return {}

# SubsumptionPerception: move toward ball, but if close, move toward opponent goal
class SubsumptionPerception(PerceptionBrain):
    def sense(self, bot, agents, objects):
        ball = next((o for o in objects if hasattr(o, 'is_ball') and o.is_ball), None)
        
        # Get opponent positions
        opponents = [(agent.x, agent.y) for agent in agents if agent.team != bot.team]
        
        if ball:
            dx = ball.x - bot.x
            dy = ball.y - bot.y
            dist = math.hypot(dx, dy)
            angle_to_ball = math.atan2(dy, dx)
            rel_angle = ((angle_to_ball - bot.theta + math.pi) % (2 * math.pi)) - math.pi
            return {
                'distance_to_ball': dist,
                'angle_to_ball': rel_angle,
                'ball_x': ball.x,
                'ball_y': ball.y,
                'ball_dx': ball.dx,
                'ball_dy': ball.dy,
                'opponents': opponents,  # Add opponents to percepts
                'field_width': globals().get('FIELD_WIDTH', 1000),
                'field_height': globals().get('FIELD_HEIGHT', 500),
                'team_has_possession': getattr(bot, 'team_has_possession', False)
            }
        return {'opponents': opponents, 'field_width': globals().get('FIELD_WIDTH', 1000), 'field_height': globals().get('FIELD_HEIGHT', 500), 'team_has_possession': getattr(bot, 'team_has_possession', False)}  # Return opponents even if ball not found

    def think_and_act(self, percepts, x, y, speed_left, speed_right):
        if not percepts:
            return 0, 0

        # Get ball info if available
        dist = percepts.get('distance_to_ball')
        ball_x = percepts.get('ball_x')
        ball_y = percepts.get('ball_y')

        # You may want to use a global or config for FIELD_WIDTH
        try:
            FIELD_WIDTH = globals().get('FIELD_WIDTH', 1000)
        except Exception:
            FIELD_WIDTH = 1000

        if dist and dist < 50:
            # Close to ball, switch to shooting toward opponent goal
            goal_x = FIELD_WIDTH if x < FIELD_WIDTH / 2 else 0
            dx = (goal_x - x) * 0.15
            dy = (ball_y - y) * 0.15
            return dx, dy
        elif ball_x and ball_y:
            # Chase the ball
            dx = (ball_x - x) * 0.1
            dy = (ball_y - y) * 0.1
            return dx, dy
        else:
            return 0, 0