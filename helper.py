#!/usr/bin/python
import sys, os

def main():
	f = open("temp")
	for line in f:
		hasword = False
		weight = 1
		tempwords = line.split()
		literals = [i for i in tempwords if (i != "v" and i != "&")]
		if (literals[0][0:2] == "~#" and literals[-1][0] != "~"):
			# add weight
			for lit in literals:
				if (lit[0] != "#" and lit[1] != "#" and lit[0] == "~"):
					weight += 1
			weight = (2 * weight) + 1
		if weight > 1:
			print ("w:" + str(weight) + " " + literals[0]),
			for lit in literals:
				if lit[0] == "#":
					hasword = True
				elif lit[0:2] != "~#":
					print(" v " + lit),
			print(" &\n"),
			if hasword:
	                      if literals[1][0] != "~":
	                              print ("w:1 " +literals[0]),
	                      else:
	                              print (literals[0]),
	                      for lit in literals:
	                              if lit[0:2] != "~#" and (lit[0] == "~" or lit[0] == "#"):
	                                      print(" v " + lit),
	                      print(" &\n"),
		else:
			print(line),


if __name__ == '__main__':
	main()
