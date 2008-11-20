from adapter import TaskAdapter

class set(TaskAdapter):
	def run(self):
		name = self.task.getProperty('name')
		value = self.task.getProperty('value')
		self.task.setProperty(name, value)
