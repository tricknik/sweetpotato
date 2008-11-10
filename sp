#!/usr/bin/python
import sys
from sweetpotato.core import SweetPotato

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

