from sweetpotato.core import Task, Target, SweetPotato

class Echo(Task):
	def run(self):
		print self.value

