import tkinter as tk
import time
from football_field import FootballField
from bot_base import Bot
from ball import Ball
from brains import ReactiveBrain, RandomWanderBrain, ChargeAtBallBrain, GoalkeeperBrain, StrikerBrain

from ball import FIELD_WIDTH, FIELD_HEIGHT

class ExperimentRunner:
    def __init__(self, bot_brains, num_runs=1, match_duration=30):  # 2 minutes
        self.bot_brains = bot_brains
        self.num_runs = num_runs
        self.match_duration = match_duration  # in seconds
        self.results = {name: [] for name in bot_brains.keys()}

    def run(self):
        for name, brain_factory in self.bot_brains.items():
            print(f"\nRunning experiments for: {name}")
            for i in range(self.num_runs):
                score = self._run_single_match(brain_factory, f"{name} - Run {i+1}")
                self.results[name].append(score)
                print(f"  Run {i+1}: Red {score['Red']} - Blue {score['Blue']}")

        self._print_summary()

    def _run_single_match(self, brain_factory, label):
        root = tk.Tk()
        root.title("Robot Football Experiment")

        field = FootballField(root)

        # Add experiment label display
        label_widget = tk.Label(root, text=label, font=("Arial", 16), bg="black", fg="white")
        label_widget.place(x=FIELD_WIDTH // 2 - 100, y=10)

        # Add score display
        score_var = tk.StringVar()
        score_label = tk.Label(root, textvariable=score_var, font=("Arial", 18, "bold"), bg="black", fg="white")
        score_label.place(x=FIELD_WIDTH // 2 - 60, y=40)

        ball = Ball()
        field.add_passive_object(ball)

        red_bot = Bot(x=100, y=FIELD_HEIGHT // 2, team_color='Red', brain=brain_factory())
        blue_bot = Bot(x=FIELD_WIDTH - 100, y=FIELD_HEIGHT // 2, team_color='Blue', brain=brain_factory())

        field.add_agent(red_bot)
        field.add_agent(blue_bot)

        end_time = time.time() + self.match_duration

        def loop():
            if time.time() < end_time:
                field.update()
                score_text = f"Red: {field.score['Red']}  |  Blue: {field.score['Blue']}"
                score_var.set(score_text)
                root.after(50, loop)
            else:
                root.destroy()

        root.after(50, loop)
        root.mainloop()
        return field.score

    def _print_summary(self):
        print("\nSummary of Results:")
        for name, scores in self.results.items():
            red_total = sum(s['Red'] for s in scores)
            blue_total = sum(s['Blue'] for s in scores)
            print(f"{name}: Avg Red {red_total / self.num_runs:.2f}, Avg Blue {blue_total / self.num_runs:.2f}")


if __name__ == '__main__':
    brains_to_test = {
        'ReactiveBrain': ReactiveBrain,
        'RandomWanderBrain': RandomWanderBrain,
        'ChargeAtBallBrain': ChargeAtBallBrain
    }

    runner = ExperimentRunner(bot_brains=brains_to_test, num_runs=1, match_duration=30)
    runner.run()
