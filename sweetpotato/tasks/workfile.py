""" sweetpotato module for workfile task adapter
"""

from sweetpotato.core import TaskAdapter
import os, logging


class workfile(TaskAdapter):
    """ sweetpotato task adapter for manipulating files
    """

    def runChildTasks(self):
        """ open working file for child tasks
        """
        self.path = self.task.getProperty("path")
        update = True
        self.mode = 'w'
        self.file = None
        if not os.path.exists(os.path.dirname(self.path)):
            os.makedirs(os.path.dirname(self.path))
        elif os.path.exists(self.path):
            if not os.path.isfile(self.path):
                raise Exception, "work file can not be a directory"
            if self.task.getProperty("append"):
                self.mode = 'a'
            else:
                divert =  self.task.getProperty("divert")
                backup =  self.task.getProperty("backup")
                if divert:
                    self.path = '.'.join((self.path, divert))
                    self.task.log("diverting to %s" % self.path, logging.DEBUG)
                elif backup:
                    dst = '.'.join((self.path, backup))
                    while os.path.exists(dst):
                        self.task.log("%s exists!" % dst, logging.WARNING)
                        dst = '.'.join((dst, backup))
                    os.rename(self.path, dst)
                    self.task.log("backup to %s" % dst, logging.DEBUG)
                else:
                    update = False
                    self.task.log("file %s exists" % self.path, logging.DEBUG)
        if update or self.task.getProperty("overwrite"):
            self.task.log("open file %s (%s)" % (self.path, self.mode), logging.DEBUG)
            TaskAdapter.runChildTasks(self)
        else:
            self.task.log("%s: nothing to do" % self.path, logging.INFO)

    def run(self):
        if hasattr(self.file, 'close'):
            self.file.close()

    def getFile(self):
        if not hasattr(self.file, 'write'):
            self.file = open(self.path, self.mode)
        return self.file

    class copy(TaskAdapter):
        """ copy file to working file
        """
        def run(self):
            import shutil
            src = self.task.getProperty("value")
            data = self.task.getProperty("value")
            parent = self.task.getParent("workfile")
            if os.path.exists(src):
                shutil.copyfile(src, parent.adapter.path) 
            else:
                self.task.log("missing: %s" % src, logging.ERROR)
    class write(TaskAdapter):
        """ write data to working file
        """
        def run(self):
            data = self.task.getProperty("value")
            parent = self.task.getParent("workfile")
            file = parent.adapter.getFile()
            file.write(data.encode("UTF-8"))
