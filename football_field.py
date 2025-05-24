import tkinter as tk
import time
import random
import tkinter.messagebox
import math

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
                self.possession_team = closest_bot.team

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
                    if self.ball_possessing_bot is None:
                        self.ball_possessing_bot = closest_bot
                        self.possession_start_time = self.elapsed_time
                        
                        # Calculate initial contact angle from ball's direction of travel
                        if ball.dx != 0 or ball.dy != 0:
                            self.initial_contact_angle = math.atan2(-ball.dy, -ball.dx)
                        else:
                            self.initial_contact_angle = math.atan2(closest_bot.y - ball.y, closest_bot.x - ball.x)
                        
                        # Find nearest teammate and their angle
                        teammate_info = self.find_nearest_teammate(closest_bot)
                        if teammate_info:
                            self.target_teammate, target_angle = teammate_info
                            # Determine optimal rotation direction
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
                        
                        self.ball_distance = distance
                        self.stored_ball_speed = (ball.dx, ball.dy)
                        ball.dx = 0
                        ball.dy = 0
                        
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
                        
                        # Update target angle continuously based on teammate movement
                        if self.target_teammate:
                            new_dx = self.target_teammate.x - closest_bot.x
                            new_dy = self.target_teammate.y - closest_bot.y
                            new_dist = math.hypot(new_dx, new_dy)
                            
                            # Check if current target is still valid
                            MAX_PASS_DISTANCE = 600
                            if new_dist > MAX_PASS_DISTANCE:
                                # Try to find a new target
                                teammate_info = self.find_nearest_teammate(closest_bot)
                                if teammate_info:
                                    # Only update target if we find a significantly better option
                                    new_teammate, new_angle = teammate_info
                                    if new_teammate != self.target_teammate:
                                        # Calculate scores for current and new target
                                        current_score = self.calculate_teammate_score(closest_bot, self.target_teammate)
                                        new_score = self.calculate_teammate_score(closest_bot, new_teammate)
                                        
                                        # Only switch if new target is significantly better (20% improvement)
                                        if new_score > current_score * 1.2:
                                            self.target_teammate = new_teammate
                                            self.target_release_angle = new_angle
                                            # Reset rotation direction for new target
                                            _, self.rotate_clockwise = self.get_shortest_rotation(
                                                self.initial_contact_angle, new_angle
                                            )
                            else:
                                # Update angle to current target
                                new_target_angle = math.atan2(new_dy, new_dx)
                                # Update target angle with optimal rotation
                                self.target_release_angle, self.rotate_clockwise = self.get_shortest_rotation(
                                    self.initial_contact_angle, new_target_angle
                                )
                        
                        if possession_time < self.possession_duration:
                            # Calculate interpolation factor (0 to 1)
                            t = possession_time / self.possession_duration
                            t = self._smooth_step(t)
                            
                            # Calculate the angle difference based on rotation direction
                            if self.rotate_clockwise:
                                current_angle = self.initial_contact_angle - (
                                    self.normalize_angle(self.initial_contact_angle - self.target_release_angle) * t
                                )
                            else:
                                current_angle = self.initial_contact_angle + (
                                    self.normalize_angle(self.target_release_angle - self.initial_contact_angle) * t
                                )
                            
                            # Update ball position based on interpolated angle
                            ball.x = closest_bot.x + math.cos(current_angle) * self.ball_distance
                            ball.y = closest_bot.y + math.sin(current_angle) * self.ball_distance
                            
                            # Draw line only to current target
                            if self.target_teammate:
                                self.canvas.create_line(
                                    closest_bot.x, closest_bot.y,
                                    self.target_teammate.x, self.target_teammate.y,
                                    fill='yellow', width=1, dash=(4, 4),
                                    tags='dynamic'
                                )
                        else:
                            # Only release if we have a valid target
                            if self.target_teammate:
                                dx = self.target_teammate.x - closest_bot.x
                                dy = self.target_teammate.y - closest_bot.y
                                dist = math.hypot(dx, dy)
                                
                                # Calculate base speed from stored momentum
                                base_speed = math.hypot(self.stored_ball_speed[0], self.stored_ball_speed[1])
                                
                                # Calculate appropriate pass speed based on distance
                                pass_speed = self.calculate_pass_speed(dist, base_speed)
                                
                                # Apply the calculated speed in the direction of the teammate
                                ball.dx = (dx / dist) * pass_speed
                                ball.dy = (dy / dist) * pass_speed
                            else:
                                # No valid target, maintain possession
                                self.possession_start_time = self.elapsed_time - (self.possession_duration - 1)
                                return
                            
                            self.ball_possessing_bot = None
                            self.possession_start_time = -1
                            self.target_teammate = None
                    
                    # If different bot touches the ball, transfer possession
                    elif self.ball_possessing_bot != closest_bot:
                        self.ball_possessing_bot = closest_bot
                        self.possession_start_time = self.elapsed_time
                        
                        # Calculate initial contact angle from ball's direction of travel
                        if ball.dx != 0 or ball.dy != 0:
                            self.initial_contact_angle = math.atan2(-ball.dy, -ball.dx)
                        else:
                            self.initial_contact_angle = math.atan2(closest_bot.y - ball.y, closest_bot.x - ball.x)
                        
                        # Find nearest teammate and their angle
                        teammate_info = self.find_nearest_teammate(closest_bot)
                        if teammate_info:
                            self.target_teammate, target_angle = teammate_info
                            # Determine optimal rotation direction
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
        """Find the best teammate to pass to based on multiple factors."""
        teammates = [agent for agent in self.agents if agent.team == bot.team and agent != bot]
        if not teammates:
            return None
            
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
        
        for teammate in teammates:
            dx = teammate.x - bot.x
            dy = teammate.y - bot.y
            dist = math.hypot(dx, dy)
            
            # Skip if outside valid passing range
            if dist > MAX_PASS_DISTANCE or dist < MIN_PASS_DISTANCE:
                continue
                
            # Calculate base position score (1.0 at MIN_PASS_DISTANCE, 0.0 at MAX_PASS_DISTANCE)
            position_score = 1.0 - ((dist - MIN_PASS_DISTANCE) / (MAX_PASS_DISTANCE - MIN_PASS_DISTANCE))
            
            # Calculate angle to teammate
            angle_to_teammate = math.atan2(dy, dx)
            
            # Calculate angle score based on current ball direction or bot's team direction
            if ball_direction is not None:
                # Prefer passes that continue the ball's general direction of movement
                angle_diff = abs(self.normalize_angle(angle_to_teammate - ball_direction))
                angle_score = 1.0 - (angle_diff / math.pi)  # 1.0 for same direction, 0.0 for opposite
            else:
                # If ball is stationary, prefer forward passes for the team's direction
                forward_angle = math.pi if bot.team == 'Red' else 0
                angle_diff = abs(self.normalize_angle(angle_to_teammate - forward_angle))
                angle_score = 1.0 - (angle_diff / math.pi)
            
            # Calculate space score (how free the teammate is from opponents)
            space_score = self.calculate_space_score(teammate)
            
            # Calculate progress score (how much closer to goal the teammate is)
            progress_score = self.calculate_progress_score(bot, teammate)
            
            # Increase weight of progress score to emphasize forward play
            final_score = (
                0.25 * position_score +   # Distance is important
                0.2 * angle_score +       # Prefer passes that maintain momentum
                0.2 * space_score +       # Good amount of space around teammate
                0.35 * progress_score     # Increased emphasis on forward progression
            )
            
            teammate_scores.append((final_score, teammate, angle_to_teammate))
        
        # If no valid teammates found
        if not teammate_scores:
            return None
            
        # Sort by score and return the best option
        teammate_scores.sort(reverse=True, key=lambda x: x[0])
        return teammate_scores[0][1], teammate_scores[0][2]

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
        MIN_SPEED = 5.0
        
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
            for bot in self.agents:
                dx = ball.x - bot.x
                dy = ball.y - bot.y
                dist = (dx ** 2 + dy ** 2) ** 0.5
                min_dist = ball.radius + bot.radius

                if dist < min_dist:
                    # If ball is not possessed, start possession
                    if self.ball_possessing_bot is None:
                        self.ball_possessing_bot = bot
                        self.possession_start_time = self.elapsed_time
                        
                        # Calculate initial contact angle from ball's direction of travel
                        if ball.dx != 0 or ball.dy != 0:
                            self.initial_contact_angle = math.atan2(-ball.dy, -ball.dx)
                        else:
                            self.initial_contact_angle = math.atan2(dy, dx)
                        
                        # Find nearest teammate and their angle
                        teammate_info = self.find_nearest_teammate(bot)
                        if teammate_info:
                            self.target_teammate, target_angle = teammate_info
                            # Determine optimal rotation direction
                            self.target_release_angle, self.rotate_clockwise = self.get_shortest_rotation(
                                self.initial_contact_angle, target_angle
                            )
                        else:
                            # If no teammates, use default forward direction
                            default_angle = math.pi if bot.team == 'Red' else 0
                            self.target_release_angle, self.rotate_clockwise = self.get_shortest_rotation(
                                self.initial_contact_angle, default_angle
                            )
                            self.target_teammate = None
                        
                        self.ball_distance = min_dist
                        self.stored_ball_speed = (ball.dx, ball.dy)
                        ball.dx = 0
                        ball.dy = 0
                        
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
                    
                    # If this bot has possession, update ball position with smooth rotation
                    if self.ball_possessing_bot == bot:
                        possession_time = self.elapsed_time - self.possession_start_time
                        
                        # Update target angle continuously based on teammate movement
                        if self.target_teammate:
                            new_dx = self.target_teammate.x - bot.x
                            new_dy = self.target_teammate.y - bot.y
                            new_dist = math.hypot(new_dx, new_dy)
                            
                            # Check if current target is still valid
                            MAX_PASS_DISTANCE = 600
                            if new_dist > MAX_PASS_DISTANCE:
                                # Try to find a new target
                                teammate_info = self.find_nearest_teammate(bot)
                                if teammate_info:
                                    # Only update target if we find a significantly better option
                                    new_teammate, new_angle = teammate_info
                                    if new_teammate != self.target_teammate:
                                        # Calculate scores for current and new target
                                        current_score = self.calculate_teammate_score(bot, self.target_teammate)
                                        new_score = self.calculate_teammate_score(bot, new_teammate)
                                        
                                        # Only switch if new target is significantly better (20% improvement)
                                        if new_score > current_score * 1.2:
                                            self.target_teammate = new_teammate
                                            self.target_release_angle = new_angle
                                            # Reset rotation direction for new target
                                            _, self.rotate_clockwise = self.get_shortest_rotation(
                                                self.initial_contact_angle, new_angle
                                            )
                            else:
                                # Update angle to current target
                                new_target_angle = math.atan2(new_dy, new_dx)
                                # Update target angle with optimal rotation
                                self.target_release_angle, self.rotate_clockwise = self.get_shortest_rotation(
                                    self.initial_contact_angle, new_target_angle
                                )
                        
                        if possession_time < self.possession_duration:
                            # Calculate interpolation factor (0 to 1)
                            t = possession_time / self.possession_duration
                            t = self._smooth_step(t)
                            
                            # Calculate the angle difference based on rotation direction
                            if self.rotate_clockwise:
                                current_angle = self.initial_contact_angle - (
                                    self.normalize_angle(self.initial_contact_angle - self.target_release_angle) * t
                                )
                            else:
                                current_angle = self.initial_contact_angle + (
                                    self.normalize_angle(self.target_release_angle - self.initial_contact_angle) * t
                                )
                            
                            # Update ball position based on interpolated angle
                            ball.x = bot.x + math.cos(current_angle) * self.ball_distance
                            ball.y = bot.y + math.sin(current_angle) * self.ball_distance
                            
                            # Draw line only to current target
                            if self.target_teammate:
                                self.canvas.create_line(
                                    bot.x, bot.y,
                                    self.target_teammate.x, self.target_teammate.y,
                                    fill='yellow', width=1, dash=(4, 4),
                                    tags='dynamic'
                                )
                        else:
                            # Only release if we have a valid target
                            if self.target_teammate:
                                dx = self.target_teammate.x - bot.x
                                dy = self.target_teammate.y - bot.y
                                dist = math.hypot(dx, dy)
                                
                                # Calculate base speed from stored momentum
                                base_speed = math.hypot(self.stored_ball_speed[0], self.stored_ball_speed[1])
                                
                                # Calculate appropriate pass speed based on distance
                                pass_speed = self.calculate_pass_speed(dist, base_speed)
                                
                                # Apply the calculated speed in the direction of the teammate
                                ball.dx = (dx / dist) * pass_speed
                                ball.dy = (dy / dist) * pass_speed
                            else:
                                # No valid target, maintain possession
                                self.possession_start_time = self.elapsed_time - (self.possession_duration - 1)
                                return
                            
                            self.ball_possessing_bot = None
                            self.possession_start_time = -1
                            self.target_teammate = None
                    
                    # If different bot touches the ball, transfer possession
                    elif self.ball_possessing_bot != bot:
                        self.ball_possessing_bot = bot
                        self.possession_start_time = self.elapsed_time
                        
                        # Calculate initial contact angle from ball's direction of travel
                        if ball.dx != 0 or ball.dy != 0:
                            self.initial_contact_angle = math.atan2(-ball.dy, -ball.dx)
                        else:
                            self.initial_contact_angle = math.atan2(dy, dx)
                        
                        # Find nearest teammate and their angle
                        teammate_info = self.find_nearest_teammate(bot)
                        if teammate_info:
                            self.target_teammate, target_angle = teammate_info
                            # Determine optimal rotation direction
                            self.target_release_angle, self.rotate_clockwise = self.get_shortest_rotation(
                                self.initial_contact_angle, target_angle
                            )
                        else:
                            # If no teammates, use default forward direction
                            default_angle = math.pi if bot.team == 'Red' else 0
                            self.target_release_angle, self.rotate_clockwise = self.get_shortest_rotation(
                                self.initial_contact_angle, default_angle
                            )
                            self.target_teammate = None
                        
                        self.ball_distance = min_dist
                        self.stored_ball_speed = (ball.dx, ball.dy)
                        ball.dx = 0
                        ball.dy = 0

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
        self.possession_duration = 30  # Reduced from 45 to 30 frames for faster rotation
        self.initial_contact_angle = 0
        self.target_release_angle = 0
        self.ball_distance = 0
        self.stored_ball_speed = (0, 0)
        self.target_teammate = None
        
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