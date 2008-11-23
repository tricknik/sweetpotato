from adapter import TaskAdapter

class token(TaskAdapter):
	def run(self):
		sweetpotato = self.task.sweetpotato
		properties = self.task.properties
		for property in properties:
			sweetpotato.setToken(property, properties[property])
