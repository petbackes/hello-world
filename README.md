# Little Snake 🌱

A tiny pastel arcade garden: collect pink apples, grow, and avoid your own tail.
Keyboard controls, pause, restart, increasing speed, and a session high score.

## Play

Python 3.10+ with Tkinter and a desktop display:

```bash
python play.py
```

Use arrows or WASD to turn, Space to pause, and R to restart. Reverse turns
are ignored. An episode also ends after four board areas without eating.
Tkinter comes with most Windows/macOS Python installers; on Ubuntu install
`python3-tk`. A headless notebook cannot open the game window.

## Inside

- `snake.py`: deterministic seeded rules, relative actions, rewards and observations.
- `play.py`: standard-library Tkinter interface; no pip dependencies.
- `test_snake.py`: growth, wall collisions, tail movement and board completion.

```bash
python -m unittest -v
```

Validation: all five rule tests and Python compilation passed. Tkinter imported
successfully, but the graphical window was not visually tested in the headless
build environment.

## Project collection

- [Snake Q-learning](https://github.com/petbackes/LieToAI): teach a snake through trial and error.
- [Kaggle lab](https://github.com/petbackes/desktop-tutorial): Titanic and House Prices baselines.

Companion repositories may require permission. Generated with AI assistance as
an educational starting point; this is not a claim of prior research or competition results.
