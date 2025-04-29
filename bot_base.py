import math
import random
from football_field import FIELD_MARGIN, FIELD_HEIGHT, FIELD_WIDTH

class Bot:
    def __init__(self, x, y, team_color, brain):
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
        self.brain = brain
        self.color = 'red' if team_color == 'Red' else 'blue'

    def update(self, canvas, agents, objects):
        percepts = self.sense(objects)
        self.dx, self.dy = self.brain.think_and_act(
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
                'ball_dy': ball.dy
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