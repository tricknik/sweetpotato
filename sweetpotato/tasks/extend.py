""" load task adapter extension
"""
from adapter import TaskAdapter

class extend(TaskAdapter):
    """ load task adapter extension
    """
    def run(self):
        name = self.task.getProperty('name')
        fromList = self.task.getProperty('from')
        self.task.sweetpotato.loadExtension(name, fromList)
