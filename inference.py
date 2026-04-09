import os
from env import HospitalEnv

API_BASE_URL = os.getenv("API_BASE_URL","https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME","gpt-4o-mini")
HF_TOKEN = os.getenv("HF_TOKEN")

if HF_TOKEN is None:
    raise ValueError("HF_TOKEN missing")

def run_episode(mode="easy"):
    env = HospitalEnv(mode=mode)
    state = env.reset()

    total_reward = 0.0
    step_count = 0

    print("[START]")

    try:
        done = False

        while not done:
            patients = state["patients"]

            if not patients:
                break

            # simple policy (your logic)
            action = max(
                range(len(patients)),
                key=lambda i: patients[i]["severity"] + patients[i]["wait"]
            )

            state, reward, done, info = env.step(action)

            total_reward += reward
            step_count += 1

            print(f"[STEP] reward={reward:.2f} done={str(done).lower()}")

        print(f"[END] total_reward={total_reward:.2f} steps={step_count}")

    except Exception as e:
        print(f"[END] error={str(e)}")


if __name__ == "__main__":
    run_episode("easy")
    run_episode("medium")
    run_episode("hard")