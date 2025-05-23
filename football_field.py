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

        if ball:
            closest_bot = min(self.agents, key=lambda bot: ((bot.x - ball.x) ** 2 + (bot.y - ball.y) ** 2) ** 0.5)
            distance = ((closest_bot.x - ball.x) ** 2 + (closest_bot.y - ball.y) ** 2) ** 0.5

            if closest_bot:
                self.possession_team = closest_bot.team  # "Red" or "Blue"

                if distance <= (closest_bot.radius + ball.radius + 10):  # close enough

                    # --- Store previous touch info ---
                    prev_touch_team = getattr(self, 'last_touch_team', None)
                    prev_touch_bot = getattr(self, 'last_touch_bot_id', None)
                    prev_touch_time = getattr(self, 'last_touch_time', -9999)

                    # --- Pass detection ---
                    if (prev_touch_team == closest_bot.team and
                            prev_touch_bot != closest_bot and
                            self.elapsed_time - prev_touch_time <= self.pass_window):
                        self.stats[closest_bot.team]['passes_completed'] += 1
                        print(f"Pass completed by {closest_bot.team} from bot {prev_touch_bot} to {closest_bot}!")

                    # --- Tackle detection ---
                    if (prev_touch_team is not None and
                            prev_touch_team != closest_bot.team and
                            prev_touch_bot != closest_bot and
                            self.elapsed_time - prev_touch_time <= 20):  # ~1s
                        self.stats[closest_bot.team]['tackles'] += 1
                        print(f"{closest_bot.team} made a TACKLE on {prev_touch_team}!")

                    # --- Update last touch info ---
                    self.last_touch_team = closest_bot.team
                    self.last_touch_bot_id = closest_bot
                    self.last_touch_time = self.elapsed_time

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
        self.check_shot_on_target()
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

                    # Check for saves after ball-bot collision
                    is_goalkeeper_zone = (
                            bot.x <= 50 or bot.x >= FIELD_WIDTH - 50  # near left or right edge
                    )

                    defending_left = bot.team == 'Red' and bot.x < FIELD_WIDTH // 2
                    defending_right = bot.team == 'Blue' and bot.x > FIELD_WIDTH // 2

                    if is_goalkeeper_zone and (defending_left or defending_right):
                        if self.last_shot_team and self.last_shot_team != bot.team:
                            if self.elapsed_time - self.last_shot_time < 30:
                                self.stats[bot.team]['saves'] += 1
                                print(f"{bot.team} keeper made a SAVE!")
                                self.last_shot_team = None  # prevent double-counting

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
                    self.stats['Blue']['goals_scored'] += 1
                    self.stats['Red']['goals_conceded'] += 1
                    self.stats['Blue']['shots_on_target'] += 1
                    print("Goal for Blue!", self.score)
                    obj.reset()
                    self._reset_agents()

                # Right goal (Red scores)
                elif bx >= FIELD_WIDTH - 10 and (FIELD_HEIGHT - GOAL_WIDTH) // 2 <= by <= (FIELD_HEIGHT + GOAL_WIDTH) // 2:
                    self.score['Red'] += 1
                    self.stats['Red']['goals_scored'] += 1
                    self.stats['Blue']['goals_conceded'] += 1
                    self.stats['Red']['shots_on_target'] += 1
                    print("Goal for Red!", self.score)
                    obj.reset()
                    self._reset_agents()

    def check_shot_on_target(self):
        ball = next((o for o in self.passive_objects if hasattr(o, 'is_ball') and o.is_ball), None)
        if not ball or not hasattr(self, 'last_touch_team'):
            return

        goal_top = (FIELD_HEIGHT - GOAL_WIDTH) // 2
        goal_bottom = (FIELD_HEIGHT + GOAL_WIDTH) // 2

        # Ball must be near a goal area vertically
        if not (goal_top <= ball.y <= goal_bottom):
            return  # Ball too high or too low, not near goal

        # --- Blue attacking Red's goal (LEFT) ---
        if self.last_touch_team == 'Blue':
            if ball.dx < 0 and ball.x <= FIELD_WIDTH // 4:
                if self.elapsed_time - self.last_shot_time > self.shot_cooldown:
                    self.last_shot_team = self.last_touch_team
                    self.stats['Blue']['shots_on_target'] += 1
                    self.last_shot_time = self.elapsed_time
                    print("Blue shot on target!")

        # --- Red attacking Blue's goal (RIGHT) ---
        elif self.last_touch_team == 'Red':
            if ball.dx > 0 and ball.x >= 3 * FIELD_WIDTH // 4:
                if self.elapsed_time - self.last_shot_time > self.shot_cooldown:
                    self.last_shot_team = self.last_touch_team
                    self.stats['Red']['shots_on_target'] += 1
                    self.last_shot_time = self.elapsed_time
                    print("Red shot on target!")

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
        self.half_time_window = tk.Toplevel(self.root)
        self.half_time_window.title("Half-Time")
        self.half_time_window.geometry("600x400")
        self.half_time_window.configure(bg='navy')

        # --- Title ---
        title_label = tk.Label(
            self.half_time_window,
            text="HALF TIME",
            font=("Arial", 28, "bold"),
            fg="white",
            bg="navy"
        )
        title_label.pack(pady=10)

        # --- Headers ---
        header_frame = tk.Frame(self.half_time_window, bg='navy')
        header_frame.pack(pady=10)

        tk.Label(header_frame, text="Stats", font=("Arial", 14, "bold"), fg="white", bg="navy", width=20).grid(row=0,
                                                                                                               column=0)
        tk.Label(header_frame, text="Red", font=("Arial", 14, "bold"), fg="red", bg="navy", width=10).grid(row=0,
                                                                                                           column=1)
        tk.Label(header_frame, text="Blue", font=("Arial", 14, "bold"), fg="blue", bg="navy", width=10).grid(row=0,
                                                                                                             column=2)

        # --- Stats List ---
        stats_frame = tk.Frame(self.half_time_window, bg='navy')
        stats_frame.pack()

        # --- Possession percentage calculation ---
        total_possession = self.stats['Red']['possession_time'] + self.stats['Blue']['possession_time']
        if total_possession > 0:
            red_possession_pct = (self.stats['Red']['possession_time'] / total_possession) * 100
            blue_possession_pct = (self.stats['Blue']['possession_time'] / total_possession) * 100
        else:
            red_possession_pct = 50.0
            blue_possession_pct = 50.0

        stat_labels = [
            ("Goals Scored", 'goals_scored'),
            ("Goals Conceded", 'goals_conceded'),
            ("Shots on Target", 'shots_on_target'),
            ("Saves", 'saves'),
            # ("Passes Completed", 'passes_completed'),
            ("Possession (%)", None),
            ("Tackles", 'tackles'),
        ]

        for i, (label_text, stat_key) in enumerate(stat_labels):
            tk.Label(stats_frame, text=label_text, font=("Arial", 12), fg="white", bg="navy", width=20,
                     anchor='w').grid(row=i, column=0, sticky='w')

            if stat_key is not None:
                red_value = self.stats['Red'][stat_key]
                blue_value = self.stats['Blue'][stat_key]
            else:
                red_value = f"{red_possession_pct:.1f}%"
                blue_value = f"{blue_possession_pct:.1f}%"

            tk.Label(stats_frame, text=str(red_value), font=("Arial", 12), fg="red", bg="navy", width=10).grid(row=i,
                                                                                                               column=1)
            tk.Label(stats_frame, text=str(blue_value), font=("Arial", 12), fg="blue", bg="navy", width=10).grid(row=i,
                                                                                                                 column=2)

            # Show live pass count for debugging
            self.canvas.create_text(
                200, 50,
                text=f"Passes: R {self.stats['Red']['passes_completed']} | B {self.stats['Blue']['passes_completed']}",
                fill='white', font=('Arial', 12), tags='scoreboard'
            )

        # --- Resume Button ---
        resume_button = tk.Button(
            self.half_time_window,
            text="Start Second Half",
            font=("Arial", 16, "bold"),
            command=self._start_second_half,
            bg="white",
            fg="black"
        )
        resume_button.pack(pady=20)

    def prompt_show_full_time_stats(self):
        self.full_time_window = tk.Toplevel(self.root)
        self.full_time_window.title("Full Time")
        self.full_time_window.geometry("600x400")
        self.full_time_window.configure(bg='navy')

        # --- Title ---
        title_label = tk.Label(
            self.full_time_window,
            text="FULL TIME",
            font=("Arial", 28, "bold"),
            fg="white",
            bg="navy"
        )
        title_label.pack(pady=10)

        # --- Headers ---
        header_frame = tk.Frame(self.full_time_window, bg='navy')
        header_frame.pack(pady=10)

        tk.Label(header_frame, text="Stats", font=("Arial", 14, "bold"), fg="white", bg="navy", width=20).grid(row=0,
                                                                                                                column=0)
        tk.Label(header_frame, text="Red", font=("Arial", 14, "bold"), fg="red", bg="navy", width=10).grid(row=0,
                                                                                                            column=1)
        tk.Label(header_frame, text="Blue", font=("Arial", 14, "bold"), fg="blue", bg="navy", width=10).grid(row=0,
                                                                                                              column=2)

        # --- Stats ---
        stats_frame = tk.Frame(self.full_time_window, bg='navy')
        stats_frame.pack()

        total_possession = self.stats['Red']['possession_time'] + self.stats['Blue']['possession_time']
        if total_possession > 0:
            red_possession_pct = (self.stats['Red']['possession_time'] / total_possession) * 100
            blue_possession_pct = (self.stats['Blue']['possession_time'] / total_possession) * 100
        else:
            red_possession_pct = blue_possession_pct = 50.0

        stat_labels = [
            ("Goals Scored", 'goals_scored'),
            ("Goals Conceded", 'goals_conceded'),
            ("Shots on Target", 'shots_on_target'),
            ("Saves", 'saves'),
            # ("Passes Completed", 'passes_completed'),
            ("Possession (%)", None),
            ("Tackles", 'tackles'),
        ]

        for i, (label_text, stat_key) in enumerate(stat_labels):
            tk.Label(stats_frame, text=label_text, font=("Arial", 12), fg="white", bg="navy", width=20,
                     anchor='w').grid(row=i, column=0)

            if stat_key is not None:
                red_value = self.stats['Red'][stat_key]
                blue_value = self.stats['Blue'][stat_key]
            else:
                red_value = f"{red_possession_pct:.1f}%"
                blue_value = f"{blue_possession_pct:.1f}%"

            tk.Label(stats_frame, text=str(red_value), font=("Arial", 12), fg="red", bg="navy", width=10).grid(row=i,
                                                                                                                column=1)
            tk.Label(stats_frame, text=str(blue_value), font=("Arial", 12), fg="blue", bg="navy", width=10).grid(row=i,
                                                                                                                  column=2)
        # --- Exit Button ---
        exit_button = tk.Button(
            self.full_time_window,
            text="Exit Game",
            font=("Arial", 14, "bold"),
            bg="white",
            fg="black",
            command=self.root.quit  # Closes the whole app
        )
        exit_button.pack(pady=20)


    def _start_second_half(self):
        self.half_time_window.destroy()  # Close the halftime popup
        self.resume_game()  # Resume the match

    def run(self):
        if self.match_running:
            self.update()
            self.elapsed_time += 1
            if hasattr(self, 'possession_team'):
                self.stats[self.possession_team]['possession_time'] += 1

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
            self.prompt_show_full_time_stats()

        self.root.after(60, self.run) #5 is the fast one

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

        self.last_shot_team = None
        self.last_shot_time = -4  # Some time far in the past
        self.last_pass_bot = None
        self.last_pass_team = None
        self.last_pass_time = -4
        self.pass_window = 1
        self.shot_cooldown = 20  # Frames to wait before counting another shot (~1s if 60fps)

        self.stats = {
            'Red': {
                'goals_scored': 0,
                'goals_conceded': 0,
                'shots_on_target': 0,
                'saves': 0,
                'possession_time': 0,
                'tackles': 0,
                'passes_completed': 0  # <-- ADD THIS
            },
            'Blue': {
                'goals_scored': 0,
                'goals_conceded': 0,
                'shots_on_target': 0,
                'saves': 0,
                'possession_time': 0,
                'tackles': 0,
                'passes_completed': 0  # <-- ADD THIS
            }
        }

        self._draw_pitch()