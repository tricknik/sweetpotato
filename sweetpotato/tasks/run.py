from adapter import TaskAdapter

class run(TaskAdapter):
	inheritModule = True
	def run(self):
		self.run.log('run')
