#!/usr/bin/python
def main():
	from optparse import OptionParser
	import sys
	sys.path.append("/dk/work/sweetpotato")
	from sweetpotato.core import Task, SweetPotato

	usage = "%prog [options] target"
	parser = OptionParser(usage=usage, version="sweetpotato 0.0.1")
	parser.add_option("-l","--list", action="store_true", help="list targets")
	parser.add_option("-L","--list-all", action="store_true", help="list all targets")
	parser.add_option("-f","--file",default="build.yaml", help="build file [default: %default]")
	parser.add_option("-S",dest="properties", metavar="PROPERT=VALUE", action="append", help="set build property")

	(options, args) = parser.parse_args()
	if 1 > len(args):
		parser.error("target missing")

	sweetpotato = SweetPotato(options)
	for target in args:
		sweetpotato.run(target)
		sweetpotato.log('BUILD FINISHED\n')
if "__main__" ==  __name__:
	main()
