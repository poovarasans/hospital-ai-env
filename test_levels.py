from env import HospitalEnv

for mode in ["easy", "medium", "hard"]:
	print("\nTesting mode:", mode )
	
	env = HospitalEnv(mode=mode)
	state = env.reset()
	print("\nInitial State:", state['patients'] )

	done = False
	total = 0

	while not done:
		action = 0
		state, reward, done, _ = env.step(action)
		total += reward

	print("Total Rewards:", state["total_reward"], "Treated:", state["treated"])  