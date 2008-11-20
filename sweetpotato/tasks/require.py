from adapter import TaskAdapter

class require(TaskAdapter):
	inherit = True
	def run(self):
		target = self.task.getProperty('value')
		self.task.sweetpotato.require(target)
