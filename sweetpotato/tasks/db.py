from adapter import TaskAdapter

class db(TaskAdapter):
	types = {}
	class read(TaskAdapter):
		def __init__(self, task):
			self.fieldlist = []
			TaskAdapter.__init__(self, task)
		def run(self):
			parent = self.task.getParent()
			type = parent.attributes['type']
			sweetpotato = self.task.sweetpotato				
			for row in db.types[type](self.task):
				self.setProperties(row)
				if 'target' in self.task.attributes:
					target = self.task.attributes['target']
					sweetpotato.run(target)
		def setProperties(self, row):
			sweetpotato = self.task.sweetpotato				
			for field in self.fieldlist:
				if field:
					(name, property) = field.items()[0]
					if name in row:
						sweetpotato.setProperty(property, row[name])
		class fields(TaskAdapter):
			def run(self):
				parent = self.task.getParent()
				fieldlist = parent.adapter.fieldlist
				attributes = self.task.attributes
				for field in attributes:
					fieldlist.append({field: attributes[field]})

def dbSweetpotato(task):
		import yaml
		parent = task.getParent()
		path = parent.attributes['path']
		task.log('from %s' % path)
		data = yaml.load(open(path))
		for row in data[task.attributes['root']]:
			yield row

db.types['sweetpotato'] = dbSweetpotato
