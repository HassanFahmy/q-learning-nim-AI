from nim import train, play, play2, play3
from collections import Counter, defaultdict


# how much the number of steps we train on affects 
# how many games the agent wins against the optimal
# strategy
def exp1():
	for n_games in [10, 100, 1000, 2500, 5000, 10000, 25000,
					 50000, 75000, 100000]:
		print()
		l = []
		ai = train(n_games)

		for _ in range(20000):
			l.append(play3(ai)[0])
		ctr = Counter(l)
		print("Percentage of games won by PerfectNim:", 100 * ctr['PerfectNim'] / sum(ctr.values()))
		print("Percentage of games won by AI:", 100 * ctr['AI'] / sum(ctr.values()))

# how much the number of steps we train on affects the
# percentage of times AI or perfectNim wins if it's
# predestined to win (it is starting with nim-sum != 0)
# or it is second with the starting nim-sum = 0
def exp2():
	for n_games in [10, 100, 1000, 2500, 5000, 10000, 25000,
					 50000, 75000, 100000]:
		print()
		d = defaultdict(int)
		l = []
		ai = train(n_games)
		for _ in range(20000):
			winner, predestined, a, b, nsteps, perfect_nsteps = play3(ai)
			d["{} predestined".format(predestined)] += 1
			if winner == predestined:
				d["{} winner".format(winner)] += 1
		print("perfectNim won {:0.2f} of its predestined games".format(100 * d["PerfectNim winner"]/d["PerfectNim predestined"]))
		print("AI won {:0.2f} of its predestined games".format(100 * d["AI winner"]/d["AI predestined"]))

def exp3():
	for n_games in [10, 100, 1000, 2500, 5000, 10000, 25000,
					 50000, 75000, 100000]:
		print()
		d = defaultdict(int)
		l = []
		ai = train(n_games)
		a_sum, b_sum = 0, 0
		ca, cb = 0, 0
		for _ in range(20000):
			winner, predestined, a, b, nsteps, perfect_nsteps = play3(ai)
			if a:
				ca += 1
				a_sum += a
			if b:
				cb += 1
				b_sum += b
			
		print("Percentage of time PerfectNim makes the right move", 100 * a_sum/ca)
		print("Percentage of time AI makes the right move", 100 * b_sum/cb)

def exp4():
	for n_games in [10, 100, 1000, 2500, 5000, 10000, 25000,
					 50000, 75000, 100000]:
		print()
		d = defaultdict(int)
		l = []
		ai = train(n_games)
		nsteps_sum, perfect_nsteps_sum = 0, 0
		for _ in range(20000):
			winner, predestined, a, b, nsteps, perfect_nsteps = play3(ai)
			nsteps_sum += nsteps
			perfect_nsteps_sum += perfect_nsteps
			
		print("Average number of actions taken to finish game by optimal algorithm", perfect_nsteps_sum/20000)
		print("Average number of actions taken to finish game by AI", nsteps_sum/20000)

if __name__ == '__main__':
	exp1()
	print('-' * 30)
	#exp2()
	print('-' * 30)
	#exp3()
	print('-' * 30)
	#exp4()