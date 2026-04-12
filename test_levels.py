from env import HospitalEnv

for mode in ["easy", "medium", "hard"]:
	print("\nTesting mode:", mode)
	
	env = HospitalEnv(mode=mode)
	state = env.reset()
	print("Initial Patients:", len(state['patients']))

	done = False
	total = 0
	steps = 0

	while not done:
		patients = state["patients"]
		
		if not patients:
			break
		
		# Use optimal action selection (not just action=0)
		action = max(
			range(len(patients)),
			key=lambda i: patients[i]["severity"] + patients[i]["wait"]
		)
		
		state, reward, done, _ = env.step(action)
		total += reward
		steps += 1

	print("Total Rewards:", state["total_reward"], "Treated:", state["treated"], "Steps:", steps)  