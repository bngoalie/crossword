#!/usr/bin/python
"""
Crossword SAT Decoder
@AUTHORS: Jeremy Dolinko & Ben Glickman
@DESCRIPTION: Takes in the output from the .ans file and
              prints out the item
"""
import sys, os

class Globs:
	cross = []
	m_row = 0
	m_col = 0

def workout_encoding(answerfile):
	Globs.cross = [[] for i in range(Globs.m_row * Globs.m_col)]
	if os.stat(answerfile)[6] == 0:
		print "UNSAT"
		sys.exit(0)
	f = open(answerfile)
	for word in f:
		if not ("-" in word):
			# words in x_num_num -> [x,num,num]
			lst = word.split()
			for item in lst:
				item = item.split("_")
				row = int(item[1])
				col = int(item[2])
				if len(Globs.cross[(row * Globs.m_row) + col]) != 0:
					print "TWO ITEMS IN SAME SPOT?"
				Globs.cross[(Globs.m_row * row) + col].append(item[0])
	f.close()
	for i in range (Globs.m_row * Globs.m_col):
			if (i % Globs.m_col == Globs.m_col-1):
				print(Globs.cross[i][0] + "\n"),
			else:
				print(Globs.cross[i][0]),

def get_args():
	if len(sys.argv) != 3:
		sys.stderr.write("Incorrect number of args")
		sys.exit(1)
	else:
		puzzle = str(sys.argv[1])
		answer = str(sys.argv[2])
		return [puzzle, answer]

def main():
	my_args = get_args()
	
	p = open(my_args[0])
	firstline = p.readline().split()
	Globs.m_row = int(firstline[0])
	Globs.m_col = int(firstline[1])
	p.close()

	workout_encoding(my_args[1])

if __name__ == '__main__':
	main()
