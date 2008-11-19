from adapter import TaskAdapter

class set(TaskAdapter):
	def run(self):
		properties = self.task.sweetpotato.properties
		properties[self.task.attributes.name] = self.task.attributes.value
