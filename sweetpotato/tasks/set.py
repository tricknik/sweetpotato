""" set a task property
"""
from adapter import TaskAdapter

class set(TaskAdapter):
    """ set a task property
    """
	def run(self):
		name = self.task.getProperty('name')
		value = self.task.getProperty('value')
		self.task.setProperty(name, value)
