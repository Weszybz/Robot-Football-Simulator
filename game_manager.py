import tkinter as tk
from football_field import FootballField
from bot_base import Bot
from ball import Ball
from brains import ReactiveBrain, RandomWanderBrain, ChargeAtBallBrain, GoalkeeperBrain, StrikerBrain


def create_game():
    root = tk.Tk()
    root.title("Robot Football Arena")

    field = FootballField(root)

    # Create ball
    ball = Ball()
    field.add_passive_object(ball)

    # Create bots with different brains
    red_bot = Bot(x=50, y=FIELD_HEIGHT // 2, team_color='Red', brain=GoalkeeperBrain())
    blue_bot = Bot(x=FIELD_WIDTH - 50, y=FIELD_HEIGHT // 2, team_color='Blue', brain=ChargeAtBallBrain())

    field.add_agent(red_bot)
    field.add_agent(blue_bot)

    field.run()
    root.mainloop()


if __name__ == '__main__':
    from ball import FIELD_WIDTH, FIELD_HEIGHT  # import constants
    create_game()
