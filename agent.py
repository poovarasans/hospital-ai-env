# agent.py
from env import HospitalEnv

for mode in ["easy", "medium", "hard"]:
    print(f"\n=== Testing {mode.upper()} mode ===")
    
    env = HospitalEnv(mode=mode)
    state = env.reset()

    done = False
    total = 0

    while not done:
        patients = state["patients"]

        if not patients:
            break

        action = max(
            range(len(patients)),
            key=lambda i: patients[i]["severity"] + patients[i]["wait"]
        )

        state, reward, done, _ = env.step(action)
        total += reward

    print(f"Final Reward: {total}")
    print(f"Patients Treated: {state['treated']}")