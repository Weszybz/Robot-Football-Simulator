import tkinter as tk
from football_field import FootballField
from bot_base import Bot
from ball import Ball
from brains import ReactiveBrain, RandomWanderBrain, ChargeAtBallBrain, GoalkeeperBrain, StrikerBrain, DefenderBrain, MidfielderBrain


def create_game():
    root = tk.Tk()
    root.title("Robot Football Arena")

    field = FootballField(root)

    # Create ball
    ball = Ball()
    field.add_passive_object(ball)

    # Create bots with different brains
    red_team = [
        Bot(x=50, y=FIELD_HEIGHT // 2, team_color='Red', brain=GoalkeeperBrain()),
        Bot(x=150, y=FIELD_HEIGHT // 4, team_color='Red', brain=DefenderBrain(role='left_back')),
        Bot(x=150, y=3 * (FIELD_HEIGHT // 4), team_color='Red', brain=DefenderBrain(role='right_back')),
        Bot(x=250, y=FIELD_HEIGHT // 2, team_color='Red', brain=MidfielderBrain()),
        Bot(x=350, y=FIELD_HEIGHT // 2, team_color='Red', brain=StrikerBrain()),
    ]
    for bot in red_team:
        field.add_agent(bot)

    blue_team = [
        Bot(x=FIELD_WIDTH - 50, y=FIELD_HEIGHT // 2, team_color='Blue', brain=GoalkeeperBrain()),
        Bot(x=FIELD_WIDTH - 150, y=FIELD_HEIGHT // 4, team_color='Blue', brain=DefenderBrain(role='left_back')),
        Bot(x=FIELD_WIDTH - 150, y=3 * (FIELD_HEIGHT // 4), team_color='Blue', brain=DefenderBrain(role='right_back')),
        Bot(x=FIELD_WIDTH - 250, y=FIELD_HEIGHT // 2, team_color='Blue', brain=MidfielderBrain()),
        Bot(x=FIELD_WIDTH - 350, y=FIELD_HEIGHT // 2, team_color='Blue', brain=StrikerBrain()),
        ]
    for bot in blue_team:
        field.add_agent(bot)

    field.run()
    root.mainloop()


if __name__ == '__main__':
    from ball import FIELD_WIDTH, FIELD_HEIGHT  # import constants
    create_game()
