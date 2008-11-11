import yaml

class Task:
	target = None
	type = None
	value = None
	def __init__(self, target, task, data):
		self.target = target
		self.type = task
		self.read(data)
	def read(self, data):
		if hasattr(data,'keys'):
			for attr in data.keys():
				setattr(self,attr,data[attr])
		elif hasattr(data,'append'):
			pass
		else:
			self.value = data
	def run(self):
		print self.type, 'has nothing to do.'

class Target:
	sweetpotato = None
	name = None
	tasks = []
	def __init__(self, sweetpotato, target, targetData):
		self.sweetpotato = sweetpotato
		self.name = target
		for taskDict in targetData:
			taskItem = taskDict.popitem();
			taskType = taskItem[0]
			taskData = taskItem[1]
			task = taskLoader(self, taskType, taskData)
			self.tasks.append(task)
	def run(self):
		for task in self.tasks:
			task.run()

class SweetPotato:
	buildData = None
	targets = {}
	def __init__(self,file):
		yamlData =  yaml.load(open(file))
		self.buildData = yamlData['sweetpotato']
	def run(self,target):
		if not self.targets.has_key(target):
			self.targets[target] = Target(self, target, self.buildData[target])
			del self.buildData[target]
		self.targets[target].run()

class Echo(Task):
	def run(self):
		print self.value

class Db(Task):
	def run(self):
		print self.path

def taskLoader(self, taskType, taskData):
	if 'echo' == taskType:
		task = Echo(self, taskType, taskData)
	if 'db' == taskType:
		task = Db(self, taskType, taskData)
	else:
		task = Task(self, taskType, taskData)
	return task
