import tkinter as tk
from football_field import FootballField
from bot_base import Bot
from ball import Ball
from brains import ReactiveBrain, RandomWanderBrain, ChargeAtBallBrain, GoalkeeperBrain, StrikerBrain, DefenderBrain, MidfielderBrain
from perception import FOVPerception, MemoryPerception, BlackboardPerception, SubsumptionPerception


def create_game():
    root = tk.Tk()
    root.title("Robot Football Arena")

    field = FootballField(root)

    # Create ball
    ball = Ball()
    field.add_passive_object(ball)

    # Create bots with different brains
    red_team = [
        Bot(x=50, y=FIELD_HEIGHT // 2, team_color='Red', position_brain=GoalkeeperBrain(), perception_brain=SubsumptionPerception()),
        Bot(x=200, y=FIELD_HEIGHT // 4, team_color='Red', position_brain=DefenderBrain(role='left_back'), perception_brain=SubsumptionPerception()),
        Bot(x=200, y=3 * FIELD_HEIGHT // 4, team_color='Red', position_brain=DefenderBrain(role='right_back'), perception_brain=SubsumptionPerception()),
        Bot(x=FIELD_WIDTH // 3, y=FIELD_HEIGHT // 2, team_color='Red', position_brain=MidfielderBrain(), perception_brain=SubsumptionPerception()),
        Bot(x=FIELD_WIDTH // 2 - 50, y=FIELD_HEIGHT // 2, team_color='Red', position_brain=StrikerBrain(), perception_brain=SubsumptionPerception()),
    ]
    for bot in red_team:
        field.add_agent(bot)

    blue_team = [
        Bot(x=FIELD_WIDTH - 50, y=FIELD_HEIGHT // 2, team_color='Blue', position_brain=GoalkeeperBrain(), perception_brain=MemoryPerception()),
        Bot(x=FIELD_WIDTH - 200, y=FIELD_HEIGHT // 4, team_color='Blue', position_brain=DefenderBrain(role='left_back'), perception_brain=MemoryPerception()),
        Bot(x=FIELD_WIDTH - 200, y=3 * FIELD_HEIGHT // 4, team_color='Blue', position_brain=DefenderBrain(role='right_back'), perception_brain=MemoryPerception()),
        Bot(x=FIELD_WIDTH * 2 // 3, y=FIELD_HEIGHT // 2, team_color='Blue', position_brain=MidfielderBrain(), perception_brain=MemoryPerception()),
        Bot(x=FIELD_WIDTH // 2 + 50, y=FIELD_HEIGHT // 2, team_color='Blue', position_brain=StrikerBrain(), perception_brain=MemoryPerception())
    ]
    for bot in blue_team:
        field.add_agent(bot)

    field.run()
    root.mainloop()


if __name__ == '__main__':
    from ball import FIELD_WIDTH, FIELD_HEIGHT  # import constants
    create_game()
