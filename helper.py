#!/usr/bin/python
import sys, os

def main():
	hasnegated = False
	hasword = False
	f = open("temp")
	for line in f:
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
			print("w:" + str(weight) + " " + line),
		else:
			print(line),


if __name__ == '__main__':
	main()