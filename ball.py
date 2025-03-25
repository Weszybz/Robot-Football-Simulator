import math
import random

FIELD_WIDTH = 1000
FIELD_HEIGHT = 600
GOAL_WIDTH = 200

class Ball:
    def __init__(self):
        self.radius = 10
        self.is_ball = True
        self.reset()

    def reset(self):
        self.x = FIELD_WIDTH // 2
        self.y = FIELD_HEIGHT // 2
        angle = random.uniform(0, 2 * math.pi)
        speed = 6.0
        self.dx = speed * math.cos(angle)
        self.dy = speed * math.sin(angle)

    def update(self, canvas):
        self.x += self.dx
        self.y += self.dy

        # Bounce off top/bottom walls
        if self.y - self.radius <= 0 or self.y + self.radius >= FIELD_HEIGHT:
            self.dy *= -1

        # Bounce off left/right walls if not in goal area
        if self.x - self.radius <= 0:
            if not ((FIELD_HEIGHT - GOAL_WIDTH)//2 <= self.y <= (FIELD_HEIGHT + GOAL_WIDTH)//2):
                self.dx *= -1
        elif self.x + self.radius >= FIELD_WIDTH:
            if not ((FIELD_HEIGHT - GOAL_WIDTH)//2 <= self.y <= (FIELD_HEIGHT + GOAL_WIDTH)//2):
                self.dx *= -1

        # Draw
        canvas.create_oval(
            self.x - self.radius, self.y - self.radius,
            self.x + self.radius, self.y + self.radius,
            fill='white', tags='dynamic')
