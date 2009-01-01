""" sweetpotato module for xhtml taskadapters
"""
if __name__ == "__main__":
    import sys, os
    sys.path.append(os.path.abspath(os.curdir))

from sweetpotato.core import TaskAdapter
import os, logging

class htmlElement(TaskAdapter):
    level = 0
    tag = 'html'
    block = True
    blockMode = True
    attributeList = ['id','class'] 
    def runChildTasks(self):
        parent = self.task.getParent('workfile')
        indent = ""
        attributes = ""
        if self.task.properties:
            elementAttributes = []
            for key in self.task.properties.keys():
                if key in self.attributeList:
                    elementAttributes.append("%s=\"%s\"" % \
                        (key, self.task.getProperty(key)))
            if elementAttributes:
                attributes = " " + " ".join(elementAttributes)
        if self.block:
            indent = "\n" + "\t" * htmlElement.level
            htmlElement.level = htmlElement.level + 1
            self.blockMode = True
        elif htmlElement.blockMode:
            indent = "\n" + "\t" * htmlElement.level
            self.blockMode = False
        parent.adapter.file.write("%s<%s%s>" % (indent, self.tag, attributes))
        TaskAdapter.runChildTasks(self)
    def run(self):
        parent = self.task.getParent('workfile') 
        value = self.task.getProperty('value') 
        indent = ""
        if self.block:
            if value:
                value = value + "\n"
            htmlElement.level = htmlElement.level - 1
            indent = "\n" + "\t" * htmlElement.level
        parent.adapter.file.write("%s%s</%s>" % (value, indent, self.tag))
 
class xhtml(htmlElement):
    """ 
    write xhtml to a working file

    >>> import sys, os
    >>> sys.path.append(os.path.abspath(os.curdir))
    >>> from sweetpotato.core import SweetPotato
    >>> data = '''
    ... sweetpotato:
    ...   test:
    ...     - workfile:
    ...        path: test.html 
    ...        overwrite: True
    ...        do:
    ...         - xhtml:
    ...           - head:
    ...             - title: Test Page
    ...           - body:
    ...             - div:
    ...                id: content
    ...                do:
    ...                 - p: Hello World!
    ... '''
    >>> sp = SweetPotato()
    >>> sp.addAdapter(xhtml)
    >>> sp.yaml(data)
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
    pass
    class head(htmlElement):
        tag = "head"
        class title(htmlElement):
            tag = "title"
            block = False 
    class body(htmlElement):
        tag = "body"
        class table(htmlElement):
            tag = "table"
            class tr(htmlElement):
                tag = "tr"
                class td(htmlElement):
                    tag = "td"
        class div(htmlElement):
            tag = "div"
        class p(TaskAdapter):
            tag = "p"
     
def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()

