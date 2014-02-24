"""
Crossword SAT Encoder
@AUTHORS: Jeremy Dolinko & Ben Glickman
@DESCRIPTION: Takes a .puzzle file describing a Crossword
              and returns the CNF encoding that can be used by
              zchaff.
"""

import sys
from sets import Set

class Glob:
	cross = [] #stores crossword elements at [r][c]
	hashmtrx = [] # stores list of possible values at [r][c]
	trie_dict = {} # dictionary
	m_row = 0 # grid row size
	m_col = 0 # grid col size

def print_set_variables():
	for r in range(Glob.m_row):
		for c in range(Glob.m_col):
			if Glob.cross[(r * Glob.m_row) + c] != ".":
				if (r == Glob.m_row -1 and c == Glob.m_row -1):
					print(Glob.cross[(r * Glob.m_row) + c] + str(r) + "_" + str(c)),
				else:
					print(Glob.cross[(r * Glob.m_row) + c] + str(r) + "_" + str(c) + " &\n"),

# helper for outer loops
def inner_loop(key, row, col, direction):
	lst = Glob.trie_dict.get(key)
	if len(lst) != 0:
		if key[0] != "":
			for i in range(len(key[0])):
				if i == (len(key[0]) - 1):
					if direction == "H":
						print("~" + key[0][i] + str(row) + "_" + str(col - len(key[0]) + i + 1)),
					else:
						print("~" + key[0][i] + str(row - len(key[0]) + i + 1) + "_" + str(col)),
				else:
					if direction == "H":
						print("~" + key[0][i] + str(row) + "_" + str(col - len(key[0]) + i + 1) + " v "),
					else:
						print("~" + key[0][i] + str(row - len(key[0]) + i + 1) + "_" + str(col) + " v "),
		for letter in lst:
			if direction == "H":
				print(" v " + letter + str(row) + "_" + str(col + 1)),
			else:
				print(" v " + letter + str(row + 1) + "_" + str(col)),
		print(" &\n"),
		for letter in lst:
			if direction == "H":
				inner_loop((key[0] + letter, key[1]), row, col + 1, direction)
			else:
				inner_loop((key[0] + letter, key[1]), row + 1, col, direction)
	if key[0] != "":
		if not (key[0][-1] in Glob.hashmtrx[(row * Glob.m_row) + col]):
			Glob.hashmtrx[(row * Glob.m_row) + col].append(key[0][-1])

def horiz_outer_loop():
	for r in range(Glob.m_row):
		counter = 0
		for c in range(Glob.m_col):
			if Glob.cross[(r * Glob.m_row) + c] != "#":
				counter = counter + 1
			elif counter > 0:
				print("~#" + str(r) + "_" + str(c - counter - 1)),
				inner_loop(("", counter), r, (c - counter - 1), "H")
			else:
				counter = 0

def vert_outer_loop():
	for c in range(Glob.m_col):
		counter = 0
		for r in range(Glob.m_row):
			if Glob.cross[(r * Glob.m_row) + c] != "#":
				counter = counter + 1
			elif counter > 0:
				print("~#" + str(r - counter - 1) + "_" + str(c)),
				inner_loop(("", counter), (r - counter - 1), c, "V")
			else:
				counter = 0

def one_per_block():
	for r in range(Glob.m_row):
		for c in range (Glob.m_col):
			for i in range( len(Glob.hashmtrx[(r * Glob.m_row) + c]) - 1 ):
				for j in range (i + 1, len(Glob.hashmtrx[(r * Glob.m_row) + c])):
					print("~" + Glob.hashmtrx[(r * Glob.m_row) + c][i] + str(r) + "_" + str(c) + " v ~" + Glob.hashmtrx[(r * Glob.m_row) + c][j] + str(r) + "_" + str(c) + " &\n"),
			for item in Glob.hashmtrx[(r * Glob.m_row) + c]:
				if item == Glob.hashmtrx[(r * Glob.m_row) + c][len(Glob.hashmtrx[(r * Glob.m_row) + c]) -1]:
					print(item + str(r) + "_" + str(c) + " &\n"),
				else:
					print(item + str(r) + "_" + str(c) + " v "),

# helper method for making our "trie"
def tries(prefix, length, rest):
	# if the key is in the dict, union the first letter of the rest in
	if (prefix,length) in Glob.trie_dict:
		Glob.trie_dict[(prefix, length)] = Glob.trie_dict[(prefix, length)] | Set([rest[0]])
	# if there's still stuff left and is not already in, put it in
	elif len(rest) > 0:
		Glob.trie_dict[(prefix, length)] = Set([rest[0]])
	# if it's done, put in the empty set
	else:
		Glob.trie_dict[(prefix, length)] = Set([])
	# if the rest isn't empty try it with the next letter
	if rest != "":
		newprx = "" + prefix + rest[0]
		tries(prefix + rest[0], length, rest[1:])

def make_trie(wordlist):
	f = open(wordlist)
	for word in f:
		word = word.strip()
		tries("", len(word), word)
	f.close()

def make_crossmtrx(puzzle):
	f = open(puzzle)
	items = f.readline().split()
	Glob.m_row = int(items[0])
	Glob.m_col = int(items[1])
	for line in f:
		line = line.strip()
		for char in line:
			Glob.cross.append(char)
	Glob.hashmtrx = [ [] for i in range(Glob.m_row * Glob.m_col)]

def get_args():
	# checks that arguments are correct
	if len(sys.argv) != 3:
		sys.stderr.write("Incorrect number of args")
		sys.exit(1)
	else:
		puzzle = str(sys.argv[1])
		wordlist = str(sys.argv[2])
		return [puzzle, wordlist]

def main():
	puzzlewords = get_args()
	puzzle = puzzlewords[0]
	wordlist = puzzlewords[1]
	make_trie(wordlist) # set up the dictionary list
	make_crossmtrx(puzzle)

	horiz_outer_loop()
	vert_outer_loop()
	one_per_block()
	print_set_variables() # working


if __name__ == '__main__':
	main()
