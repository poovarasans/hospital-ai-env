from fastapi import FastAPI
from pydantic import BaseModel
from env import HospitalEnv

app = FastAPI()

env = None


class StepInput(BaseModel):
    action: int


@app.post("/reset")
def reset():
    global env

    env = HospitalEnv(mode="easy")
    state = env.reset()

    return {"state": state}


@app.post("/step")
def step(data: StepInput):
    global env

    if env is None:
        return {
            "state": {},
            "reward": 0.0,
            "done": False,
            "info": {"error": "env not initialized"}
        }

    try:
        state, reward, done, info = env.step(data.action)
    except Exception as e:
        return {
            "state": {},
            "reward": 0.0,
            "done": False,
            "info": {"error": str(e)}
        }

    return {
        "state": state,
        "reward": float(round(reward, 2)),
        "done": done,
        "info": info
    }