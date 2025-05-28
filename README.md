# 🤖 Robot Football Simulator

A modular 2D simulation where intelligent agents play football using various perception and decision-making systems. Built in Python using `tkinter`.

---

## ⚽ Overview

This project explores how different sensing systems influence robot performance in a dynamic football environment. Autonomous bots use different AI strategies to intercept the ball, block goals, and score.

### 🧠 Core Features

- **Simulation Engine**: 2D football field with goals, ball physics, and collision logic
- **Autonomous Bots**:
  - **Position Brains**:
    - `GoalkeeperBrain`, `DefenderBrain`, `MidfielderBrain`, `StrikerBrain` (role-specific behavior)
  - **Perception Brains**:
    - `FOVPerception`: only reacts when the ball is visible within a limited field of view
    - `SubsumptionPerception`: layered decision-making based on priorities
    - `MemoryPerception`: remembers the last seen ball position
    - `BlackboardPerception`: shares ball location among teammates
- **Ball Physics**: velocity control, goal detection
- **Stat Tracking**: goals, shots on target, passes completed, possession, saves, tackles
- **Scoreboard & Timer**: visible at half-time and full-time
- **Experiment Framework**: run automated matchups to test perception systems head-to-head
- **League Format**: agents play each other in a round-robin tournament (Premier League style)

---

## 🧪 Research Purpose

> “How do different robot perception systems impact their ability to score goals, defend, and coordinate under time constraints?”

Experiments are logged and summarised to compare each bot’s success across multiple 2-minute matches.

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
```
