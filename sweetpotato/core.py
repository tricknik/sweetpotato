from collections import deque
import yaml, re

class Task:
	def __init__(self, sweetpotato, parent, type, data):
		self.adapter = None
		self.tasks = deque()
		self.properties = {}
		self.sweetpotato = sweetpotato
		self.parent = parent
		self.type = str(type)
		self.read("value", data)

	def read(self, property, data):
		if hasattr(data,"popitem"):
			self.readDict(data)
		elif hasattr(data,"pop"):
			self.readList(data, property)
		else:
			self.setProperty(property, data)

	def setProperty(self, property, value):
		if self.properties.has_key(property):
			if hasattr(self.properties[property],"appendleft"):
				self.properties[property].append(value)
			else:
				value = deque((self.properties[property], value))
				self.properties[property] = value
		else:
			self.properties[property] = value

	def readDict(self, data):
		while data:
			key, value = data.popitem()
			if hasattr(value, "pop"):
				self.readList([{key:value}])
			else:
				self.setProperty(key, value)

	def readList(self, data, property="value"):
		while data:
			value = data.pop()
			if hasattr(value, "popitem"):	
				itemkey, itemdata = value.items()[0]
				if hasattr(itemdata, 'append') \
						and not hasattr(itemdata[0], 'pop'):
					self.readList(itemdata, itemkey)
				else:
					self.addChildTask(value)
			else:
				self.setProperty(property, value)

	def addChildTask(self, value, property="value"):
		if hasattr(value, "popitem"):	
			itemkey, itemvalue = value.popitem()
			child = Task(self.sweetpotato, self, itemkey, itemvalue)
			self.tasks.appendleft(child)
			if (value):
				raise Exception, "Only 1 key alowed in Task"
		else:
			raise Exception, "Task must be {key: value}"

	def getParent(self, parentType):
		parent = self.parent
		while parentType != parent.type:
			parent = parent.parent
		return parent

	def loadAdapter(self):
		module = None
		parent = self.parent
		while parent:
			if hasattr(parent.adapter, self.type):
				module = parent.adapter
			parent = parent.parent
		if not module:
			module = self.importModule(self.type)
		self.adapter = getattr(module, self.type)(self)

	def importModule(self, type):
		from copy import copy
		fromList = ["sweetpotato","tasks"]
		nameList = copy(fromList)
		nameList.append(type)
		taskModule = ".".join(nameList)
		return __import__(taskModule, fromlist=fromList)

	def log(self, message):
		self.sweetpotato.log(message, self)

	def expand(self, value):
		key = value.groups()[0].strip().lower()
		if key in self.sweetpotato.tokens:
			token = self.sweetpotato.tokens[key]	
		else:
			token = None
		return str(token)

	def expandValue(self, value):
		expanded = value
		if hasattr(value,'islower'):
			expanded = re.sub(self.sweetpotato.regex, self.expand, value)
		return expanded

	def getProperty(self, key):
		if key in self.properties:
			if hasattr(self.properties[key],"islower"):
				property = self.properties[key]
				expanded = self.expandValue(property)
			elif hasattr(self.properties[key],"append"):
				expanded = deque()
				for item in  self.properties[key]:
					expandedItem = self.expandValue(item)
					if expandedItem:
						expanded.appendleft(expandedItem)
			else:
				expanded = self.properties[key]
		else:
			expanded = ''
		return expanded

	def run(self):
		if self.parent:
			self.loadAdapter()
		for task in self.tasks:
			task.run()
		if hasattr(self.adapter, "run"):
			self.adapter.run()

	def __str__(self):
		task = self
		typePath = deque([self.type])
		while task and task.parent:
			task = task.parent
			if task.adapter:
				typePath.appendleft(task.type)
			task = task.parent
		strType = ".".join(typePath)
		return strType

class SweetPotato:
	regex = re.compile("\{\{([^}]+)\}\}")

	def __init__(self, options):
		self.options = options
		self.tokens = {}
		if hasattr(self.options, "tokens") and \
				self.options.tokens:
			for token in self.options.tokens:
				(key, value) = token.split("=")
				self.setToken(key, value.strip())
			del self.options.tokens
		file = options.file
		self.load(file)
		self.targets = {}
		self.startTime = None

	def load(self, buildfile):
		yamlData =  yaml.load(open(buildfile))
		self.buildData = yamlData["sweetpotato"]

	def setToken(self, key, value):
		self.tokens[key.strip().lower()] = value

	def getTarget(self, target):
		if not self.targets.has_key(target):
			self.targets[target] = \
				Task(self, None, "target", self.buildData[target])
			del self.buildData[target]
		return self.targets[target]

	def log(self, message, task=None):
		from datetime import datetime
		now = datetime.now()
		if not self.startTime:
			self.startTime = now
		time = str(now.time())
		if not task:
			print "%s %s" % (time, message)
		else:
			print "%s    %s\t%s" % (time, str(task).title(), message)

	def require(self, targetName):
		if not targetName in self.targets:
			target = self.getTarget(targetName)
			self.log(":: %s" % targetName.upper())
			target.run()
			self.log(" ^")

	def run(self,targetName):
		self.log("~{ %s " % targetName.upper())
		target = self.getTarget(targetName)
		target.run()
		self.log("--")
