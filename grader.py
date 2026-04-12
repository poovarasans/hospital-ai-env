import math
import os
import sys


def choose_action(patients):
    """Choose best patient based on severity + wait time."""
    if not patients:
        return 0.1
    return max(
        range(len(patients)),
        key=lambda i: patients[i]["severity"] + patients[i]["wait"]
    )


def grade_level(mode):
    """Grade a specific difficulty level."""
    try:
        from env import HospitalEnv
    except ImportError as e:
        sys.stderr.write(f"Error importing HospitalEnv: {e}\n")
        return 0.1
    
    try:
        env = HospitalEnv(mode=mode)
        state = env.reset()
    except Exception as e:
        sys.stderr.write(f"Error initializing environment: {e}\n")
        return 0.1

    total_reward = 0
    steps = 0
    done = False

    try:
        while not done and steps < 10:
            patients = state.get("patients", [])
            if not patients:
                break
            
            action = choose_action(patients)
            state, reward, done, _ = env.step(action)
            total_reward += reward
            steps += 1
    except Exception as e:
        sys.stderr.write(f"Error during episode: {e}\n")
        if steps > 0:
            denominator = max(1, steps * 10)
            raw_score = total_reward / denominator
            if not math.isfinite(raw_score):
                raw_score = 0.5
            raw_score = max(-10, min(10, raw_score))
            score = 1 / (1 + math.exp(-raw_score))
            return max(0.01, min(0.99, score))
        return 0.1

    if steps <= 0:
        return 0.1

    denominator = max(1, steps * 10)
    raw_score = total_reward / denominator

    if not math.isfinite(raw_score):
        raw_score = 0.1

    raw_score = max(-10, min(10, raw_score))
    
    score = 1 / (1 + math.exp(-raw_score))

    score = max(0.01, min(0.99, score))

    return score


def grade():
    """Grade the task specified by OPENENV_TASK environment variable."""
    task = os.getenv("OPENENV_TASK", "easy")
    
    if task not in ["easy", "medium", "hard"]:
        task = "easy"
    
    return grade_level(task)


if __name__ == "__main__":
    try:
        score = grade()
        print(score)
    except Exception as e:
        sys.stderr.write(f"Fatal error in grader: {e}\n")
        print(0.1)