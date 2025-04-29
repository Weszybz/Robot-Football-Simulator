import tkinter as tk
import time
import random
import tkinter.messagebox

FIELD_WIDTH = 1000
FIELD_HEIGHT = 600
GOAL_WIDTH = 200
FIELD_MARGIN = 20

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

    def draw_scoreboard(self):
        # --- Parameters for compact design ---
        center_x = 100
        top_y = 10
        box_height = 30
        box_width = 50
        score_box_width = 40
        timer_box_width = 50

        # --- Background (optional black bar behind) ---
        self.canvas.create_rectangle(
            center_x - (score_box_width + box_width + timer_box_width) // 2,
            top_y,
            center_x + (score_box_width + box_width + timer_box_width) // 2,
            top_y + box_height,
            fill='black', outline='', tags='scoreboard'
        )

        # --- Left team block (Red) ---
        self.canvas.create_rectangle(
            center_x - (score_box_width // 2 + box_width),
            top_y,
            center_x - (score_box_width // 2),
            top_y + box_height,
            fill='red', outline='', tags='scoreboard'
        )
        self.canvas.create_text(
            center_x - (score_box_width // 2 + box_width // 2),
            top_y + box_height // 2,
            text="RED", font=('Arial', 12, 'bold'),
            fill='white', tags='scoreboard'
        )

        # --- Right team block (Blue) ---
        self.canvas.create_rectangle(
            center_x + (score_box_width // 2),
            top_y,
            center_x + (score_box_width // 2 + box_width),
            top_y + box_height,
            fill='blue', outline='', tags='scoreboard'
        )
        self.canvas.create_text(
            center_x + (score_box_width // 2 + box_width // 2),
            top_y + box_height // 2,
            text="BLUE", font=('Arial', 12, 'bold'),
            fill='white', tags='scoreboard'
        )

        # --- Score text ("0 - 0") ---
        score_text = f"{self.score['Red']} - {self.score['Blue']}"
        self.canvas.create_text(
            center_x,
            top_y + box_height // 2,
            text=score_text, font=('Arial', 14, 'bold'),
            fill='white', tags='scoreboard'
        )
        # --- Timer Box (Black Background) ---
        self.canvas.create_rectangle(
            center_x + (score_box_width // 2 + timer_box_width),
            top_y,
            center_x + (score_box_width // 2 + timer_box_width + timer_box_width),
            top_y + box_height,
            fill='black', outline='', tags='scoreboard'
        )

        # --- Timer text ("45:00") ---
        minutes = self.elapsed_time // 60
        seconds = self.elapsed_time % 60
        time_text = f"{minutes:02}:{seconds:02}"
        self.canvas.create_text(
            center_x + (score_box_width // 2 + box_width + timer_box_width // 2),
            top_y + box_height // 2,
            text=time_text, font=('Arial', 12, 'bold'),
            fill='white', tags='scoreboard'
        )

    def add_agent(self, agent):
        self.agents.append(agent)

    def add_passive_object(self, obj):
        self.passive_objects.append(obj)

    def _reset_agents(self):
        for bot in self.agents:
            bot.reset()

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
        self.canvas.delete('scoreboard')

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
        self.draw_scoreboard()

    def _check_collisions(self):
        # --- Ball-bot collision detection ---
        ball = next((o for o in self.passive_objects if hasattr(o, 'is_ball') and o.is_ball), None)
        if ball:
            for bot in self.agents:
                dx = ball.x - bot.x
                dy = ball.y - bot.y
                dist = (dx ** 2 + dy ** 2) ** 0.5
                min_dist = ball.radius + bot.radius

                if dist < min_dist:
                    # Normalize direction vector
                    if dist == 0:
                        dist = 0.01  # Avoid divide-by-zero
                    nx, ny = dx / dist, dy / dist

                    # Apply bounce effect
                    force = 8.0
                    ball.dx = nx * force
                    ball.dy = ny * force

        # --- Bot-bot collision detection ---
        num_bots = len(self.agents)
        extra_gap = 100.0
        for i in range(num_bots):
            for j in range(i + 1, num_bots):
                bot1 = self.agents[i]
                bot2 = self.agents[j]
                dx = bot2.x - bot1.x
                dy = bot2.y - bot1.y
                dist = (dx ** 2 + dy ** 2) ** 0.5
                min_dist = bot1.radius + bot2.radius + extra_gap

                if dist < min_dist and dist > 0:
                    # Normalize direction vector
                    nx, ny = dx / dist, dy / dist

                    # Push bots apart
                    overlap = min_dist - dist
                    bot1.x -= nx * overlap / 4
                    bot1.y -= ny * overlap / 2
                    bot2.x += nx * overlap / 4
                    bot2.y += ny * overlap / 2

    def _check_goals(self):
        for obj in self.passive_objects:
            if hasattr(obj, 'is_ball') and obj.is_ball:
                bx, by = obj.x, obj.y

                # Left goal (Blue scores)
                if bx <= 10 and (FIELD_HEIGHT - GOAL_WIDTH) // 2 <= by <= (FIELD_HEIGHT + GOAL_WIDTH) // 2:
                    self.score['Blue'] += 1
                    print("Goal for Blue!", self.score)
                    obj.reset()
                    self._reset_agents()

                # Right goal (Red scores)
                elif bx >= FIELD_WIDTH - 10 and (FIELD_HEIGHT - GOAL_WIDTH) // 2 <= by <= (FIELD_HEIGHT + GOAL_WIDTH) // 2:
                    self.score['Red'] += 1
                    print("Goal for Red!", self.score)
                    obj.reset()
                    self._reset_agents()

    def resume_game(self):
        self.match_running = True

    def pause_game(self):
        self.match_running = False
        # Optionally reset ball, freeze bots
        print("Paused for half-time. Press a key to continue...")

    def end_game(self):
        self.match_running = False
        print(f"Match ended! Final Score - Red: {self.score['Red']}, Blue: {self.score['Blue']}")
        # Optionally show a "Full Time" banner

    def prompt_resume_second_half(self):
        response = tkinter.messagebox.askokcancel(
            "Half Time",
            "Half-Time!\nClick OK to start the second half."
        )

        if response:
            self.resume_game()

    def run(self):
        if self.match_running:
            self.update()

        if not self.match_running:
            return  # Stop ticking after match ends

        self.elapsed_time += 1

        # --- Half-time ---
        if self.elapsed_time == 2701 and not self.half_time_reached:  # 45 * 60 = 2700 seconds
            print("Half Time!")
            self.half_time_reached = True
            self.match_running = False
            self.pause_game()
            self.prompt_resume_second_half()

        # --- Full-time ---
        if self.elapsed_time == 5401 and not self.full_time_reached:  # 90 * 60 = 5400 seconds
            print("Full Time!")
            self.full_time_reached = True
            self.match_running = False
            self.end_game()

        self.root.after(50, self.run)

    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=FIELD_WIDTH, height=FIELD_HEIGHT, bg='green')
        self.canvas.pack()

        self.agents = []
        self.passive_objects = []
        self.score = {'Red': 0, 'Blue': 0}
        self.elapsed_time = 0

        self.half_time_reached = False
        self.full_time_reached = False
        self.match_running = True

        self._draw_pitch()