from adapter import TaskAdapter

class db(TaskAdapter):
	types = {}

	class read(TaskAdapter):
		def __init__(self, task):
			self.fieldlist = []
			TaskAdapter.__init__(self, task)

		def run(self):
			parent = self.task.getParent()
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
				parent = self.task.getParent()
				fieldlist = parent.adapter.fieldlist
				properties = self.task.properties
				for field in properties:
					fieldlist.append({field: properties[field]})

def dbSweetpotato(task):
		import yaml
		parent = task.getParent()
		path = parent.properties["path"]
		task.log("from %s" % path)
		data = yaml.load(open(path))
		for row in data[task.properties["root"]]:
			yield row

db.types["sweetpotato"] = dbSweetpotato
