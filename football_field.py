import tkinter as tk
import time
import random
import tkinter.messagebox
import math
from constants import FIELD_WIDTH, FIELD_HEIGHT, FIELD_MARGIN, GOAL_WIDTH
from bot_base import DefenderBrain

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
                'teammates': [(mate.x, mate.y) for mate in team_bots if mate != bot],
                'elapsed_time': self.elapsed_time  # Add elapsed time to percepts
            }

    def update(self):
        self.canvas.delete('dynamic')
        self.canvas.delete('scoreboard')

        # Store original positions for all agents if not already stored
        if not hasattr(self, 'original_positions'):
            self.original_positions = {agent: (agent.x, agent.y) for agent in self.agents}

        ball = next((o for o in self.passive_objects if hasattr(o, 'is_ball') and o.is_ball), None)

        # Check if keeper has the ball
        keeper_has_ball = False
        keeper = None
        if self.ball_possessing_bot and hasattr(self.ball_possessing_bot, 'position_brain') and self.ball_possessing_bot.position_brain.__class__.__name__ == 'GoalkeeperBrain':
            keeper_has_ball = True
            keeper = self.ball_possessing_bot
            if not hasattr(self, 'keeper_hold_start_time') or self.keeper_hold_start_time < 0:
                self.keeper_hold_start_time = self.elapsed_time
            # Set keeper's rotation duration to 1 second (60 frames)
            self.possession_duration = 60
        else:
            self.keeper_hold_start_time = -1
            # Reset to default for other players (quicker rotation)
            self.possession_duration = 18

        # If keeper has ball, move all other players to original positions
        all_back = True
        if keeper_has_ball:
            for agent in self.agents:
                if agent is keeper:
                    continue
                orig_x, orig_y = self.original_positions[agent]
                dx = orig_x - agent.x
                dy = orig_y - agent.y
                dist = math.hypot(dx, dy)
                if dist > 2.0:
                    agent.x += dx * 0.03
                    agent.y += dy * 0.03
                    all_back = False
            # Keeper holds the ball until all players are back or 1 second (60 frames)
            if not all_back and self.elapsed_time - self.keeper_hold_start_time < 60:
                # Prevent keeper from releasing the ball
                self.possession_start_time = self.elapsed_time
                self.stored_ball_speed = (0, 0)
                if ball:
                    ball.dx = 0
                    ball.dy = 0
                # Freeze keeper's position (keeper stays wherever they are)
            else:
                # After 1 second, force the keeper to rotate and make a pass from their current position
                if self.ball_possessing_bot == keeper:
                    teammate_options = self.find_nearest_teammate(keeper)
                    if teammate_options:
                        self.target_teammate, target_angle = teammate_options[0]
                        self.second_target = teammate_options[1] if len(teammate_options) > 1 else None
                        self.target_release_angle, self.rotate_clockwise = self.get_shortest_rotation(
                            self.initial_contact_angle, target_angle
                        )
                    else:
                        default_angle = math.pi if keeper.team == 'Red' else 0
                        self.target_release_angle, self.rotate_clockwise = self.get_shortest_rotation(
                            self.initial_contact_angle, default_angle
                        )
                        self.target_teammate = None
                        self.second_target = None
                    # Use the keeper's current position for the pass (do not move keeper back)
                    self.ball_distance = abs(ball.x - keeper.x) + abs(ball.y - keeper.y)
                    self.stored_ball_speed = (0, 0)
                    # Let the normal rotation/release logic handle the pass
                    self.possession_start_time = self.elapsed_time - self.possession_duration
                self.keeper_hold_start_time = -1

        if ball:
            closest_bot = min(self.agents, key=lambda bot: ((bot.x - ball.x) ** 2 + (bot.y - ball.y) ** 2) ** 0.5)
            distance = ((closest_bot.x - ball.x) ** 2 + (closest_bot.y - ball.y) ** 2) ** 0.5

            if closest_bot:
                self.possession_team = closest_bot.team

                # Draw any shooting lines from percepts
                if hasattr(closest_bot, 'external_percepts'):
                    shooting_lines = closest_bot.external_percepts.get('shooting_lines', [])
                    for line in shooting_lines:
                        start_x, start_y = line['start']
                        end_x, end_y = line['end']
                        # Only strikers get purple lines, others get yellow
                        if hasattr(closest_bot, 'position_brain') and closest_bot.position_brain.__class__.__name__ == 'StrikerBrain':
                            color = 'purple'
                        else:
                            color = 'yellow'
                        self.canvas.create_line(
                            start_x, start_y,
                            end_x, end_y,
                            fill=color,
                            width=2,
                            dash=(4, 4),
                            tags='dynamic'
                        )

                if distance <= (closest_bot.radius + ball.radius + 10):  # close enough
                    # Store previous touch info
                    prev_touch_team = self.last_touch_team
                    prev_touch_bot = self.last_touch_bot_id
                    prev_touch_time = self.last_touch_time
                    prev_touch_pos = self.last_touch_pos

                    # Pass detection logic
                    if prev_touch_team == closest_bot.team and prev_touch_bot != closest_bot:
                        time_since_last_touch = self.elapsed_time - prev_touch_time
                        
                        if time_since_last_touch <= self.pass_window:
                            # Calculate pass distance
                            if prev_touch_pos:
                                pass_distance = ((closest_bot.x - prev_touch_pos[0]) ** 2 + 
                                               (closest_bot.y - prev_touch_pos[1]) ** 2) ** 0.5
                                
                                # Check if it's a valid pass
                                if pass_distance >= self.min_pass_distance:
                                    self.stats[closest_bot.team]['passes_completed'] += 1
                                    print(f"Pass completed by {closest_bot.team} from bot {prev_touch_bot} to {closest_bot}!")

                                    # Visual feedback for completed pass
                                    if not (hasattr(closest_bot, 'position_brain') and closest_bot.position_brain.__class__.__name__ == 'StrikerBrain'):
                                        self.canvas.create_line(
                                            prev_touch_pos[0], prev_touch_pos[1],
                                            closest_bot.x, closest_bot.y,
                                            fill='yellow', width=2, dash=(4, 4),
                                            tags='dynamic'
                                        )

                    # Update last touch info
                    self.last_touch_team = closest_bot.team
                    self.last_touch_bot_id = closest_bot
                    self.last_touch_time = self.elapsed_time
                    self.last_touch_pos = (closest_bot.x, closest_bot.y)

                    # If this is a new touch by a different bot, count as pass attempt
                    if prev_touch_bot != closest_bot and prev_touch_team == closest_bot.team:
                        self.stats[closest_bot.team]['passes_attempted'] += 1

                    # If ball is not possessed, start possession
                    if self.ball_possessing_bot is None or self.ball_possessing_bot != closest_bot:
                        self.ball_possessing_bot = closest_bot
                        self.possession_start_time = self.elapsed_time
                        
                        # Calculate initial contact angle from ball's direction of travel
                        if ball.dx != 0 or ball.dy != 0:
                            self.initial_contact_angle = math.atan2(-ball.dy, -ball.dx)
                        else:
                            self.initial_contact_angle = math.atan2(closest_bot.y - ball.y, closest_bot.x - ball.x)
                        
                        # --- SHOOTING OR PASSING MECHANIC FOR ALL PLAYERS ---
                        in_opponent_half = (closest_bot.team == 'Red' and closest_bot.x > FIELD_WIDTH // 2) or (closest_bot.team == 'Blue' and closest_bot.x < FIELD_WIDTH // 2)
                        # New: also shoot if inside opponent's 18-yard box
                        in_opponent_box = (
                            (closest_bot.team == 'Red' and closest_bot.x > FIELD_WIDTH * 0.75) or
                            (closest_bot.team == 'Blue' and closest_bot.x < FIELD_WIDTH * 0.25)
                        )
                        if in_opponent_half or in_opponent_box:
                            # Always reset and attempt shooting rotation
                            is_left_team = closest_bot.team == 'Red'
                            goal_x = FIELD_WIDTH if is_left_team else 0
                            goal_y = FIELD_HEIGHT // 2
                            target_angle = math.atan2(goal_y - closest_bot.y, goal_x - closest_bot.x)
                            self.target_release_angle, self.rotate_clockwise = self.get_shortest_rotation(
                                self.initial_contact_angle, target_angle
                            )
                            self.target_teammate = None
                            self.second_target = None
                            self.ball_distance = distance
                            self.stored_ball_speed = (ball.dx, ball.dy)
                            ball.dx = 0
                            ball.dy = 0
                            closest_bot._striker_action = 'shoot'
                        else:
                            # Use passing mechanic
                            teammate_options = self.find_nearest_teammate(closest_bot)
                            perception_type = getattr(closest_bot, 'perception_type', None)
                            chosen_option = None
                            if len(teammate_options) > 1:
                                if perception_type == 'aggressive':
                                    # Aggressive: usually pick progressive, but sometimes pick safe
                                    if random.random() < 0.8:
                                        chosen_option = teammate_options[1]
                                    else:
                                        chosen_option = teammate_options[0]
                                elif perception_type == 'safe':
                                    # Safe: usually pick safe, but sometimes pick progressive
                                    if random.random() < 0.8:
                                        chosen_option = teammate_options[0]
                                    else:
                                        chosen_option = teammate_options[1]
                                else:
                                    # Default: randomize between the two
                                    chosen_option = random.choice(teammate_options)
                            else:
                                chosen_option = teammate_options[0]
                            self.target_teammate, target_angle = chosen_option
                            self.second_target = teammate_options[1] if len(teammate_options) > 1 else None
                            self.target_release_angle, self.rotate_clockwise = self.get_shortest_rotation(
                                self.initial_contact_angle, target_angle
                            )
                        self.ball_distance = distance
                        self.stored_ball_speed = (ball.dx, ball.dy)
                        ball.dx = 0
                        ball.dy = 0
                        closest_bot._striker_action = None
                        
                        # Check for saves after ball-bot collision
                        is_goalkeeper_zone = (
                            closest_bot.x <= 50 or closest_bot.x >= FIELD_WIDTH - 50  # near left or right edge
                        )

                        defending_left = closest_bot.team == 'Red' and closest_bot.x < FIELD_WIDTH // 2
                        defending_right = closest_bot.team == 'Blue' and closest_bot.x > FIELD_WIDTH // 2

                        if is_goalkeeper_zone and (defending_left or defending_right):
                            if self.last_shot_team and self.last_shot_team != closest_bot.team:
                                if self.elapsed_time - self.last_shot_time < 30:
                                    self.stats[closest_bot.team]['saves'] += 1
                                    print(f"{closest_bot.team} keeper made a SAVE!")
                                    self.last_shot_team = None  # prevent double-counting

                    # If this bot has possession, update ball position with smooth rotation
                    if self.ball_possessing_bot == closest_bot:
                        possession_time = self.elapsed_time - self.possession_start_time
                        # --- PANIC SHOT LOGIC ---
                        in_opponent_half = (closest_bot.team == 'Red' and closest_bot.x > FIELD_WIDTH // 2) or (closest_bot.team == 'Blue' and closest_bot.x < FIELD_WIDTH // 2)
                        is_striker = hasattr(closest_bot, 'position_brain') and closest_bot.position_brain.__class__.__name__ == 'StrikerBrain'
                        panic_shot = False
                        panic_pass = False
                        if is_striker and getattr(closest_bot, '_striker_action', None) == 'shoot':
                            # Always move striker toward goal while rotating
                            goal_x = FIELD_WIDTH if closest_bot.team == 'Red' else 0
                            goal_y = FIELD_HEIGHT // 2
                            move_dx = (goal_x - closest_bot.x) * 0.15
                            move_dy = (goal_y - closest_bot.y) * 0.15
                            speed = math.hypot(move_dx, move_dy)
                            if speed > 4.0:
                                move_dx = (move_dx / speed) * 4.0
                                move_dy = (move_dy / speed) * 4.0
                            closest_bot.x += move_dx
                            closest_bot.y += move_dy
                            # Panic shot if pushed back to own half, rotation takes too long, or close to goal
                            distance_to_goal = abs(goal_x - closest_bot.x)
                            if not in_opponent_half or possession_time > self.possession_duration * 1.5 or distance_to_goal < FIELD_WIDTH / 4:
                                panic_shot = True
                        elif getattr(closest_bot, '_striker_action', None) != 'shoot':
                            # For all other passing (not shooting): forced pass if rotation takes too long
                            if possession_time > self.possession_duration * 1.5:
                                panic_pass = True
                        if (possession_time < self.possession_duration and not panic_shot and not panic_pass):
                            t = possession_time / self.possession_duration
                            t = self._smooth_step(t)
                            # Use robust angle interpolation
                            current_angle = self.interpolate_angle(
                                self.initial_contact_angle, self.target_release_angle, t, self.rotate_clockwise
                            )
                            # Always update ball position using rotation
                            rotated_x = closest_bot.x + math.cos(current_angle) * self.ball_distance
                            rotated_y = closest_bot.y + math.sin(current_angle) * self.ball_distance
                            ball.x = rotated_x
                            ball.y = rotated_y
                            # Draw lines as before
                            if hasattr(closest_bot, 'position_brain') and closest_bot.position_brain.__class__.__name__ == 'StrikerBrain':
                                if getattr(closest_bot, '_striker_action', None) == 'shoot':
                                    is_left_team = closest_bot.team == 'Red'
                                    goal_x = FIELD_WIDTH if is_left_team else 0
                                    goal_y = FIELD_HEIGHT // 2
                                    # Find the opponent keeper
                                    keeper = None
                                    for agent in self.agents:
                                        if agent.team != closest_bot.team and hasattr(agent, 'position_brain') and agent.position_brain.__class__.__name__ == 'GoalkeeperBrain':
                                            keeper = agent
                                            break
                                    # Default target is center of goal
                                    shot_target_y = goal_y
                                    # If keeper found, aim away from them
                                    if keeper:
                                        goal_top = (FIELD_HEIGHT - GOAL_WIDTH) // 2
                                        goal_bottom = (FIELD_HEIGHT + GOAL_WIDTH) // 2
                                        # If keeper is left of center, shoot right; if right, shoot left; if center, randomize
                                        if keeper.y < goal_y - 10:
                                            shot_target_y = goal_y + GOAL_WIDTH // 4  # shoot right
                                        elif keeper.y > goal_y + 10:
                                            shot_target_y = goal_y - GOAL_WIDTH // 4  # shoot left
                                        else:
                                            # Keeper is centered, randomize left/right
                                            if random.random() < 0.5:
                                                shot_target_y = goal_y + GOAL_WIDTH // 4
                                            else:
                                                shot_target_y = goal_y - GOAL_WIDTH // 4
                                    dx_to_goal = goal_x - rotated_x
                                    dy_to_goal = shot_target_y - rotated_y
                                    shot_distance = math.hypot(dx_to_goal, dy_to_goal)
                                    MIN_POWER = 28.0
                                    MAX_POWER = 48.0
                                    power_factor = shot_distance / (FIELD_WIDTH // 2)
                                    shot_power = MIN_POWER + (MAX_POWER - MIN_POWER) * power_factor
                                    ball.dx = (dx_to_goal / shot_distance) * shot_power
                                    ball.dy = (dy_to_goal / shot_distance) * shot_power
                                else:
                                    if self.target_teammate:
                                        self.canvas.create_line(
                                            closest_bot.x, closest_bot.y,
                                            self.target_teammate.x, self.target_teammate.y,
                                            fill='yellow', width=1, dash=(4, 4), tags='dynamic'
                                        )
                                    if self.second_target:
                                        self.canvas.create_line(
                                            closest_bot.x, closest_bot.y,
                                            self.second_target[0].x, self.second_target[0].y,
                                            fill='yellow', width=1, dash=(4, 4), tags='dynamic'
                                        )
                            else:
                                if self.target_teammate:
                                    self.canvas.create_line(
                                        closest_bot.x, closest_bot.y,
                                        self.target_teammate.x, self.target_teammate.y,
                                        fill='yellow', width=1, dash=(4, 4), tags='dynamic'
                                    )
                                if self.second_target:
                                    self.canvas.create_line(
                                        closest_bot.x, closest_bot.y,
                                        self.second_target[0].x, self.second_target[0].y,
                                        fill='yellow', width=1, dash=(4, 4), tags='dynamic'
                                    )
                        else:
                            if panic_pass:
                                print(f"Panic pass triggered for {closest_bot} at time {self.elapsed_time}")
                            # --- RELEASE BALL ---
                            # Use the last rotated position as the starting point
                            t = 1.0
                            current_angle = self.interpolate_angle(
                                self.initial_contact_angle, self.target_release_angle, t, self.rotate_clockwise
                            )
                            rotated_x = closest_bot.x + math.cos(current_angle) * self.ball_distance
                            rotated_y = closest_bot.y + math.sin(current_angle) * self.ball_distance
                            ball.x = rotated_x
                            ball.y = rotated_y
                            if hasattr(closest_bot, 'position_brain') and closest_bot.position_brain.__class__.__name__ == 'StrikerBrain':
                                if getattr(closest_bot, '_striker_action', None) == 'shoot':
                                    is_left_team = closest_bot.team == 'Red'
                                    goal_x = FIELD_WIDTH if is_left_team else 0
                                    goal_y = FIELD_HEIGHT // 2
                                    # Find the opponent keeper
                                    keeper = None
                                    for agent in self.agents:
                                        if agent.team != closest_bot.team and hasattr(agent, 'position_brain') and agent.position_brain.__class__.__name__ == 'GoalkeeperBrain':
                                            keeper = agent
                                            break
                                    # Default target is center of goal
                                    shot_target_y = goal_y
                                    # If keeper found, aim away from them
                                    if keeper:
                                        goal_top = (FIELD_HEIGHT - GOAL_WIDTH) // 2
                                        goal_bottom = (FIELD_HEIGHT + GOAL_WIDTH) // 2
                                        # If keeper is left of center, shoot right; if right, shoot left; if center, randomize
                                        if keeper.y < goal_y - 10:
                                            shot_target_y = goal_y + GOAL_WIDTH // 4  # shoot right
                                        elif keeper.y > goal_y + 10:
                                            shot_target_y = goal_y - GOAL_WIDTH // 4  # shoot left
                                        else:
                                            # Keeper is centered, randomize left/right
                                            if random.random() < 0.5:
                                                shot_target_y = goal_y + GOAL_WIDTH // 4
                                            else:
                                                shot_target_y = goal_y - GOAL_WIDTH // 4
                                    dx_to_goal = goal_x - rotated_x
                                    dy_to_goal = shot_target_y - rotated_y
                                    shot_distance = math.hypot(dx_to_goal, dy_to_goal)
                                    MIN_POWER = 28.0
                                    MAX_POWER = 48.0
                                    power_factor = shot_distance / (FIELD_WIDTH // 2)
                                    shot_power = MIN_POWER + (MAX_POWER - MIN_POWER) * power_factor
                                    ball.dx = (dx_to_goal / shot_distance) * shot_power
                                    ball.dy = (dy_to_goal / shot_distance) * shot_power
                                else:
                                    if self.target_teammate:
                                        dx = self.target_teammate.x - rotated_x
                                        dy = self.target_teammate.y - rotated_y
                                        dist = math.hypot(dx, dy)
                                        BASE_PASS_SPEED = 12.0  # or whatever feels right
                                        pass_speed = self.calculate_pass_speed(dist, BASE_PASS_SPEED)
                                        ball.dx = (dx / dist) * pass_speed
                                        ball.dy = (dy / dist) * pass_speed
                                    else:
                                        # No teammate: release ball forward
                                        direction = 1 if closest_bot.team == 'Red' else -1
                                        ball.dx = direction * 15.0
                                        ball.dy = 0.0
                            else:
                                # Always release the pass after rotation for non-strikers
                                if self.target_teammate:
                                    dx = self.target_teammate.x - rotated_x
                                    dy = self.target_teammate.y - rotated_y
                                    dist = math.hypot(dx, dy)
                                    BASE_PASS_SPEED = 12.0  # or whatever feels right
                                    pass_speed = self.calculate_pass_speed(dist, BASE_PASS_SPEED)
                                    ball.dx = (dx / dist) * pass_speed
                                    ball.dy = (dy / dist) * pass_speed
                                else:
                                    # No teammate: release ball forward
                                    direction = 1 if closest_bot.team == 'Red' else -1
                                    ball.dx = direction * 15.0
                                    ball.dy = 0.0
                            self.ball_possessing_bot = None
                            self.possession_start_time = -1
                            self.target_teammate = None
                            self.second_target = None
                    
                    # If different bot touches the ball, transfer possession
                    elif self.ball_possessing_bot != closest_bot:
                        self.ball_possessing_bot = closest_bot
                        self.possession_start_time = self.elapsed_time
                        
                        # Calculate initial contact angle from ball's direction of travel
                        if ball.dx != 0 or ball.dy != 0:
                            self.initial_contact_angle = math.atan2(-ball.dy, -ball.dx)
                        else:
                            self.initial_contact_angle = math.atan2(closest_bot.y - ball.y, closest_bot.x - ball.x)
                        
                        # Find nearest teammates and their angles
                        teammate_options = self.find_nearest_teammate(closest_bot)
                        if teammate_options:
                            # Use the first option as primary target
                            self.target_teammate, target_angle = teammate_options[0]
                            # Store second option if available
                            self.second_target = teammate_options[1] if len(teammate_options) > 1 else None
                            
                            # Determine optimal rotation direction for primary target
                            self.target_release_angle, self.rotate_clockwise = self.get_shortest_rotation(
                                self.initial_contact_angle, target_angle
                            )
                        else:
                            # If no teammates, use default forward direction
                            default_angle = math.pi if closest_bot.team == 'Red' else 0
                            self.target_release_angle, self.rotate_clockwise = self.get_shortest_rotation(
                                self.initial_contact_angle, default_angle
                            )
                            self.target_teammate = None
                            self.second_target = None
                        
                        self.ball_distance = distance
                        self.stored_ball_speed = (ball.dx, ball.dy)
                        ball.dx = 0
                        ball.dy = 0

            red_team = [bot for bot in self.agents if bot.team == 'Red']
            blue_team = [bot for bot in self.agents if bot.team == 'Blue']

            self.assign_closest_percepts(red_team, ball)
            self.assign_closest_percepts(blue_team, ball)

        for obj in self.passive_objects:
            obj.update(self.canvas)

        for agent in self.agents:
            # Restrict non-keeper players from entering within 1/8 field width from the goal inside the 18-yard box
            is_keeper = hasattr(agent, 'position_brain') and agent.position_brain.__class__.__name__ == 'GoalkeeperBrain'
            x_min = 0
            x_max = FIELD_WIDTH
            y_min_box = FIELD_HEIGHT // 6
            y_max_box = 5 * (FIELD_HEIGHT // 6)
            box_limit = FIELD_WIDTH // 8
            # Left side restriction
            if not is_keeper and agent.x < box_limit and y_min_box <= agent.y <= y_max_box:
                agent.x = box_limit
            # Right side restriction
            if not is_keeper and agent.x > FIELD_WIDTH - box_limit and y_min_box <= agent.y <= y_max_box:
                agent.x = FIELD_WIDTH - box_limit
            agent.update(self.canvas, self.agents, self.passive_objects)

        self._check_collisions()
        self._check_goals()
        self.check_shot_on_target()
        self.draw_scoreboard()

        # Update scoreboard with pass completion stats
        self.canvas.create_text(
            200, 30,
            text=f"Passes (Completed/Attempted): Red {self.stats['Red']['passes_completed']}/{self.stats['Red']['passes_attempted']} | Blue {self.stats['Blue']['passes_completed']}/{self.stats['Blue']['passes_attempted']}",
            fill='white', font=('Arial', 12), tags='scoreboard'
        )

    def calculate_progress_score(self, passer, receiver):
        """Calculate how progressive the pass is towards the goal."""
        # Determine which x-coordinate represents progress (depends on team)
        target_x = FIELD_WIDTH if passer.team == 'Red' else 0
        
        # Calculate how much closer to the target the receiver is compared to passer
        passer_distance = abs(passer.x - target_x)
        receiver_distance = abs(receiver.x - target_x)
        
        # Check if receiver is in goalkeeper area
        GOALKEEPER_AREA_WIDTH = 100  # Width of the goalkeeper area from goal
        is_goalkeeper_area = False
        
        if passer.team == 'Red':
            # For Red team (attacking right), check if receiver is in left goalkeeper area
            if receiver.x <= GOALKEEPER_AREA_WIDTH:
                is_goalkeeper_area = True
        else:
            # For Blue team (attacking left), check if receiver is in right goalkeeper area
            if receiver.x >= FIELD_WIDTH - GOALKEEPER_AREA_WIDTH:
                is_goalkeeper_area = True
        
        # Heavily penalize backwards passes to goalkeeper area
        if is_goalkeeper_area and receiver_distance > passer_distance:
            return 0.0  # Strongly discourage passing back to goalkeeper
        
        # Convert to a score between 0.0 and 1.0
        # 1.0 means receiver is significantly closer to goal
        # 0.0 means receiver is further from goal
        progress = (passer_distance - receiver_distance) / FIELD_WIDTH
        
        # Additional penalty for any backward pass
        if progress < 0:
            progress *= 2  # Double the negative effect of backward passes
        
        return max(0.0, min(1.0, progress + 0.5))  # Normalize to 0-1 range

    def find_nearest_teammate(self, bot):
        """Find the best teammates to pass to based on multiple factors. Striker is preferred for midfielders and defenders, but not forced."""
        teammates = [agent for agent in self.agents if agent.team == bot.team and agent != bot]
        if not teammates:
            return None
        # Identify the striker on the team
        striker = None
        for agent in teammates:
            if hasattr(agent, 'position_brain') and agent.position_brain.__class__.__name__ == 'StrikerBrain':
                striker = agent
                break
        # Calculate scores for all teammates in range
        teammate_scores = []
        MAX_PASS_DISTANCE = 600  # Maximum distance for a valid pass
        MIN_PASS_DISTANCE = 50   # Minimum distance to consider (avoid too short passes)
        # Get ball's current direction if moving
        ball = next((o for o in self.passive_objects if hasattr(o, 'is_ball') and o.is_ball), None)
        if ball and (ball.dx != 0 or ball.dy != 0):
            ball_direction = math.atan2(ball.dy, ball.dx)
        else:
            ball_direction = None
        # Check if the passing bot is a midfielder or defender
        is_midfielder = hasattr(bot, 'position_brain') and bot.position_brain.__class__.__name__ == 'MidfielderBrain'
        is_defender = hasattr(bot, 'position_brain') and bot.position_brain.__class__.__name__ == 'DefenderBrain'
        for teammate in teammates:
            dx = teammate.x - bot.x
            dy = teammate.y - bot.y
            dist = math.hypot(dx, dy)
            if dist > MAX_PASS_DISTANCE or dist < MIN_PASS_DISTANCE:
                continue
            position_score = 1.0 - ((dist - MIN_PASS_DISTANCE) / (MAX_PASS_DISTANCE - MIN_PASS_DISTANCE))
            angle_to_teammate = math.atan2(dy, dx)
            if ball_direction is not None:
                angle_diff = abs(self.normalize_angle(angle_to_teammate - ball_direction))
                angle_score = 1.0 - (angle_diff / math.pi)
            else:
                forward_angle = math.pi if bot.team == 'Red' else 0
                angle_diff = abs(self.normalize_angle(angle_to_teammate - forward_angle))
                angle_score = 1.0 - (angle_diff / math.pi)
            space_score = self.calculate_space_score(teammate)
            progress_score = self.calculate_progress_score(bot, teammate)
            # Prefer striker for midfielders and defenders
            role_bonus = 1.0
            if (is_midfielder or is_defender) and striker and teammate is striker:
                role_bonus = 2.0  # Big bonus for passing to striker
            final_score = role_bonus * (
                0.25 * position_score +
                0.2 * angle_score +
                0.2 * space_score +
                0.35 * progress_score
            )
            teammate_scores.append((final_score, teammate, angle_to_teammate))
        if not teammate_scores:
            return None
        teammate_scores.sort(reverse=True, key=lambda x: x[0])
        best_options = []
        if teammate_scores:
            best_options.append((teammate_scores[0][1], teammate_scores[0][2]))
            for score, teammate, angle in teammate_scores[1:]:
                first_teammate = best_options[0][0]
                dx = teammate.x - first_teammate.x
                dy = teammate.y - first_teammate.y
                dist_between = math.hypot(dx, dy)
                if dist_between > 100:
                    best_options.append((teammate, angle))
                    break
        return best_options if best_options else None

    def calculate_space_score(self, teammate):
        """Calculate how much space a teammate has (not marked by opponents)."""
        MARKING_DISTANCE = 100  # Distance at which an opponent is considered marking
        
        # Find all opponents
        opponents = [agent for agent in self.agents if agent.team != teammate.team]
        
        # Find closest opponent
        min_distance = float('inf')
        for opponent in opponents:
            dist = math.hypot(opponent.x - teammate.x, opponent.y - teammate.y)
            min_distance = min(min_distance, dist)
        
        # Score from 0.0 (opponent very close) to 1.0 (no opponents within MARKING_DISTANCE)
        if min_distance <= MARKING_DISTANCE:
            return 1.0 - (min_distance / MARKING_DISTANCE)
        return 1.0

    def calculate_pass_speed(self, distance, base_speed):
        """Calculate pass speed based on distance to teammate."""
        # Minimum and maximum speed multipliers
        MIN_SPEED_MULT = 0.8  # For very close passes
        MAX_SPEED_MULT = 2.0  # For long-range passes
        
        # Distance thresholds (in pixels)
        SHORT_PASS = 100   # Passes under this distance use MIN_SPEED
        LONG_PASS = 400    # Passes over this distance use MAX_SPEED
        
        # Ensure minimum speed (prevent dead balls)
        MIN_SPEED = 9.0
        
        if distance <= SHORT_PASS:
            speed = base_speed * MIN_SPEED_MULT
        elif distance >= LONG_PASS:
            speed = base_speed * MAX_SPEED_MULT
        else:
            # Linear interpolation between min and max multipliers
            t = (distance - SHORT_PASS) / (LONG_PASS - SHORT_PASS)
            speed_mult = MIN_SPEED_MULT + (MAX_SPEED_MULT - MIN_SPEED_MULT) * t
            speed = base_speed * speed_mult
        
        # Ensure speed never falls below minimum
        return max(speed, MIN_SPEED)

    def normalize_angle(self, angle):
        """Normalize angle to be between 0 and 2π"""
        return angle % (2 * math.pi)

    def get_shortest_rotation(self, current_angle, target_angle):
        """
        Calculate the shortest rotation direction and final target angle.
        Returns: (target_angle, is_clockwise)
        """
        # Normalize angles to 0-2π range
        current_angle = self.normalize_angle(current_angle)
        target_angle = self.normalize_angle(target_angle)
        
        # Calculate both possible rotation amounts
        clockwise_dist = current_angle - target_angle if current_angle > target_angle else current_angle + (2 * math.pi - target_angle)
        counterclockwise_dist = target_angle - current_angle if target_angle > current_angle else (2 * math.pi - current_angle) + target_angle
        
        # Choose shortest rotation
        if clockwise_dist < counterclockwise_dist:
            return target_angle, True
        else:
            return target_angle, False

    def _check_collisions(self):
        # --- Ball-bot collision detection ---
        ball = next((o for o in self.passive_objects if hasattr(o, 'is_ball') and o.is_ball), None)
        if ball:
            # Find the closest bot to the ball
            closest_bot = min(self.agents, key=lambda bot: ((bot.x - ball.x) ** 2 + (bot.y - ball.y) ** 2) ** 0.5)
            for bot in self.agents:
                dx = ball.x - bot.x
                dy = ball.y - bot.y
                dist = (dx ** 2 + dy ** 2) ** 0.5
                min_dist = ball.radius + bot.radius + (self.possession_buffer if self.ball_possessing_bot == bot else 0)

                if dist < min_dist:
                    # Only the closest bot can take possession
                    if bot == closest_bot:
                        if self.ball_possessing_bot is None or self.ball_possessing_bot != bot:
                            self.ball_possessing_bot = bot
                            self.possession_start_time = self.elapsed_time
                            # Calculate initial contact angle from ball's direction of travel
                            if ball.dx != 0 or ball.dy != 0:
                                self.initial_contact_angle = math.atan2(-ball.dy, -ball.dx)
                            else:
                                self.initial_contact_angle = math.atan2(dy, dx)
                            # Find nearest teammates and their angles
                            teammate_options = self.find_nearest_teammate(bot)
                            if teammate_options:
                                self.target_teammate, target_angle = teammate_options[0]
                                self.second_target = teammate_options[1] if len(teammate_options) > 1 else None
                                self.target_release_angle, self.rotate_clockwise = self.get_shortest_rotation(
                                    self.initial_contact_angle, target_angle
                                )
                            else:
                                default_angle = math.pi if bot.team == 'Red' else 0
                                self.target_release_angle, self.rotate_clockwise = self.get_shortest_rotation(
                                    self.initial_contact_angle, default_angle
                                )
                                self.target_teammate = None
                                self.second_target = None
                            self.ball_distance = min_dist
                            self.stored_ball_speed = (ball.dx, ball.dy)
                            ball.dx = 0
                            ball.dy = 0
                            # If this bot has possession, update ball position with smooth rotation (existing logic continues)
                    # Non-closest bots do not affect the ball (no bounce/push)

        # --- Bot-bot collision detection ---
        num_bots = len(self.agents)
        possession_gap = 100.0  # Base gap for team in possession
        defender_possession_gap = 150.0  # Larger gap for defenders in possession
        minimal_gap = 30.0     # Smaller gap to prevent complete overlap
        
        for i in range(num_bots):
            for j in range(i + 1, num_bots):
                bot1 = self.agents[i]
                bot2 = self.agents[j]
                
                # Skip separation rules for goalkeepers
                if not bot1.uses_separation_rule or not bot2.uses_separation_rule:
                    separation_gap = 0
                # If both are defenders from same team in possession, use larger gap
                elif (bot1.team == bot2.team == self.possession_team and 
                      isinstance(bot1.position_brain, DefenderBrain) and 
                      isinstance(bot2.position_brain, DefenderBrain)):
                    separation_gap = defender_possession_gap
                # If same team and has possession, use normal possession gap
                elif bot1.team == bot2.team and bot1.team == self.possession_team:
                    separation_gap = possession_gap
                # If same team but not in possession, use minimal gap
                elif bot1.team == bot2.team:
                    separation_gap = minimal_gap
                # If different teams, use minimal gap
                else:
                    separation_gap = minimal_gap
                
                dx = bot2.x - bot1.x
                dy = bot2.y - bot1.y
                dist = (dx ** 2 + dy ** 2) ** 0.5
                min_dist = bot1.radius + bot2.radius + separation_gap

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
                    
                    # Visual feedback for Blue's shot
                    goal_center_x = 0  # Left goal
                    goal_center_y = FIELD_HEIGHT // 2
                    self.canvas.create_line(
                        ball.x, ball.y,
                        goal_center_x, goal_center_y,
                        fill='purple',
                        width=2,
                        dash=(4, 4),
                        tags='dynamic'
                    )

        # --- Red attacking Blue's goal (RIGHT) ---
        elif self.last_touch_team == 'Red':
            if ball.dx > 0 and ball.x >= 3 * FIELD_WIDTH // 4:
                if self.elapsed_time - self.last_shot_time > self.shot_cooldown:
                    self.last_shot_team = self.last_touch_team
                    self.stats['Red']['shots_on_target'] += 1
                    self.last_shot_time = self.elapsed_time
                    print("Red shot on target!")
                    
                    # Visual feedback for Red's shot
                    goal_center_x = FIELD_WIDTH  # Right goal
                    goal_center_y = FIELD_HEIGHT // 2
                    self.canvas.create_line(
                        ball.x, ball.y,
                        goal_center_x, goal_center_y,
                        fill='purple',
                        width=2,
                        dash=(4, 4),
                        tags='dynamic'
                    )

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
            ("Passes (Completed/Attempted)", 'passes'),
            ("Possession (%)", None),
            ("Tackles", 'tackles'),
        ]

        for i, (label_text, stat_key) in enumerate(stat_labels):
            tk.Label(stats_frame, text=label_text, font=("Arial", 12), fg="white", bg="navy", width=20,
                     anchor='w').grid(row=i, column=0, sticky='w')

            if stat_key == 'passes':
                red_value = f"{self.stats['Red']['passes_completed']}/{self.stats['Red']['passes_attempted']}"
                blue_value = f"{self.stats['Blue']['passes_completed']}/{self.stats['Blue']['passes_attempted']}"
            elif stat_key is not None:
                red_value = self.stats['Red'][stat_key]
                blue_value = self.stats['Blue'][stat_key]
            else:
                red_value = f"{red_possession_pct:.1f}%"
                blue_value = f"{blue_possession_pct:.1f}%"

            tk.Label(stats_frame, text=str(red_value), font=("Arial", 12), fg="red", bg="navy", width=10).grid(row=i,
                                                                                                               column=1)
            tk.Label(stats_frame, text=str(blue_value), font=("Arial", 12), fg="blue", bg="navy", width=10).grid(row=i,
                                                                                                                 column=2)

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
            ("Passes (Completed/Attempted)", 'passes'),
            ("Possession (%)", None),
            ("Tackles", 'tackles'),
        ]

        for i, (label_text, stat_key) in enumerate(stat_labels):
            tk.Label(stats_frame, text=label_text, font=("Arial", 12), fg="white", bg="navy", width=20,
                     anchor='w').grid(row=i, column=0)

            if stat_key == 'passes':
                red_value = f"{self.stats['Red']['passes_completed']}/{self.stats['Red']['passes_attempted']}"
                blue_value = f"{self.stats['Blue']['passes_completed']}/{self.stats['Blue']['passes_attempted']}"
            elif stat_key is not None:
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
        self.shot_cooldown = 20
        
        # Ball possession and control variables
        self.ball_possessing_bot = None
        self.possession_start_time = -1
        self.possession_duration = 18  # Reduced from 45 to 18 frames for faster rotation
        self.initial_contact_angle = 0
        self.target_release_angle = 0
        self.ball_distance = 0
        self.stored_ball_speed = (0, 0)
        self.target_teammate = None
        self.second_target = None
        self.possession_buffer = 35  # Increased buffer for more reliable possession
        
        # Pass detection variables
        self.pass_window = 60  # Increased to 60 frames (about 1 second)
        self.min_pass_distance = 50  # Minimum distance for a pass to be counted
        self.last_touch_team = None
        self.last_touch_bot_id = None
        self.last_touch_time = -4
        self.last_touch_pos = None  # Store position of last touch
        self.potential_pass_in_progress = False

        self.stats = {
            'Red': {
                'goals_scored': 0,
                'goals_conceded': 0,
                'shots_on_target': 0,
                'saves': 0,
                'possession_time': 0,
                'tackles': 0,
                'passes_completed': 0,
                'passes_attempted': 0
            },
            'Blue': {
                'goals_scored': 0,
                'goals_conceded': 0,
                'shots_on_target': 0,
                'saves': 0,
                'possession_time': 0,
                'tackles': 0,
                'passes_completed': 0,
                'passes_attempted': 0
            }
        }

        self._draw_pitch()

    def _smooth_step(self, t):
        """
        Smooth step function for more natural ball rotation
        Creates an ease-in-out effect
        """
        return t * t * (3 - 2 * t)

    def calculate_teammate_score(self, passer, receiver):
        """Calculate a single teammate's score based on all factors."""
        if not receiver:
            return 0.0
            
        dx = receiver.x - passer.x
        dy = receiver.y - passer.y
        dist = math.hypot(dx, dy)
        
        # Skip if outside valid passing range
        MAX_PASS_DISTANCE = 600
        MIN_PASS_DISTANCE = 50
        if dist > MAX_PASS_DISTANCE or dist < MIN_PASS_DISTANCE:
            return 0.0
            
        # Calculate all individual scores
        position_score = 1.0 - ((dist - MIN_PASS_DISTANCE) / (MAX_PASS_DISTANCE - MIN_PASS_DISTANCE))
        
        # Get ball direction for angle score
        ball = next((o for o in self.passive_objects if hasattr(o, 'is_ball') and o.is_ball), None)
        angle_to_teammate = math.atan2(dy, dx)
        
        if ball and (ball.dx != 0 or ball.dy != 0):
            ball_direction = math.atan2(ball.dy, ball.dx)
            angle_diff = abs(self.normalize_angle(angle_to_teammate - ball_direction))
            angle_score = 1.0 - (angle_diff / math.pi)
        else:
            forward_angle = math.pi if passer.team == 'Red' else 0
            angle_diff = abs(self.normalize_angle(angle_to_teammate - forward_angle))
            angle_score = 1.0 - (angle_diff / math.pi)
        
        space_score = self.calculate_space_score(receiver)
        progress_score = self.calculate_progress_score(passer, receiver)
        
        # Combine scores with weights
        return (
            0.25 * position_score +
            0.2 * angle_score +
            0.2 * space_score +
            0.35 * progress_score
        )

    def interpolate_angle(self, start, end, t, clockwise):
        # Normalize angles to [0, 2π)
        start = start % (2 * math.pi)
        end = end % (2 * math.pi)
        if clockwise:
            if start < end:
                start += 2 * math.pi
            angle = start - (start - end) * t
        else:
            if end < start:
                end += 2 * math.pi
            angle = start + (end - start) * t
        return angle % (2 * math.pi)

    def should_shoot_striker(self, bot):
        # Striker should shoot if close to the opponent's goal and not heavily marked
        is_left_team = bot.team == 'Red'
        goal_x = FIELD_WIDTH if is_left_team else 0
        # Distance to goal
        distance_to_goal = abs(goal_x - bot.x)
        # Only shoot if within 40% of field width to goal
        close_enough = distance_to_goal < FIELD_WIDTH * 0.4
        # Check for nearby opponents (marking)
        MARKING_DISTANCE = 100
        opponents = [agent for agent in self.agents if agent.team != bot.team]
        min_distance = min((math.hypot(agent.x - bot.x, agent.y - bot.y) for agent in opponents), default=9999)
        not_marked = min_distance > MARKING_DISTANCE
        return close_enough and not_marked