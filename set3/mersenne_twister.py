

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
	
	def pick_num(self):
		if self.index >= 624:
			self.twist()
		y = self.MT[self.index]	
		y = y^(y >> self.u)
		y = y^((y << self.s) & self.b)
		y = y^((y << self.t) & self.c)
		y = y^(y >> self.l)
		
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
		
def main():
	rng = mersenne_rng(1234)
	

main()
