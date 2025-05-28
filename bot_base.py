import math
import random
from constants import FIELD_MARGIN, FIELD_HEIGHT, FIELD_WIDTH
from brains import GoalkeeperBrain, DefenderBrain

MIN_SPACING = 20.0
REPULSION_FACTOR = 5.0

class Bot:
    def __init__(self, x, y, team_color, position_brain, perception_brain):
        self.x = x
        self.y = y
        self.dx = 0.0
        self.dy = 0.0
        self.start_x = x  # Remember initial starting position
        self.start_y = y
        self.radius = 20
        self.theta = -math.pi / 2  # Not used in vertical-only mode
        self.speed_left = 0.0
        self.speed_right = 0.0
        self.team = team_color
        self.position_brain = position_brain
        self.perception_brain = perception_brain
        self.color = 'red' if team_color == 'Red' else 'blue'
        
        # Determine if this bot should use the separation rule based on its brain type
        self.uses_separation_rule = not isinstance(position_brain, GoalkeeperBrain)  # Goalkeepers don't use separation

    def update(self, canvas, agents, objects):
        # Use perception_brain to sense the world (teammates, opponents, ball, etc.)
        percepts = self.perception_brain.sense(self, agents, objects)
        # Add team and role info to percepts for use in brains
        percepts['team'] = self.team
        if hasattr(self.position_brain, 'role'):
            percepts['role'] = getattr(self.position_brain, 'role', None)
        # Add teammates and opponents as seen by perception (if not already present)
        if 'teammates' not in percepts:
            percepts['teammates'] = [(agent.x, agent.y) for agent in agents if agent.team == self.team and agent != self]
        if 'opponents' not in percepts:
            percepts['opponents'] = [(agent.x, agent.y) for agent in agents if agent.team != self.team]
        self.dx, self.dy = self.position_brain.think_and_act(
            percepts, self.x, self.y, self.speed_left, self.speed_right
        )
        self.move()

        canvas.create_oval(
            self.x - self.radius, self.y - self.radius,
            self.x + self.radius, self.y + self.radius,
            fill=self.color, tags='dynamic'
        )

    def sense(self, objects):
        ball = next((o for o in objects if hasattr(o, 'is_ball') and o.is_ball), None)
        if ball:
            dx = ball.x - self.x
            dy = ball.y - self.y
            dist = math.hypot(dx, dy)
            angle_to_ball = math.atan2(dy, dx)
            rel_angle = self._normalize_angle(angle_to_ball - self.theta)
            return {
                'distance_to_ball': dist,
                'angle_to_ball': rel_angle,
                'ball_x': ball.x,
                'ball_y': ball.y,
                'ball_dx': ball.dx,
                'ball_dy': ball.dy,
                'is_closest': False,  # You might update this externally
                'ball_visible': True,  # Assuming default for now
                'last_seen_ball': None,  # Only MemoryPerception fills this
                'shared_blackboard': {},  # Only BlackboardPerception uses this
                'ball_from_teammate': False
            }
        return {}

    def move(self):
        # Move both horizontally and vertically
        self.x += self.dx
        self.y += self.dy

        # Clamp inside field boundaries
        self.x = max(self.radius + FIELD_MARGIN, min(FIELD_WIDTH - self.radius - FIELD_MARGIN, self.x))
        self.y = max(self.radius + FIELD_MARGIN, min(FIELD_HEIGHT - self.radius - FIELD_MARGIN, self.y))

    def _normalize_angle(self, angle):
        while angle < -math.pi:
            angle += 2 * math.pi
        while angle > math.pi:
            angle -= 2 * math.pi
        return angle

    def reset(self):
        self.x = self.start_x
        self.y = self.start_y
        self.speed_left = 0.0
        self.speed_right = 0.0