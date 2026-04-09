from env import HospitalEnv
 
def grade():
	env = HospitalEnv()
	state = env.reset()

	total_reward = 0
	steps = 0

	done = False

	while not done and step < 10:
		#simple agent logic
		action = 0

		state, reward, done, _ = env.step(action)
		total_reward += reward
		steps += 1

	# scoring logic
	max_possible = 10
	score = total_reward / max_possible

	# normalize (0 to 1)
	score = max(0, min(1, score))

	return score

if __name__ == "__main__":
	print("Score:", grade())