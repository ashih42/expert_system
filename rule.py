class Rule:

	def __init__(self, lhs, rhs):
		self.lhs = lhs
		self.rhs = rhs

	def __str__(self):
		return self.lhs + ' => ' + ' + '.join(self.rhs)

