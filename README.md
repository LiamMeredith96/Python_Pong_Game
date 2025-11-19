# Python Pong AI with NEAT

This project is a Pong game implemented with `pygame`, with an AI trained using the NEAT algorithm from neat-python.

There are three main ways to use the project:

1. Train the AI (NEAT, AI vs AI)
2. Test the trained AI against a human (Human vs AI)
3. Play a separate manual 2-player Pong game (Human vs Human)


# Requirements

- Python 3.12.7
- pip

Python dependencies:
    pygame==2.6.1
    neat-python==0.92


# Installation

1. Clone or download the repository:

        git clone https://github.com/LiamMeredith96/Python_Pong_Game
        cd Python_Pong_Game

2. Create a virtual environment:

        python -m venv .venv

3. Activate the virtual environment (Windows, PowerShell):

        .\.venv\Scripts\Activate

4. Install dependencies:

        pip install -r requirements.txt

Training mode (NEAT, AI vs AI)

In training mode, NEAT evolves neural networks that control the paddles.

- Both paddles are controlled by AI during training.
- Each genome represents a neural network.
- Two networks are paired against each other in Pong matches.
- Fitness is based on paddle-ball hits and game outcomes.


At the bottom of `main.py`, enable training mode:

# Uncomment one of these depending on whether you want to train or test:

    run_neat(config)
    test_ai(config)