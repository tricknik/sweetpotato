from adapter import TaskAdapter

class echo(TaskAdapter):
	def run(self):
		self.task.log(self.task.getProperty('value'))
