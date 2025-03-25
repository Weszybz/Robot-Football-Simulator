# 🤖 Robot Football Simulator

A modular 2D simulation where intelligent agents play football using various perception and decision-making systems. Built in Python using `tkinter`.

---

## ⚽ Overview

This project explores how different sensing systems influence robot performance in a dynamic football environment. Autonomous bots use different AI strategies to intercept the ball, block goals, and score.

### 🧠 Core Features

- **Simulation Engine**: 2D football field with scoring, physics, and boundaries
- **Autonomous Bots**:
  - `ReactiveBrain`: turns and charges toward the ball
  - `ChargeAtBallBrain`: aggressively pursues the ball head-on
  - `RandomWanderBrain`: moves unpredictably
- **Ball Physics**: bounces off walls and resets on goal
- **Real-time Scoreboard**: displayed at top-center of the game
- **Experiment Mode**: run multiple matches to compare AI strategies
- **Visual Display**: includes match label and performance output

---

## 🧪 Research Purpose

> “How do different robot perception systems impact their ability to score goals, block shots, and react in real time?”

Experiments are logged and summarized to compare each bot’s success across multiple 2-minute matches.

---

## 🚀 Getting Started

### ✅ Requirements

- Python 3.6+
- `tkinter` (included in most Python installs)

### ▶ Run a Single Match

```bash
python game_manager.py
```

### 🧪 Run Experiments
```bash
python experiments.py
```

### 🗂 Project Structure
```bash
├── ball.py               # Ball physics and movement
├── bot_base.py           # Bot motion and perception
├── brains.py             # AI strategies for bots
├── football_field.py     # Field layout and canvas drawing
├── game_manager.py       # Run one game with two bots
├── experiments.py        # Automated evaluation of multiple AI brains
└── README.md
```

### 📊 Example Output
```text
Running experiments for: ReactiveBrain
  Run 1: Red 3 - Blue 1
  Run 2: Red 2 - Blue 0
  Run 3: Red 4 - Blue 2

Summary of Results:
ReactiveBrain: Avg Red 3.00, Avg Blue 1.00
```
