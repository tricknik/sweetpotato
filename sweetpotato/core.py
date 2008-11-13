import yaml

class Task:
	def __init__(self, parent, task, data):
		self.tasks = []
		self.attributes={}
		self.type = None
		self.parent = parent
		self.adapter = None
		self.type = task
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
			if hasattr(value, 'popitem'):
				self.addChildTasks([{key:value}])
			else:
				self.read(key, value)

	def addChildTasks(self, data):
		while data:
			value = data.pop()
			if hasattr(value, 'popitem'):	
				itemkey, itemvalue = value.popitem()
				child = Task(self, itemkey, itemvalue)
				self.tasks.append(child)
				if (value):
					raise Exception, 'Only 1 key alowed in Task'
			else:
				raise Exception, "Task must be {'key': value}"

	def initAdapter(self):
		if hasattr(self.parent.adapter,self.type):
			self.adapter = getattr(self.parent.adapter,self.type)(self)
		else:
			module = self.importAdapter(self.parent.type)
			if hasattr(module,'__dict__') and module.__dict__.has_key(self.type):
				self.adapter = module.__dict__[self.type](self)
			else:
				self.adapter = self.importAdapter(self.type)
				self.adapter.__init__(self)
		
	def importAdapter(self, type):
		from copy import copy
		fromList = ['sweetpotato','tasks']
		nameList = copy(fromList)
		nameList.append(type)
		adapter = '.'.join(nameList)
		return __import__(adapter, fromlist=fromList)

	def run(self):
		print '::', self
		if self.parent:
			self.initAdapter()
		for task in self.tasks:
			if task.parent is self:
				task.run()
			else:
				raise Exception, '%s does not belong to %s' % (task, self)

	def __str__(self):
		t = self
		s = [self.type]
		while t.parent:
			s.append(t.parent.type)
			t = t.parent
		s.reverse()
		p = '.'.join(s)
		return p

class SweetPotato:
	buildData = None
	targets = {}
	def __init__(self,file):
		yamlData =  yaml.load(open(file))
		self.buildData = yamlData['sweetpotato']
	def getTarget(self, target):
		if not self.targets.has_key(target):
			self.targets[target] = Task(None, 'target', self.buildData[target])
			del self.buildData[target]
		return self.targets[target]
	def run(self,targetName):
		target = self.getTarget(targetName)
		target.run()

