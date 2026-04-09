# agent.py
from env import HospitalEnv

env = HospitalEnv()
state = env.reset()

done = False
total = 0

while not done:
    patients = state["patients"]

    action = max(
        range(len(patients)),
        key=lambda i: patients[i]["severity"] + patients[i]["wait"]
    )

    state, reward, done, _ = env.step(action)
    total += reward

print("Final Reward:", total)