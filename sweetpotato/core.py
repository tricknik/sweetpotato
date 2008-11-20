from collections import deque
import yaml, re

class Task:
	def __init__(self, sweetpotato, parent, type, data):
		self.adapter = None
		self.tasks = deque()
		self.attributes = {}
		self.sweetpotato = sweetpotato
		self.parent = parent
		self.type = str(type)
		self.read("value", data)

	def read(self, attribute, data):
		if hasattr(data,"popitem"):
			self.readDict(data)
		elif hasattr(data,"pop"):
			self.readList(data, attribute)
		else:
			self.setAttribute(attribute, data)

	def setAttribute(self, attribute, value):
		if self.attributes.has_key(attribute):
			if hasattr(self.attributes[attribute],"appendleft"):
				self.attributes[attribute].appendleft(value)
			else:
				value = deque([value, self.attributes[attribute]])
				self.attributes[attribute] = value
		else:
			self.attributes[attribute] = value

	def readDict(self, data):
		while data:
			key, value = data.popitem()
			if hasattr(value, "pop"):
				self.readList([{key:value}])
			else:
				self.setAttribute(key, value)

	def readList(self, data, attribute="value"):
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
				self.setAttribute(attribute, value)

	def addChildTask(self, value, attribute="value"):
		if hasattr(value, "popitem"):	
			itemkey, itemvalue = value.popitem()
			child = Task(self.sweetpotato, self, itemkey, itemvalue)
			self.tasks.appendleft(child)
			if (value):
				raise Exception, "Only 1 key alowed in Task"
		else:
			raise Exception, "Task must be {key: value}"

	def getParent(self):
		parent = self.parent
		if hasattr(parent, "adapter") and \
				hasattr(parent.adapter, "inherit"):
			while parent.adapter and parent.adapter.inherit:
				parent = parent.adapter.task.parent
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

	def getAttribute(self, key):
		if key in self.attributes:
			if hasattr(self.attributes[key],"islower"):
				attribute = self.attributes[key]
				expanded = re.sub(self.sweetpotato.regex, 
					self.expand, attribute)
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
		if hasattr(self.adapter, "run"):
			self.adapter.run()

	def __str__(self):
		task = self
		typePath = deque([self.type])
		while task and task.parent:
			task = task.getParent()
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
		yamlData =  yaml.load(open(file))
		self.buildData = yamlData["sweetpotato"]
		self.targets = {}
		self.startTime = None

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
			print "%s %s\t%s" % (time, str(task).title(), message)

	def run(self,targetName):
		self.log(":: %s" % targetName.upper())
		target = self.getTarget(targetName)
		target.run()
