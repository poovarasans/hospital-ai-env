import math
import os
from env import HospitalEnv


def grade_level(mode):
    
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

    raw_score = max(-10, min(10, raw_score))
    
    score = 1 / (1 + math.exp(-raw_score))

    score = max(0.01, min(0.99, score))

    return score


def grade():

    task = os.getenv("OPENENV_TASK", "easy")
    
    if task not in ["easy", "medium", "hard"]:
        task = "easy"
    
    return grade_level(task)


if __name__ == "__main__":
    grade()