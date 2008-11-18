import yaml, re

class Task:
	def __init__(self, sweetpotato, parent, type, data):
		self.tasks = []
		self.attributes = {}
		self.sweetpotato = sweetpotato
		self.type = None
		self.parent = parent
		self.adapter = None
		self.type = type
		self.read('value', data)
		self.tasks.reverse()
	def read(self, attribute, data):
		if hasattr(data,'popitem'):
			self.setAttributes(data)
		elif hasattr(data,'pop'):
			self.addChildTasks(data)
		else:
			if self.attributes.has_key(attribute):
				raise Exception, str(self) + ': Duplicate Attribute'
			else:
				self.attributes[attribute] = data

	def setAttributes(self, data):
		while data:
			key, value = data.popitem()
			if hasattr(value, 'pop'):
				self.addChildTasks([{key:value}])

	def addChildTasks(self, data):
		while data:
			value = data.pop()
			if hasattr(value, 'popitem'):	
				itemkey, itemvalue = value.popitem()
				child = Task(self.sweetpotato, self, itemkey, itemvalue)
				self.tasks.append(child)
				if (value):
					raise Exception, 'Only 1 key alowed in Task'
			else:
				raise Exception, "Task must be {'key': value}"

	def loadAdapter(self):
		adapter = self.parent.adapter
		if hasattr(adapter, 'inheritModule'):
			while adapter.inheritModule:
				adapter = adapter.task.parent.adapter
				print 'inheriting module', adapter
		if hasattr(adapter, self.type):
			module = adapter
		else:
			module = self.importModule(self.type)
		self.adapter = getattr(module, self.type)(self)
	def importModule(self, type):
		from copy import copy
		fromList = ['sweetpotato','tasks']
		nameList = copy(fromList)
		nameList.append(type)
		taskModule = '.'.join(nameList)
		return __import__(taskModule, fromlist=fromList)
	def log(self, message):
		self.sweetpotato.log(message, self)
	def expand(self, value):
		key = value.groups()[0].strip().lower()
		if self.sweetpotato.properties and \
				key in self.sweetpotato.properties:
			property = self.sweetpotato.properties[key]	
		else:
			property = None
		return str(property)
	def getAttribute(self, key):
		if key in self.attributes:
			if hasattr(self.attributes[key],'islower'):
				attribute = self.attributes[key]
				expanded = re.sub(self.sweetpotato.regex, self.expand, attribute)
			else:
				expanded = self.attributes[key]
		else:
			expanded = None
		return expanded
	def run(self):
		if self.parent:
			self.loadAdapter()
		for task in self.tasks:
			task.run()
		if hasattr(self.adapter, 'run'):
			self.adapter.run()
	def __str__(self):
		task = self
		typePath = [self.type]
		while task.parent:
			if task.parent.adapter:
				typePath.append(task.parent.type)
			task = task.parent
		typePath.reverse()
		strType = '.'.join(typePath)
		return strType

class SweetPotato:
	regex = re.compile('\{\{([^}]+)\}\}')
	def __init__(self, options):
		self.options = options
		self.properties = {}
		if hasattr(self.options, 'properties') and \
				self.options.properties:
			for property in self.options.properties:
				(key, value) = property.split("=")
				self.setProperty(key, value.strip())
			del self.options.properties
		file = options.file
		yamlData =  yaml.load(open(file))
		self.buildData = yamlData['sweetpotato']
		self.targets = {}
		self.startTime = None
	def setProperty(self, key, value):
		self.properties[key.strip().lower()] = value
	def getTarget(self, target):
		if not self.targets.has_key(target):
			self.targets[target] = \
				Task(self, None, 'target', self.buildData[target])
			del self.buildData[target]
		return self.targets[target]
	def log(self, message, task=None):
		from datetime import datetime
		now = datetime.now()
		if not self.startTime:
			self.startTime = now
		time = str(now.time())
		if not task:
			print '%s %s' % (time, message)
		else:
			print '%s %s\t%s' % (time, str(task).title(), message)
	def run(self,targetName):
		self.log(':: %s' % targetName.upper())
		target = self.getTarget(targetName)
		target.run()
		self.log('\n')
