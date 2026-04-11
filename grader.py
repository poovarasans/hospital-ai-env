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
        total_reward += reward
        steps += 1

    if steps == 0:
        return 0.5

    raw_score = total_reward / (steps * 10)
    
    epsilon = 1e-6
    score = min(1 - epsilon, max(epsilon, raw_score))

    return score


if __name__ == "__main__":
    print("Score:", grade())