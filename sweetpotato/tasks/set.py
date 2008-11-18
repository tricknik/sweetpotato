from adapter import TaskAdapter

class set(TaskAdapter):
	def run(self):
		self.task.sweetpotato.properties[self.task.attributes.name] = self.task.attributes.value
