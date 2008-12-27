""" sweetpotato module for xhtml taskadapters
"""
m
if __name__ == "__main__":
    import sys, os
    sys.path.append(os.path.abspath(os.curdir))

from sweetpotato.core import TaskAdapter
import os, logging
class htmlElement(TaskAdapter):
    tag = 'html'
    def runChildTasks(self):
        parent = self.task.getParent('workfile')
        parent.adapter.file.write("<%s>\n" % self.tag)
        TaskAdapter.runChildTasks(self)
    def run(self):
        parent = self.task.getParent('workfile')
        parent.adapter.file.write("\n</%s>\n" % self.tag)
 
class xhtml(TaskAdapter):
    """ 
    write xhtml to a working file

    >>> import sys, os
    >>> sys.path.append(os.path.abspath(os.curdir))
    >>> from sweetpotato.core import SweetPotato
    >>> data = {'sweetpotato':
    ...     {'test':
    ...         [{'workfile': 
    ...             {'path':'test.html',
    ...                 'do': [
    ... {'xhtml':[
    ...     {'head': [{'title':'xhtml writer'}]},
    ...     {'div': [{'p':'xhtml writer'}]}
    ... ]}]}}]}}
    >>> sp = SweetPotato()
    >>> sp.addAdapter(xhtml)
    >>> sp.load(data)
    >>> sp.run('test')
    >>> f = open('test.html').read()
    >>> f.find('<html>') >= 0
    True
    >>> f.find('<head>') >= 0
    True
    >>> f.find('</head>') > 0
    True
    >>> f.find('</html>') > 0
    True
    >>> #os.remove('test.html')
    """

    def runChildTasks(self):
        parent = self.task.getParent('workfile')
        parent.adapter.file.write("<html>\n")
        TaskAdapter.runChildTasks(self)
    def run(self):
        parent = self.task.getParent('workfile')
        parent.adapter.file.write("\n</html>\n")
    class head(TaskAdapter):
        def runChildTasks(self):
            parent = self.task.getParent('workfile')
            parent.adapter.file.write("\n\t<head>\n")
            TaskAdapter.runChildTasks(self)
        def run(self):
            parent = self.task.getParent('workfile')
            parent.adapter.file.write("\n\t</head>\n")
        class title(TaskAdapter):
            def run(self):
                parent = self.task.getParent('workfile')
                value = self.task.getProperty('value') 
                parent.adapter.file.write("<title>%s</title>" % value)
    class div(TaskAdapter):
        def runChildTasks(self):
            parent = self.task.getParent('workfile')
            parent.adapter.file.write("\n<div>\n")
            TaskAdapter.runChildTasks(self)
        def run(self):
            parent = self.task.getParent('workfile')
            parent.adapter.file.write("\n</div>\n")
    class p(TaskAdapter):
        def run(self):
            parent = self.task.getParent('workfile')
            value = self.task.getProperty('value') 
            parent.adapter.file.write("<p>%s</p>" % value)
 
def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()

