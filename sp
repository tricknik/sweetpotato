#!/usr/bin/python
import sys
sys.path.append('/dk/work/sweetpotato')
from sweetpotato.core import Task, Target, SweetPotato

if 3 > len(sys.argv):
	fileName = 'build.yaml'
else:
	fileName = sys.argv.pop()
if 2 > len(sys.argv):
	targetName = 'build'
else:
	fileName = sys.argv.pop()

sweetpotato = SweetPotato(fileName)
sweetpotato.run(targetName)

