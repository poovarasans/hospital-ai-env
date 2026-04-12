from fastapi import FastAPI
from pydantic import BaseModel
import sys
import os

# Add parent directory to path to import env
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from env import HospitalEnv
import uvicorn

app = FastAPI()

env = None
current_mode = "easy"


class StepInput(BaseModel):
    action: int


class ResetInput(BaseModel):
    mode: str = "easy"


@app.post("/reset")
def reset(data: ResetInput = None):
    global env, current_mode
    
    # Support both with and without body
    mode = data.mode if data else "easy"
    if mode not in ["easy", "medium", "hard"]:
        mode = "easy"
    
    current_mode = mode
    env = HospitalEnv(mode=mode)
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

def main():
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)


if __name__ == "__main__":
    main()