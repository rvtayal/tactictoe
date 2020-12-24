class Test(object):
	def __init__(self):
		print("init 1")
		self.var = 5

	def a(self):
		pass

	def b(self):
		self.a()
		print(self.var)

class Test2(Test):
	def __init__(self):
		super(Test2, self).__init__()
		print("init 2")

	def a(self):
		print("blah")

if __name__ == "__main__":
	t = Test2()
	t.b()
