import math
import os
from env import HospitalEnv


def grade_level(mode):
    """Grade a specific difficulty level."""
    env = HospitalEnv(mode=mode)
    state = env.reset()

    total_reward = 0
    steps = 0
    done = False

    while not done and steps < 10:
        action = 0
        state, reward, done, _ = env.step(action)
        total_reward += reward
        steps += 1

    if steps <= 0:
        return 0.5

    denominator = max(1, steps * 10)
    raw_score = total_reward / denominator

    if not math.isfinite(raw_score):
        raw_score = 0.5

    score = 1 / (1 + math.exp(-raw_score))

    epsilon = 1e-7
    score = max(epsilon, min(1 - epsilon, score))

    return score


def grade():
    """Grade based on task context."""
    task = os.getenv("OPENENV_TASK", None)
    
    if task and task in ["easy", "medium", "hard"]:
        return grade_level(task)
    else:
        return [grade_level(mode) for mode in ["easy", "medium", "hard"]]


if __name__ == "__main__":
    grade()