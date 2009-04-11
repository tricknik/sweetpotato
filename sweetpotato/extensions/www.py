""" sweetpotato module for xhtml taskadapters
"""
if __name__ == "__main__":
    import sys, os
    sys.path.append(os.path.abspath(os.curdir))

from sweetpotato.core import TaskAdapter
import os, logging, urllib, urlparse
from lxml.html import parse, tostring, Element

class www(TaskAdapter):
    def __init__(self, task):
        self.selectlist = []
        TaskAdapter.__init__(self, task)

    def runChildTasks(self):
        self.url = self.task.getProperty('url')
        self.doc = parse(self.url).getroot() 
        TaskAdapter.runChildTasks(self)

    def run(self):
        sweetpotato = self.task.sweetpotato                
        for select in self.selectlist:
            if select:
                (token, selector) = select.items()[0]
                xml = []
                for element in self.doc.cssselect(selector):
                    for child in element.getchildren():
                        clean = self.clean(child)
                        if clean is not None:
                            clean.rewrite_links(self.rewrite_links)
                            text = tostring(clean,method="xml",encoding=unicode)
                            xml.append(text)
                sweetpotato.setToken(token, u"".join(xml))

    def rewrite_links(self, link):
        parsedUrl = urlparse.urlparse(link)
        if not parsedUrl.netloc:
            #dogey logic, works for moin, improve later
            resource = parsedUrl.path.split('/').pop()
            if '.' not in resource:
                link = '.'.join((resource,'html'))
        return link

    def clean(self, element):
        cleanElement = None
        dropEmpty = ('span', 'p', 'div') 
        downloadDir = self.task.getProperty('download')
        if 'img' == element.tag:
               src = urlparse.urljoin(self.url, element.attrib['src'])
               file, info = urllib.urlretrieve(src)
               url = urlparse.urlparse(src)
               disposition = info.getheader('Content-Disposition')
               filename = None
               if disposition:
                   type, filename = disposition.split(';')
                   key, filename = filename.split('=')
                   filename = filename.strip('"')
               if not filename:
                   filename = os.path.basename(file)
               splitf = filename.split('.')
               lenf = len(splitf)
               ext = splitf.pop()
               if lenf < 2 or info.subtype != ext:
                   filename = '.'.join((filename, info.subtype))
               element.attrib['src']  = filename
               os.rename(file, '/'.join((downloadDir, filename)))
        #moin specific hack for now
        if 'a' == element.tag and '/Category' in element.attrib['href']:
            pass
        elif element.tag not in dropEmpty \
                or bool(element.getchildren()) \
                or (bool(element.text) \
                    and bool(element.text.strip())):
            cleanElement = Element(element.tag)
            cleanElement.text = element.text
            stripattribs = ('class', 'style', 'id')
            for a in element.attrib:
                if a not in stripattribs:
                    cleanElement.set(a, element.attrib[a])  
            for e in element.getchildren():
                clean = (self.clean(e))
                if clean is not None:
                    cleanElement.append(clean)
        return cleanElement        


    class select(TaskAdapter):
        def run(self):
            parent = self.task.getParentWithAttribute('doc')
            selectlist = parent.adapter.selectlist
            properties = self.task.properties
            for select in properties:
                selectlist.append({select: properties[select]})
        
