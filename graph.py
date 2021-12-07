import numpy as np
import matplotlib.pyplot as plt


def plot_rewards(rewards: list, test: str):
    plt.plot(rewards)
    plt.ylabel("Reward")
    plt.xlabel("Episodes")
    plt.title(f"Reward per Experience for {test}")
    plt.savefig(f"./static/Reward{test}.png")
    plt.show()
