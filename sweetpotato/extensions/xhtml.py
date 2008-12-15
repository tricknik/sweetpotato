""" sweetpotato module for xhtml taskadapters
"""

from sweetpotato.core import TaskAdapter
import os, logging

class xhtml(TaskAdapter):
    """ write data to working file
    """
    def runChildTasks(self):
        self.task.log('opening html', logging.INFO)
        parent = self.task.getParent('workfile')
        parent.adapter.file.write("<html>\n")
        TaskAdapter.runChildTasks(self)
    def run(self):
        self.log.log('closing html', logging.INFO)
        parent = self.task.getParent('workfile')
        parent.adapter.file.write("\n</html>\n")
