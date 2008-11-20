from adapter import TaskAdapter

class token(TaskAdapter):
	def run(self):
		name = self.task.getProperty('name')
		value = self.task.getProperty('value')
		sweetpotato = self.task.sweetpotato
		sweetpotato.setToken(name, value)
