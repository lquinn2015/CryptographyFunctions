import time
import numpy as np


class mersenne_rng(object):
	def __init__(self, seed=5489):

		self.MT = [0] * 624
		self.lower_mask = (1 << 31) - 1
		self.upper_mask = 1<<31 
		self.index = 624
		self.f = 0x6c078965
		self.m = 397
		self.u = 11
		self.s = 7
		self.b = 0x9d2c5680
		self.t = 15
		self.c = 0xefc60000
		self.l = 18
		self.lower_mask = (1 << 31) - 1
		self.upper_mask = (1 << 31)
		

		self.MT[0] = seed
		for i in range(1,624):
			self.MT[i] = self.int_32(self.f*(self.MT[i-1]^(self.MT[i-1]>>30)) + i)
	

	def temper(self,y):
		y = y^(y >> self.u)
		y = y^((y << self.s) & self.b)
		y = y^((y << self.t) & self.c)
		y = y^(y >> self.l)
		return y	

	def pick_num(self):
		if self.index >= 624:
			self.twist()
		y = self.MT[self.index]	
		y = self.temper(y)
		self.index += 1
		return self.int_32(y)

	def twist(self):
		for i in range(624):

			y = self.int_32((self.MT[i] & self.upper_mask) + (self.MT[(i+1) % 624] & self.lower_mask))
			ys = y >> 1
			if y % 2 != 0:
				ys ^= 0x9908b0df
			self.MT[i] = self.MT[(i + self.m) % 624] ^ ys
		self.index = 0
	
	def int_32(self, number):
		return int(0xFFFFFFFF & number)


def reverseTwist(rng, MT):
	
	for i in reversed(range(624)):
		result = 0
		tmp = MT[i]
		tmp ^= MT[(i + 397) % 624]
		if( (tmp & 0x80000000) == 0x80000000 ):
			tmp ^= 0x9908b0df
		
		result = (tmp << 1) & 0x80000000

		tmp = MT[(i - 1 + 624) % 624]
		tmp ^= MT[(i + 396) % 624]
		if((tmp & 0x80000000) == 0x80000000):
			tmp ^= 0x9908b0df
			result |= 1

		result |= (tmp << 1) & 0x7fffffff
		MT[i] = result
	return MT

# the assumption is using default tempering variables but we cannot access the interal state for obvious reasons
def untemperArray(rng, arr):
	ret = []
	for num in arr:	
		x = num
		x1 = x ^ (x >> rng.l)
		x2 = x1 ^ (x1 << rng.t) & rng.c
		SMask = (1<<rng.s) - 1
		
		x3 = x2
		for i in range(1,5):
			x3 = x3 ^ (x3 << rng.s) & rng.b & (SMask << (rng.s* i))
		
		UMask = (1 << rng.u) - 1
		x = x3
		for i in reversed(range(3)):
			x = x^(x >> rng.u) & (UMask << (rng.u*i))
	
		ret.append(x)
	return ret

def guess_seed():
	
	t1 = int(time.time() + np.random.randint(40,1000))
	t2 = int(t1 + np.random.randint(40,1000))

	rng = mersenne_rng(t1)

	n = rng.pick_num()

	seed = t2
	guess = mersenne_rng(seed).pick_num()

	while guess != n:
		seed -= 1
		guess = mersenne_rng(seed).pick_num()
	
	assert(seed == t1)
	print("Seed was " + str(seed) )
		
		


def rng_backwards():
	rng = mersenne_rng(5)

	pre_twist = [rng.MT[i] for i in range(624)]
	arr = [rng.pick_num() for x in range(624)]
	pre_temper = [rng.MT[i] for i in range(624)]
	post_twist = untemperArray(rng, arr)
	

	for x,y in zip(pre_temper, post_twist):
		assert(x==y)

	# after untempering we need to reverse the first twist
	prev = reverseTwist(rng, post_twist)

	MTN = [prev[i] for i in range(624)]
	rng2 = mersenne_rng()
	rng2.MT = MTN
	arr2 = [rng2.pick_num() for x in range(624)]
	print(arr == arr2) # this is more than a clone its a step backward

	# this works except when we are getting the seed value because that does not about the recurence relation aka we know when we hit the seed!!

	pre_twists = []
	arrs = []
	seed = np.random.randint(1000)
	rng = mersenne_rng(seed) # make guessing easier

	for x in range(50):
		pre_twists.append([rng.MT[i] for i in range(624)])
		arrs.append([rng.pick_num() for i in range(624)]) 

	i = 49
	for pre,arr in zip(reversed(pre_twists), reversed(arrs)):
		post = untemperArray(rng, arr)
		prev = reverseTwist(rng, post)
		if pre[0] != prev[0]:
			assert(i==0)
		else:
			assert(pre == prev)
		i -= 1

	arr = arrs[0]
	correct_threshold = 600
	cout = 0
	seed_guess = -1
	for i in range(1000):
		rng = mersenne_rng(i)
		for	x in range(correct_threshold+1):
			if rng.pick_num() == arr[x]:
				cout += 1
			else:
				cout = 0
		if cout > correct_threshold:
			print("The Seed is probably " + str(i))
			seed_guess = i 
			break

	assert seed_guess == seed

def main():
	#guess_seed()
	rng_backwards()

main()
