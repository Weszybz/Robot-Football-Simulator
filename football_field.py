import tkinter as tk
import time
import random

FIELD_WIDTH = 1000
FIELD_HEIGHT = 600
GOAL_WIDTH = 200

class FootballField:

    def _draw_pitch(self):
        # Midline
        self.canvas.create_line(
            FIELD_WIDTH // 2, 0, FIELD_WIDTH // 2, FIELD_HEIGHT,
            fill='white', dash=(10, 6), width=2, tags='static'
        )

        # 18-yard box
        self.canvas.create_line(FIELD_WIDTH // 4, (FIELD_HEIGHT // 6), FIELD_WIDTH // 4, 5 * (FIELD_HEIGHT // 6), fill='white', width=2, tags='static')
        self.canvas.create_line(0, (FIELD_HEIGHT // 6), FIELD_WIDTH // 4, (FIELD_HEIGHT // 6),
                                fill='white', width=2, tags='static')
        self.canvas.create_line(0, 5 * (FIELD_HEIGHT // 6), FIELD_WIDTH // 4, 5 * (FIELD_HEIGHT // 6),
                                fill='white', width=2, tags='static')

        self.canvas.create_line(3*(FIELD_WIDTH // 4), (FIELD_HEIGHT // 6), 3 * (FIELD_WIDTH // 4), 5 * (FIELD_HEIGHT // 6), fill='white', width =2, tags='static')
        self.canvas.create_line(3 * (FIELD_WIDTH // 4), (FIELD_HEIGHT // 6), FIELD_WIDTH, (FIELD_HEIGHT // 6),
                                fill='white', width=2, tags='static')
        self.canvas.create_line(3 * (FIELD_WIDTH // 4), 5 * (FIELD_HEIGHT // 6), FIELD_WIDTH, 5 * (FIELD_HEIGHT // 6),
                                fill='white', width=2, tags='static')

        # Penalty spot
        self.canvas.create_oval(
            FIELD_WIDTH // 6, FIELD_HEIGHT // 2,
            FIELD_WIDTH // 6, FIELD_HEIGHT // 2,
            outline='white', width=8, tags='static'
        )
        self.canvas.create_oval(
            5 * FIELD_WIDTH // 6, FIELD_HEIGHT // 2,
            5 * FIELD_WIDTH // 6, FIELD_HEIGHT // 2,
            outline='white', width=8, tags='static'
        )

        # 6-yard box
        self.canvas.create_line(FIELD_WIDTH // 12, (FIELD_HEIGHT // 3.5), FIELD_WIDTH // 12, 2.5 * (FIELD_HEIGHT // 3.5),
                                fill='white', width=2, tags='static')
        self.canvas.create_line(0, (FIELD_HEIGHT // 3.5), FIELD_WIDTH // 12, (FIELD_HEIGHT // 3.5),
                                fill='white', width=2, tags='static')
        self.canvas.create_line(0, 2.5 * (FIELD_HEIGHT // 3.5), FIELD_WIDTH // 12, 2.5 * (FIELD_HEIGHT // 3.5),
                                fill='white', width=2, tags='static')

        self.canvas.create_line(11 * FIELD_WIDTH // 12, (FIELD_HEIGHT // 3.5), 11 * FIELD_WIDTH // 12,
                                2.5 * (FIELD_HEIGHT // 3.5),
                                fill='white', width=2, tags='static')
        self.canvas.create_line(11 * FIELD_WIDTH // 12, (FIELD_HEIGHT // 3.5), FIELD_WIDTH, (FIELD_HEIGHT // 3.5),
                                fill='white', width=2, tags='static')
        self.canvas.create_line(11 * FIELD_WIDTH // 12, 2.5 * (FIELD_HEIGHT // 3.5), FIELD_WIDTH, 2.5 * (FIELD_HEIGHT // 3.5),
                                fill='white', width=2, tags='static')

        # Goals
        self.canvas.create_rectangle(
            0, (FIELD_HEIGHT - GOAL_WIDTH) // 2,
            10, (FIELD_HEIGHT + GOAL_WIDTH) // 2,
            fill='white', tags='static'
        )
        self.canvas.create_rectangle(
            FIELD_WIDTH - 10, (FIELD_HEIGHT - GOAL_WIDTH) // 2,
            FIELD_WIDTH, (FIELD_HEIGHT + GOAL_WIDTH) // 2,
            fill='white', tags='static'
        )

        # Center circle
        self.canvas.create_oval(
            FIELD_WIDTH // 2 - 50, FIELD_HEIGHT // 2 - 50,
            FIELD_WIDTH // 2 + 50, FIELD_HEIGHT // 2 + 50,
            outline='white', width=3, tags='static'
        )
        self.canvas.create_oval(
            FIELD_WIDTH // 2, FIELD_HEIGHT // 2,
            FIELD_WIDTH // 2, FIELD_HEIGHT // 2,
            outline='white', width=6, tags='static'
        )

    def add_agent(self, agent):
        self.agents.append(agent)

    def add_passive_object(self, obj):
        self.passive_objects.append(obj)

    def assign_closest_percepts(self, team_bots, ball):
        def distance_to_ball(bot):
            return ((bot.x - ball.x) ** 2 + (bot.y - ball.y) ** 2) ** 0.5

        closest_bot = min(team_bots, key=distance_to_ball)

        for bot in team_bots:
            bot.external_percepts = {
                'is_closest': (bot == closest_bot),
                'teammates': [(mate.x, mate.y) for mate in team_bots if mate != bot]
            }

    def update(self):
        self.canvas.delete('dynamic')

        ball = next((o for o in self.passive_objects if hasattr(o, 'is_ball') and o.is_ball), None)

        # --- Assign Closest Percepts ---
        if ball:
            red_team = [bot for bot in self.agents if bot.team == 'Red']
            blue_team = [bot for bot in self.agents if bot.team == 'Blue']

            self.assign_closest_percepts(red_team, ball)
            self.assign_closest_percepts(blue_team, ball)

        for obj in self.passive_objects:
            obj.update(self.canvas)

        for agent in self.agents:
            agent.update(self.canvas, self.agents, self.passive_objects)

        self._check_collisions()
        self._check_goals()

    def _check_collisions(self):
        # Ball-bot collision detection
        ball = next((o for o in self.passive_objects if hasattr(o, 'is_ball') and o.is_ball), None)
        if not ball:
            return

        for bot in self.agents:
            dx = ball.x - bot.x
            dy = ball.y - bot.y
            dist = (dx**2 + dy**2)**0.5
            min_dist = ball.radius + bot.radius

            if dist < min_dist:
                # Normalize direction vector
                if dist == 0:
                    dist = 0.01  # avoid divide-by-zero
                nx, ny = dx / dist, dy / dist

                # Apply bounce effect
                force = 8.0
                ball.dx = nx * force
                ball.dy = ny * force

    def _check_goals(self):
        for obj in self.passive_objects:
            if hasattr(obj, 'is_ball') and obj.is_ball:
                bx, by = obj.x, obj.y

                # Left goal (Blue scores)
                if bx <= 10 and (FIELD_HEIGHT - GOAL_WIDTH) // 2 <= by <= (FIELD_HEIGHT + GOAL_WIDTH) // 2:
                    self.score['Blue'] += 1
                    print("Goal for Blue!", self.score)
                    obj.reset()

                # Right goal (Red scores)
                elif bx >= FIELD_WIDTH - 10 and (FIELD_HEIGHT - GOAL_WIDTH) // 2 <= by <= (FIELD_HEIGHT + GOAL_WIDTH) // 2:
                    self.score['Red'] += 1
                    print("Goal for Red!", self.score)
                    obj.reset()

    def run(self):
        self.update()
        self.root.after(50, self.run)

    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=FIELD_WIDTH, height=FIELD_HEIGHT, bg='green')
        self.canvas.pack()

        self.agents = []
        self.passive_objects = []
        self.score = {'Red': 0, 'Blue': 0}

        self._draw_pitch()