class TaskAdapter:
	def __init__(self, task):
		self.task = task
	def runChildTasks(self):
		for task in self.task.tasks:
			task.run()
		if hasattr(self, "run"):
			self.run()
