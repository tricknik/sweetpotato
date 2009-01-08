""" database interface module
"""
from sweetpotato.core import TaskAdapter

class db(TaskAdapter):
    """ database interface module
        defines a connection to a data source  
    """

    types = {}
    class read(TaskAdapter):
        def __init__(self, task):
            self.fieldlist = []
            TaskAdapter.__init__(self, task)

        def run(self):
            parent = self.task.getParent("db")
            type = parent.properties["type"]
            sweetpotato = self.task.sweetpotato                
            for row in db.types[type](self.task):
                self.setTokens(row)
                if "target" in self.task.properties:
                    target = self.task.properties["target"]
                    sweetpotato.run(target)

        def setTokens(self, row):
            sweetpotato = self.task.sweetpotato                
            for field in self.fieldlist:
                if field:
                    (name, token) = field.items()[0]
                    if name in row:
                        sweetpotato.setToken(token, row[name])

        class fields(TaskAdapter):
            def run(self):
                parent = self.task.getParent("read")
                fieldlist = parent.adapter.fieldlist
                properties = self.task.properties
                for field in properties:
                    fieldlist.append({field: properties[field]})

def dbSweetpotato(task):
        import yaml
        parent = task.getParent("db")
        path = parent.getProperty("path")
        task.log("reading from %s" % path)
        data = yaml.load(open(path))
        for row in data[task.properties["root"]]:
            yield row

def dbMoinCategory(task):
        from lxml.html import parse
        from urlparse import urlsplit
        parent = task.getParent("db")
        url = parent.getProperty("url")
        moin_url = '://'.join(urlsplit(url)[0:2])
        task.log("reading from %s" % moin_url)
        doc = parse(url).getroot()
        for link in doc.cssselect('#content ol li a'):
            page = link.attrib['href'].split('?')[0]
            name = page.split('/').pop()
            title = link.text_content();
            row = {'url': '%s%s' % (moin_url, page),
                   'name': name,
                   'title': title}
            yield row


db.types["sweetpotato"] = dbSweetpotato
db.types["moincategory"] = dbMoinCategory

