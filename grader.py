import math
from env import HospitalEnv
 
def grade():
    env = HospitalEnv()
    state = env.reset()

    total_reward = 0
    steps = 0
    done = False

    while not done and steps < 10:
        action = 0
        state, reward, done, _ = env.step(action)
        # print(f"Step {steps} → reward: {reward}")
        total_reward += reward
        steps += 1

    # print("TOTAL:", total_reward)
    # print("STEPS:", steps)

    if steps == 0:
        return 0.5

    raw_score = math.tanh(total_reward / 50)
    score = (raw_score + 1) / 2

    epsilon = 1e-3
    score = min(1 - epsilon, max(epsilon, score))

    # print("RAW SCORE:", raw_score)
    # print("FINAL SCORE:", score)

    return score


if __name__ == "__main__":
    print("Score:", grade())