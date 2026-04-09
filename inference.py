import os
import json
from env import HospitalEnv

def choose_action(patients):
    return max(
        range(len(patients)),
        key=lambda i: patients[i]["severity"] + patients[i]["wait"]
    )

def run_episode(mode):
    env = HospitalEnv(mode=mode)
    state = env.reset()

    print("[START]")

    done = False

    try:
        while not done:

            patients = state["patients"]

            if not patients:
                break

            action = choose_action(patients)

            state, reward, done, info = env.step(action)

            print("[STEP]", json.dumps({
                "reward": round(reward, 2),
                "done": str(done).lower(),
                "success": "true",
                "error": None
            }))

    except Exception as e:
        print("[STEP]", json.dumps({
            "reward": 0.00,
            "done": "true",
            "success": "false",
            "error": str(e)
        }))

    finally:
        print("[END]")


if __name__ == "__main__":
    run_episode("easy")
    run_episode("medium")
    run_episode("hard")